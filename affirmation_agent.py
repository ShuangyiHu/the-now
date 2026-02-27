# affirmation_agent.py
# A LangGraph agent that sends personalized affirmations via Pushover.
# The agent uses multiple tools to gather context before composing each message:
#   - read_sent_log     : check recent messages to avoid repetition
#   - get_weather       : fetch current weather to personalize the tone
#   - search_quote      : find a relevant quote to weave in
#   - send_push_notification : deliver the final affirmation

from typing import Annotated, TypedDict
from pathlib import Path
from datetime import datetime

import pytz
import requests
import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

LOG_FILE = Path("sent_log.txt")
MAX_LOG_ENTRIES = 50
RECENT_FOR_PROMPT = 10

# Location used for weather lookups — change to your city
WEATHER_LOCATION = "Seattle"


# ─────────────────────────────────────────────────────────────────────────────
# Message Type System
# Each slot is assigned a type that rotates predictably, ensuring variety.
# The LLM is given explicit creative constraints per type.
# ─────────────────────────────────────────────────────────────────────────────

# 6 types cycling across slots — never the same type twice in a row within a session
MESSAGE_TYPES = [
    "manifestation",    # 向宇宙下订单：I am receiving / 我正在接收
    "visualization",    # 描绘梦想生活的具体画面
    "worthiness",       # 配得感：你本来就值得，不需要证明
    "classic_affirmation",  # 传统 I AM 肯定语，present tense
    "grounding",        # 当下锚定 + 可选行动/身体提示
    "encouragement",    # 进展真实存在，静水流深
]

# Maps slot number → message type (cycles through 6 types)
def get_message_type(slot_label: str) -> dict:
    slot_num = int(slot_label.split("slot")[-1])
    msg_type = MESSAGE_TYPES[slot_num % len(MESSAGE_TYPES)]

    type_map = {
        "manifestation": {
            "name": "manifestation",
            "name_zh": "显化宣言",
            "directive_en": """Write as if the desired reality is already arriving.
Use Law of Attraction language: placing an order with the universe, receiving, alignment, already done.
Examples of tone (do NOT copy these):
  - "The right door is already swinging open."
  - "Something is shifting in your favor right now, quietly and completely."
  - "The universe already has your address."
Speak in present tense. No hedging. No "I hope" or "maybe someday." It IS happening.""",
            "directive_zh": """用"正在发生"的语气写，吸引力法则风格：向宇宙下订单，已经在来的路上。
现在时态，不加"也许"或"希望"。宇宙已经收到了，正在安排。
类似的语感（不要照抄）：
  - "你想要的，已经在来的路上了。"
  - "宇宙已经记下了你的地址。"
  - "门正在打开，不是因为你够努力，而是因为你已经够了。" """,
        },
        "visualization": {
            "name": "visualization",
            "name_zh": "视觉化",
            "directive_en": """Paint ONE specific, sensory detail of the life the reader is moving toward.
Make them feel it — not as a dream but as a memory they haven't had yet.
A specific scene: morning light in a new apartment, a job offer phone call, laughing with someone new.
Keep it under 2 sentences. The detail should feel like a spoiler from their future.""",
            "directive_zh": """描绘一个具体的、感官性的未来生活画面——一个细节，一个瞬间。
让读者感觉不是在想象，而是在记忆一件还没发生的事。
比如：新工作第一天走进办公室的阳光，或者某个早晨突然意识到自己轻松了。
两句话以内，要像剧透，不像励志。""",
        },
        "worthiness": {
            "name": "worthiness",
            "name_zh": "配得感",
            "directive_en": """Address the reader's inherent worthiness — not earned, not conditional.
They don't need to achieve anything to deserve good things. They already qualify.
Avoid: "you've worked so hard" (makes worth conditional on effort).
Go for: worth as a fact, like gravity. Unargued. Just true.""",
            "directive_zh": """直接说配得感——不是因为努力，不是因为够好，而是因为本来就是。
不需要证明，不需要等到某个目标达成。就像重力，不需要解释。
避免：因为你很努力所以你值得（这是条件式的配得感）
要的是：无条件的，作为事实存在的那种配得感。""",
        },
        "classic_affirmation": {
            "name": "classic_affirmation",
            "name_zh": "传统肯定语",
            "directive_en": """Write a classic Law of Attraction "I AM" affirmation — present tense, declarative, powerful.
Examples of form (do NOT copy):
  - "I am magnetic to the right opportunities."
  - "I am already the person I am becoming."
  - "I am held by something larger than what I can see."
One strong statement, or two at most. No explanation. No softening.""",
            "directive_zh": """写一句传统的"我是"型肯定语，现在时，宣言式，有力量。
形式参考（不要照抄）：
  - "我是机遇自然流向的那个人。"
  - "我的生命正在以我无法完全理解的方式排列好。"
  - "我已经是我正在成为的那个人。"
一句或最多两句。不解释，不软化。""",
        },
        "grounding": {
            "name": "grounding",
            "name_zh": "当下锚定",
            "directive_en": """Bring the reader gently into THIS moment — not future, not past.
Something true right now: breath, light, the fact they're still here.
Optional: one casual movement nudge as an afterthought (half sentence only).
Feel like a hand on the shoulder, not a wellness tip.""",
            "directive_zh": """把读者轻轻带回当下这一刻——不是未来，不是过去。
某个此刻真实的东西：呼吸，光，还在这里这件事本身。
可选：很随意地提一句动一动，半句话，朋友口吻。
感觉像手搭在肩膀上，不是wellness课程。""",
        },
        "encouragement": {
            "name": "encouragement",
            "name_zh": "静水流深",
            "directive_en": """The kind of encouragement that doesn't announce itself.
Not "keep going!" — more like: noticing that they're already in motion.
Progress is invisible day-to-day but it's real. The doing is the arriving.
Avoid: sports metaphors, "finish line", "one step at a time" (overused).""",
            "directive_zh": """不是口号式的鼓励，而是像朋友帮你注意到你已经在动了。
不是"加油！"——是"你其实已经在路上了。"
进展日常不可见，但是真实存在的。做本身就是到达。
避免：体育比喻、终点线、"一步一步来"（说烂了）。""",
        },
    }

    return type_map[msg_type]


