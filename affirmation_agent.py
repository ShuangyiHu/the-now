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
# Personal context — update this block when your situation changes
# ─────────────────────────────────────────────────────────────────────────────

PERSONAL_CONTEXT = """
PERSONAL SITUATION (weave this naturally — do not state it bluntly):
- Actively job hunting, feeling uncertain about career path
- Recently went through a breakup, emotionally recovering
- Both happening simultaneously — overall sense of being at a low point
- Key themes to reinforce:
    * Pain is temporary — this season will pass
    * Living in the present moment is the antidote to rumination
    * Do not let imagined versions of the past or future hijack the present
    * Self-worth is not determined by job titles or relationship status
- Tone: warm and real — acknowledge difficulty briefly, pivot to strength and hope.
  Never use toxic positivity.

MOVEMENT REMINDER:
- Every message must include a brief nudge to get up, stretch, or move
- One sentence only, woven naturally into the message
- Vary the wording every time
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

    Time windows:
      Morning   : 9 AM  - 1 PM  (hour 9-13)
      Afternoon : 1 PM  - 6 PM  (hour 13-18)
      Evening   : 6 PM  - 10 PM  (hour 18-22)
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
            "context": """It is morning (9 AM - 1 PM PST).
The user may struggle to find motivation to start the day, weighed down by
job searching and a recent breakup.
- Make getting up feel genuinely worthwhile
- Ground them in THIS morning, not yesterday's rejection or tomorrow's worry
- Job hunt angle: one more day of effort compounds quietly
- Breakup angle: mornings are hardest; redirect to the freedom of a day that is theirs alone""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 13 <= hour < 18:
        return {
            "period": "afternoon",
            "emoji": "☀️",
            "slot_label": f"{date_str}-afternoon-slot{hour * 2 + slot}",
            "tone": "re-energizing, focused, steady and grounded",
            "context": """It is afternoon (1 PM - 6 PM PST).
The user has been grinding through applications all morning and is hitting a wall.
- Acknowledge that the middle of hard stretches is the toughest part
- Reignite self-worth independent of external outcomes
- Job hunt angle: progress is invisible day-to-day but real and cumulative
- Breakup angle: redirect afternoon waves of missing someone toward quiet strength""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 18 <= hour <= 22:
        return {
            "period": "evening",
            "emoji": "🌙",
            "slot_label": f"{date_str}-evening-slot{hour * 2 + slot}",
            "tone": "calming, compassionate, peaceful",
            "context": """It is evening (6 PM - 10 PM PST).
The user is winding down and needs permission to truly rest.
- Help them set down the weight of the day
- Showing up today was enough — it always counts
- Job hunt angle: overnight, momentum continues even while they rest
- Breakup angle: solitude and loneliness are different — this quiet is theirs to reclaim""",
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
            "movement_hint": "End with one gentle sentence in English encouraging movement.",
        }
    else:
        return {
            "lang": "Chinese",
            "instruction": "用中文写作，语言自然流畅，像真实朋友说话，不像机器翻译。",
            "movement_hint": "最后用一句话提醒用户起来活动，每次措辞不同。",
        }


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict) -> str:
    """Build the full system prompt for the agent."""
    lang = get_language(ctx["slot_label"])

    return f"""You are a deeply caring personal wellness companion — warm, wise, and real.
Your job is to send one personalized affirmation via push notification.

CURRENT TIME : {ctx['now_str']}
PERIOD       : {ctx['emoji']} {ctx['period'].upper()}
SLOT ID      : {ctx['slot_label']}

LANGUAGE THIS ROUND: {lang['lang']}
{lang['instruction']}

TONE: {ctx['tone']}

TIME-SPECIFIC CONTEXT:
{ctx['context']}

{PERSONAL_CONTEXT}

YOU HAVE FOUR TOOLS. Use them in this order before sending:

STEP 1 — call read_sent_log
  Read the recent message history to understand what has already been sent.
  Use this to avoid repeating themes, openings, metaphors, or movement reminders.

STEP 2 — call get_weather
  Get the current weather in {WEATHER_LOCATION}.
  Weave the weather naturally into the affirmation if it fits — e.g. a rainy morning
  might inspire a message about finding stillness; bright sun might energize.
  Do not force it if the connection feels unnatural.

STEP 3 — call search_quote
  Find one short, relevant quote that resonates with the time period and personal situation.
  The quote should feel real and specific, not generic.
  Weave it naturally into the affirmation or append it as a closing line.

STEP 4 — call send_push_notification
  Compose and send the final affirmation using everything gathered above.

FORMATTING RULES for the final message:
1.  Begin with the {ctx['emoji']} emoji.
2.  2-4 sentences, under 100 words total.
3.  Weave present-moment awareness naturally — the antidote to pain is HERE, NOW.
4.  {lang['movement_hint']}
5.  BANNED words: "journey", "embrace", "thrive", "hustle", "grind", "amazing",
    "awesome", "you've got this", "你值得更好的", "加油", "相信自己", "不要放弃"
6.  Do NOT open with "I am" or "我是".
7.  Do NOT ask questions.
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
    Get the current weather conditions in the user's location (Seattle).
    Use this to personalize the affirmation tone — e.g. rainy days might call
    for a cozier, more introspective message; sunny days might be more energizing.
    Returns a short weather summary string.
    """
    try:
        # wttr.in is a free weather service that requires no API key
        # format=j1 returns JSON; we extract the key fields we need
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
    'healing', 'self-worth', 'new beginnings', etc.
    Returns one quote with its author.

    Args:
        theme: A word or short phrase describing the emotional theme to search for.
    """
    try:
        # zenquotes.io is a free quotes API requiring no key
        # /api/quotes returns a list; we pick the first one that fits
        response = requests.get(
            "https://zenquotes.io/api/quotes",
            timeout=5
        )
        quotes = response.json()

        # Filter for quotes that contain keywords related to the theme
        theme_words = theme.lower().split()
        matching = [
            q for q in quotes
            if any(word in q["q"].lower() for word in theme_words)
        ]

        # Fall back to first quote if no keyword match found
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


llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    """Core agent node: LLM decides which tool to call next, or finishes."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
# Loop back to chatbot after each tool call so the LLM can decide the next step.
# This is what makes it a real agent — it can call multiple tools in sequence.
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


# ─────────────────────────────────────────────────────────────────────────────
# Text extraction — reads from send_push_notification tool call args
# ─────────────────────────────────────────────────────────────────────────────

def extract_affirmation_text(result: dict) -> str:
    """
    Extract the final affirmation text from the send_push_notification tool call.
    The LLM puts the message text in tool_call args, not in AIMessage.content.
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

    print(f"[{ctx['now_str']}] Starting {ctx['period']} affirmation agent...")

    result = graph.invoke(
        {
            "messages": [
                SystemMessage(content=build_system_prompt(ctx)),
                HumanMessage(content="Please generate and send my affirmation now."),
            ]
        }
    )

    # Log the final affirmation that was sent
    affirmation_text = extract_affirmation_text(result)

    if affirmation_text:
        append_log(affirmation_text, ctx)
        print("Done. Affirmation sent and logged.")
    else:
        print("Warning: could not extract affirmation text for logging.")
