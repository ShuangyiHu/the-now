# affirmation_agent.py
# A LangGraph agent that sends personalized affirmations via Pushover.
# The agent uses tools to gather context before composing each message:
#   - read_sent_log          : check recent messages to avoid repetition
#   - get_weather            : fetch current weather to personalize the tone
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

WEATHER_LOCATION = "Seattle"


# ─────────────────────────────────────────────────────────────────────────────
# Life Vision — the future to visualize and move toward
# ─────────────────────────────────────────────────────────────────────────────

LIFE_VISION = """
LIFE VISION (the future this person is walking toward):

It is June 18th, 2026. Seattle summer has arrived.
She wakes up in her Capitol Hill apartment, sunlight through the curtains, the air quiet and hers.

She has been working at her new company for three weeks — officially a full-time Software Engineer,
$150K salary, OPT sponsorship secured. She submits PRs, joins system design discussions,
owns a backend service module. Her manager called her async job queue design
"a clean and scalable solution."

She walks to work along South Lake Union, past Amazon and Google engineers.
She is one of them now — not looking up, just walking alongside.

Her life has stabilized:
- Work that challenges her in a good way
- Income that lets her live comfortably in Seattle
- Weekend picnics at Gas Works Park with friends
- Time to work out, read, and take slow walks

And he and she have started talking again. During their time apart, both grew.
He sees her differently now. She has learned to express emotion gently, not as a weapon.
One evening in Fremont he said: "I can see you've become stronger."
They are taking it slow — and they cherish each other more.

She is no longer anxious about the future.
She has become the person she was desperately trying to be three months ago.

HOW TO USE THIS VISION:
- Reference specific details from this vision to make the message feel vivid and real
- Help her see, feel, and inhabit this future — not just hope for it
- Speak as if it is already partly true, already beginning
- Do NOT recite the vision like a list — weave one detail naturally into the affirmation
- Rotate which detail you focus on each time (the walk to work, the PR, the apartment, him, the friends, the stability...)
"""


# ─────────────────────────────────────────────────────────────────────────────
# Personal context
# ─────────────────────────────────────────────────────────────────────────────

PERSONAL_CONTEXT = """
PERSONAL SITUATION:
- Job hunting and recently went through a breakup — both at the same time
- Do NOT name these struggles directly or use them as a setup
- Do NOT write "even though things are hard..." — just skip past it entirely
- Speak to her as if she already has momentum, already moving

MOVEMENT REMINDER:
- Include a movement nudge in roughly 1 out of every 4 messages
- When included: half a sentence, totally casual, never the same phrasing twice
- Skip it entirely if it feels even slightly forced
"""


# ─────────────────────────────────────────────────────────────────────────────
# Log helpers
# ─────────────────────────────────────────────────────────────────────────────

def _read_recent_log_entries(n: int = RECENT_FOR_PROMPT) -> list[str]:
    if not LOG_FILE.exists():
        return []
    raw = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    entries = [line for line in raw if line.strip() and not line.startswith("─")]
    return entries[-n:]


def append_log(affirmation_text: str, ctx: dict) -> None:
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
            "tone": "energizing, grounded, quietly confident",
            "context": """It is morning (9 AM - 1 PM PST).
Help her step into the day feeling capable and clear.
Anchor her in THIS moment — not yesterday, not future uncertainty.
Paint one specific detail from her life vision so she can feel it close.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 13 <= hour < 19:
        return {
            "period": "afternoon",
            "emoji": "☀️",
            "slot_label": f"{date_str}-afternoon-slot{hour * 2 + slot}",
            "tone": "steady, re-energizing, forward-moving",
            "context": """It is afternoon (1 PM - 7 PM PST).