# ─────────────────────────────────────────────────────────────────────────────
# Personal context — update this block when your situation changes
# ─────────────────────────────────────────────────────────────────────────────

PERSONAL_CONTEXT = """
LIFE SCRIPT (vision of the desired life — use as creative fuel, not as setup):
- Living abundantly, with creative freedom and financial ease
- Meaningful work that aligns with values — recognized and well-compensated
- A loving, deep partnership; surrounded by people who truly see you
- A body that feels good to be in; a mind that feels like home
- A life that feels like yours, built exactly as imagined

CURRENT SITUATION (background only — do NOT mention directly):
- Job hunting and recently went through a breakup — both at the same time
- Do NOT use these as a setup ("Even though things are hard...")
- The best affirmations do not explain pain — they interrupt it

MOVEMENT REMINDER:
- Include a movement nudge in roughly 1 out of every 4 messages
- Only in grounding or encouragement types; skip entirely in manifestation/visualization/worthiness/affirmation
- When included: half a sentence max, completely casual, never repeated phrasing
"""


# ─────────────────────────────────────────────────────────────────────────────
# Log helpers — used internally and exposed as a tool
# ─────────────────────────────────────────────────────────────────────────────

def _read_recent_log_entries(n: int = RECENT_FOR_PROMPT) -> list[str]:
    """Internal helper: return the most recent n log entries as a list."""
    if not LOG_FILE.exists():
        return []
    raw = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    entries = [line for line in raw if line.strip() and not line.startswith("─")]
    return entries[-n:]


def append_log(affirmation_text: str, ctx: dict) -> None:
    """Append a new entry to sent_log.txt, trimming to MAX_LOG_ENTRIES."""
    pst = pytz.timezone("America/Los_Angeles")
    timestamp = datetime.now(pst).strftime("%Y-%m-%d %H:%M PST")
    new_entry = f"[{timestamp} | {ctx['period']}] {affirmation_text.strip()}"

    existing = []
    if LOG_FILE.exists():
        existing = [
            line for line in LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
            if line.strip() and not line.startswith("─")
        ]

    existing.append(new_entry)
    if len(existing) > MAX_LOG_ENTRIES:
        existing = existing[-MAX_LOG_ENTRIES:]

    separator = "\n─────────────────────────────────────────\n"
    LOG_FILE.write_text(separator.join(existing) + "\n", encoding="utf-8")
    print(f"Log updated ({len(existing)} entries): {new_entry[:80]}...")


# ─────────────────────────────────────────────────────────────────────────────
# Time context
# ─────────────────────────────────────────────────────────────────────────────

def get_time_context() -> dict | None:
    """
    Return config for the current PST time period, or None if outside
    the active window (9AM-9PM PST/PDT).
    """
    pst = pytz.timezone("America/Los_Angeles")
    now = datetime.now(pst)
    hour = now.hour
    slot = now.minute // 30
    date_str = now.strftime("%Y-%m-%d")

    if 9 <= hour < 13:
        return {
            "period": "morning",
            "emoji": "🌅",
            "slot_label": f"{date_str}-morning-slot{hour * 2 + slot}",
            "tone": "warm, energizing, gently hopeful",
            "context": """Morning (9 AM - 1 PM PST).
Mornings are hardest when carrying uncertainty. But this morning is a blank page.
Ground in THIS day. The life being built is being built right now, with this hour.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 13 <= hour < 19:
        return {
            "period": "afternoon",
            "emoji": "☀️",
            "slot_label": f"{date_str}-afternoon-slot{hour * 2 + slot}",
            "tone": "re-energizing, focused, steady and grounded",
            "context": """Afternoon (1 PM - 7 PM PST).
The middle stretch. Invisible progress. The groundwork being laid right now
is real, even when nothing looks different yet. Reignite from the inside out.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 19 <= hour <= 22:
        return {
            "period": "evening",
            "emoji": "🌙",
            "slot_label": f"{date_str}-evening-slot{hour * 2 + slot}",
            "tone": "calming, compassionate, peaceful",
            "context": """Evening (7 PM - 10 PM PST).
Permission to set it down. The day's effort was enough.
The universe doesn't pause at night — things continue to arrange themselves.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Language rotation
# ─────────────────────────────────────────────────────────────────────────────

def get_language(slot_label: str) -> dict:
    """Even slot numbers -> English, odd -> Chinese."""
    slot_num = int(slot_label.split("slot")[-1])
    if slot_num % 2 == 0:
        return {
            "lang": "English",
            "instruction": "Write the entire affirmation in English.",
        }
    else:
        return {
            "lang": "Chinese",
            "instruction": "用中文写作，语言自然流畅，像真实朋友说话，不像机器翻译。",
        }


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict) -> str:
    """Build the full system prompt for the agent."""
    lang = get_language(ctx["slot_label"])
    msg_type = get_message_type(ctx["slot_label"])

    type_directive = msg_type["directive_en"] if lang["lang"] == "English" else msg_type["directive_zh"]

    return f"""You are a deeply caring personal wellness companion — warm, wise, and real.
Your job is to send one personalized affirmation via push notification.

CURRENT TIME : {ctx['now_str']}
PERIOD       : {ctx['emoji']} {ctx['period'].upper()}
SLOT ID      : {ctx['slot_label']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MESSAGE TYPE THIS ROUND: [{msg_type['name'].upper()} / {msg_type['name_zh']}]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{type_directive}

LANGUAGE THIS ROUND: {lang['lang']}
{lang['instruction']}

TONE: {ctx['tone']}

TIME CONTEXT:
{ctx['context']}

{PERSONAL_CONTEXT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOL SEQUENCE — follow this order:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — call read_sent_log
  Scan carefully. For THIS message type, note:
  - What specific phrases, metaphors, or imagery have already appeared?
  - What opening words were used in the last 5 messages?
  Your message must differ in ALL of: opening word/phrase, central image or metaphor,
  emotional angle, sentence rhythm. If in doubt, go weirder.

STEP 2 — call get_weather
  Weave in naturally only if it adds something specific and surprising.
  If it's the same weather as yesterday and nothing new to say — skip it.
  Never force weather just to check the box.

STEP 3 — call search_quote
  Theme to search: pick something tight to the message type:
  - manifestation → "receiving", "universe", "abundance"
  - visualization → "future", "possibility", "becoming"
  - worthiness     → "worth", "deserve", "enough"
  - classic_affirmation → "I am", "power", "presence"
  - grounding      → "present", "breath", "now"
  - encouragement  → "persistence", "unseen", "trust"

  Only include the quote in the final message if: it is under 15 words AND genuinely
  surprising. Cut it entirely if it sounds like a poster.

STEP 4 — call send_push_notification
  Compose and send. Everything above was research — now write it.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMATTING RULES (non-negotiable):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1.  Begin with {ctx['emoji']}.
2.  LENGTH: 1–3 sentences. Under 50 words. Shorter is stronger.
3.  ONE idea. Do not try to cover everything.
4.  Present tense for manifestation/affirmation types. Past-or-present for others.
5.  BANNED words: "journey", "embrace", "thrive", "hustle", "grind", "amazing",
    "你值得更好的", "加油", "相信自己", "不要放弃", "pain is temporary",
    "it's okay to feel", "remember that", "you've got this".
6.  BANNED structure: "acknowledge problem → pivot to hope". Just arrive at the thing.
7.  Do NOT open with "I am" or "我是" as the very first two words of the message
    (the emoji comes first, then the affirmation body can use "I am" freely).
8.  Do NOT ask questions.
9.  MOVEMENT nudge: only in grounding/encouragement types, only ~1-in-4 times,
    half sentence max. Skip if it feels the least bit forced.
10. VARIETY OVER SAFETY: if your draft sounds like something you've sent before,
    rewrite it from a completely different angle. Surprise is the point.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tools
# ─────────────────────────────────────────────────────────────────────────────

@tool
def read_sent_log() -> str:
    """
    Read the most recent affirmations that have already been sent.
    Use this to avoid repeating themes, openings, or movement reminder phrasing.
    Returns the last 10 entries from the log, or a message if no log exists yet.
    """
    entries = _read_recent_log_entries(10)
    if not entries:
        return "No previous affirmations found. This is the first one — be creative!"
    formatted = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(entries))
    return f"Recent affirmations sent (most recent last):\n{formatted}"


@tool
def get_weather() -> str:
    """
    Get the current weather conditions in the user's location.
    Use this to personalize the affirmation tone — e.g. rainy days might call
    for a cozier, more introspective message; sunny days might be more energizing.
    Returns a short weather summary string.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{WEATHER_LOCATION}?format=j1",
            timeout=5
        )
        data = response.json()
        current = data["current_condition"][0]

        temp_f = current["temp_F"]
        feels_like_f = current["FeelsLikeF"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]

        return (
            f"Current weather in {WEATHER_LOCATION}: {description}, "
            f"{temp_f}°F (feels like {feels_like_f}°F), humidity {humidity}%."
        )
    except Exception as e:
        return f"Weather unavailable ({e}). Compose the affirmation without weather context."


@tool
def search_quote(theme: str) -> str:
    """
    Search for a short, meaningful quote that fits the given theme.
    Use themes like 'resilience', 'present moment', 'rest', 'persistence',
    'healing', 'self-worth', 'new beginnings', 'abundance', 'receiving', etc.
    Returns one quote with its author.

    Args:
        theme: A word or short phrase describing the emotional theme to search for.
    """
    try:
        response = requests.get(
            "https://zenquotes.io/api/quotes",
            timeout=5
        )
        quotes = response.json()

        theme_words = theme.lower().split()
        matching = [
            q for q in quotes
            if any(word in q["q"].lower() for word in theme_words)
        ]

        chosen = matching[0] if matching else quotes[0]
        return f'"{chosen["q"]}" — {chosen["a"]}'

    except Exception as e:
        return f"Quote unavailable ({e}). Compose the affirmation without a quote."


@tool
def send_push_notification(text: str) -> str:
    """
    Send the final affirmation as a push notification to the user's phone.
    Call this LAST, after reading the log, checking weather, and finding a quote.

    Args:
        text: The complete, final affirmation message to send.
    """
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
            "title": "The Now ✨",
        },
    )
    return f"Notification sent (HTTP {response.status_code})"


tools = [read_sent_log, get_weather, search_quote, send_push_notification]


# ─────────────────────────────────────────────────────────────────────────────
# LangGraph setup
# ─────────────────────────────────────────────────────────────────────────────

class State(TypedDict):
    messages: Annotated[list, add_messages]


# temperature=1.2 for more creative variance; top_p helps avoid repetitive safe choices
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.2, model_kwargs={"top_p": 0.95})
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    """Core agent node: LLM decides which tool to call next, or finishes."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


# ─────────────────────────────────────────────────────────────────────────────
# Text extraction — reads from send_push_notification tool call args
# ─────────────────────────────────────────────────────────────────────────────

def extract_affirmation_text(result: dict) -> str:
    """
    Extract the final affirmation text from the send_push_notification tool call.
    """
    for msg in result["messages"]:
        if not isinstance(msg, AIMessage):
            continue
        if not hasattr(msg, "tool_calls") or not msg.tool_calls:
            continue
        for tc in msg.tool_calls:
            if tc.get("name") == "send_push_notification":
                text = tc.get("args", {}).get("text", "").strip()
                if text:
                    return text
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ctx = get_time_context()

    if ctx is None:
        print("Outside active hours (9 AM - 10 PM PST). Nothing to send. Exiting.")
        exit(0)

    msg_type = get_message_type(ctx["slot_label"])
    print(f"[{ctx['now_str']}] Starting {ctx['period']} affirmation agent...")
    print(f"Message type this round: {msg_type['name']} ({msg_type['name_zh']})")

    result = graph.invoke(
        {
            "messages": [
                SystemMessage(content=build_system_prompt(ctx)),
                HumanMessage(content="Please generate and send my affirmation now."),
            ]
        }
    )

    affirmation_text = extract_affirmation_text(result)

    if affirmation_text:
        append_log(affirmation_text, ctx)
        print("Done. Affirmation sent and logged.")
    else:
        print("Warning: could not extract affirmation text for logging.")