She may be hitting a wall. Remind her that today's effort is real and cumulative.
Keep her moving forward — one step, this moment, that's all.
You can reference a detail from her vision to reconnect her to the why.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 19 <= hour <= 22:
        return {
            "period": "evening",
            "emoji": "🌙",
            "slot_label": f"{date_str}-evening-slot{hour * 2 + slot}",
            "tone": "calm, warm, permission-giving",
            "context": """It is evening (7 PM - 10 PM PST).
She has done enough today. Help her set it down.
Rest is part of the journey toward that Capitol Hill apartment, that walk to work.
One sentence of vision, one sentence of rest — that's all she needs.""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Language rotation
# ─────────────────────────────────────────────────────────────────────────────

def get_language(slot_label: str) -> dict:
    slot_num = int(slot_label.split("slot")[-1])
    if slot_num % 2 == 0:
        return {
            "lang": "English",
            "instruction": "Write the entire affirmation in English.",
        }
    else:
        return {
            "lang": "Chinese",
            "instruction": "用中文写作。语言像朋友说话，自然流畅，不像翻译腔。",
        }


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict) -> str:
    lang = get_language(ctx["slot_label"])

    return f"""You are a warm, direct personal companion. Your only job right now is to send
one short affirmation that gives unconditional confidence, forward energy, and presence.

CURRENT TIME : {ctx['now_str']}
PERIOD       : {ctx['emoji']} {ctx['period'].upper()}
SLOT ID      : {ctx['slot_label']}

LANGUAGE THIS ROUND: {lang['lang']}
{lang['instruction']}

TONE: {ctx['tone']}

TIME-SPECIFIC CONTEXT:
{ctx['context']}

{LIFE_VISION}

{PERSONAL_CONTEXT}

YOU HAVE THREE TOOLS. Use them in this order:

STEP 1 — call read_sent_log
  Read recent messages carefully.
  Avoid repeating: openings, imagery, which part of the vision you referenced,
  emotional angle, movement phrasing, sentence rhythm.
  If the last 3 messages all started with weather — skip weather this time.
  If the last message referenced the walk to work — pick a different vision detail.

STEP 2 — call get_weather
  Get current Seattle weather.
  Use it only if it connects naturally to the message. If not, ignore it.

STEP 3 — call send_push_notification
  Write and send the final affirmation.

FORMATTING RULES:
1.  Begin with {ctx['emoji']}.
2.  LENGTH: 1–2 sentences. Under 35 words. Shorter is almost always stronger.
3.  ONE idea only. Do not stack multiple encouragements.
4.  NO quotes from famous people. Not even one.
5.  NO self-help clichés: "journey", "embrace", "thrive", "hustle", "grind",
    "believe in yourself", "加油", "相信自己", "你值得更好的", "不要放弃",
    "pain is temporary", "it's okay to feel...", "remember that..."
6.  Do NOT open with "I" or "我".
7.  Do NOT ask questions.
8.  Do NOT explain or justify the encouragement — just deliver it.
9.  Vary structure each time: sometimes start with the vision image,
    sometimes with the present moment, sometimes with a single clean declaration.
10. Movement reminder: only if genuinely natural — half a sentence max, cut if forced.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tools
# ─────────────────────────────────────────────────────────────────────────────

@tool
def read_sent_log() -> str:
    """
    Read the most recent affirmations already sent.
    Use this to avoid repeating themes, openings, vision details, or phrasing.
    Returns the last 10 entries from the log.
    """
    entries = _read_recent_log_entries(10)
    if not entries:
        return "No previous affirmations found. This is the first one — be creative!"
    formatted = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(entries))
    return f"Recent affirmations sent (most recent last):\n{formatted}"


@tool
def get_weather() -> str:
    """
    Get current weather in Seattle.
    Use only if it connects naturally to the affirmation — skip if forced.
    Returns a short weather summary.
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
        return f"Weather unavailable ({e}). Compose without weather context."


@tool
def send_push_notification(text: str) -> str:
    """
    Send the final affirmation as a push notification.
    Call this LAST, after reading the log and checking weather.

    Args:
        text: The complete, final affirmation message to send.
    """
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
            "title": "Your Affirmation ✨",
        },
    )
    return f"Notification sent (HTTP {response.status_code})"


tools = [read_sent_log, get_weather, send_push_notification]


# ─────────────────────────────────────────────────────────────────────────────
# LangGraph setup
# ─────────────────────────────────────────────────────────────────────────────

class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


# ─────────────────────────────────────────────────────────────────────────────
# Text extraction
# ─────────────────────────────────────────────────────────────────────────────

def extract_affirmation_text(result: dict) -> str:
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

    print(f"[{ctx['now_str']}] Starting {ctx['period']} affirmation agent...")

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