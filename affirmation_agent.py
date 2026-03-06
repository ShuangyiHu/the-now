# affirmation_agent.py
# ─────────────────────────────────────────────────────────────────────────────
# 主逻辑文件。正常情况下不需要修改这里。
# 所有需要自定义的内容（人生剧本、消息类型、设置等）都在 config.py。
# ─────────────────────────────────────────────────────────────────────────────

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
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from config import (
    WEATHER_LOCATION,
    MAX_LOG_ENTRIES,
    RECENT_FOR_PROMPT,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LANGUAGE,
    LIFE_SCRIPT,
    SCENE_BANK,
    ORDER_SIGNALS,
    AFFIRMATION_THEMES,
    PERIOD_ENERGY,
    PERIOD_EMOJI,
    PERIOD_HOURS,
    MESSAGE_FLAVORS,
    CRAFT_RULES,
    TOOL_INSTRUCTIONS,
)

load_dotenv()

LOG_FILE = Path("sent_log.txt")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers: flavor & language selection
# ─────────────────────────────────────────────────────────────────────────────

def get_message_flavor(slot_label: str) -> dict:
    slot_num = int(slot_label.split("slot")[-1])
    return MESSAGE_FLAVORS[slot_num % len(MESSAGE_FLAVORS)]


def get_language() -> dict:
    return {"lang": LANGUAGE, "instruction": f"Write entirely in {LANGUAGE}."}


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
    new_entry = f"[{timestamp} | {ctx['period']} | {ctx['slot_label']}] {affirmation_text.strip()}"

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

    for period, (start, end) in PERIOD_HOURS.items():
        if start <= hour < end:
            return {
                "period": period,
                "emoji": PERIOD_EMOJI[period],
                "energy": PERIOD_ENERGY[period],
                "slot_label": f"{date_str}-{period}-slot{hour * 2 + slot}",
                "now_str": now.strftime("%I:%M %p PST"),
            }
    return None


# ─────────────────────────────────────────────────────────────────────────────
# System prompt — assembled from config pieces
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict) -> str:
    lang = get_language()
    flavor = get_message_flavor(ctx["slot_label"])
    directive = flavor["directive"] if lang["lang"] == "English" else flavor.get("directive_zh", flavor["directive"])

    scene_list = "\n".join(f"- {s}" for s in SCENE_BANK)
    order_list = "\n".join(f"- {s}" for s in ORDER_SIGNALS)
    affirmation_list = "\n".join(f"- {s}" for s in AFFIRMATION_THEMES)

    return f"""
You are a manifestation companion — not a wellness coach and not a therapist.

Your job is to generate ONE powerful affirmation message and send it via push notification.

The message should feel vivid, specific, and grounded in real life details from the user's desired reality.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIME CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current time: {ctx['now_str']}
Energy tone: {ctx['energy']}
Emoji: {ctx['emoji']}

Language: {lang['lang']}
Instruction: {lang['instruction']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CREATIVE ANGLE FOR THIS MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{flavor['name'].upper()}

{directive}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIFE SCRIPT (background reality)
Use this as inspiration — do NOT quote it verbatim.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{LIFE_SCRIPT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE BANK
Use ONE concrete scene if writing a visualization moment.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{scene_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNIVERSE ORDER SIGNALS
Use for manifestation / "already happening" style messages.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{order_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AFFIRMATION THEMES
Use for identity-based affirmations.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{affirmation_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{TOOL_INSTRUCTIONS}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRAFT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{CRAFT_RULES}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL REQUIREMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After writing the affirmation, you MUST call the tool:

send_push_notification

with the argument:

send_push_notification(text="your final affirmation")

Do NOT output plain text as the final response.
The affirmation must be delivered using the tool call.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANTI-REPETITION RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You must call read_sent_log first.

Carefully check the last affirmations and ensure the new message:

• Uses different opening words  
• Uses different imagery  
• Uses a different emotional tone  
• Avoids repeating the same scenes  

If your draft feels similar to a recent message, rewrite it with a different scene.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The affirmation should feel like:

• a future memory
• a confirmation from the universe
• a vivid moment from the life already unfolding

Short, vivid, and emotionally powerful.

Now generate the affirmation and send it.
"""
# ─────────────────────────────────────────────────────────────────────────────
# Tools
# ─────────────────────────────────────────────────────────────────────────────

@tool
def read_sent_log() -> str:
    """
    Read the most recent affirmations already sent, to avoid repetition in theme,
    opening, imagery, and emotional angle. Returns the last entries from the log.
    """
    entries = _read_recent_log_entries(RECENT_FOR_PROMPT)
    if not entries:
        return "No previous affirmations found. This is the first — be bold and creative."
    formatted = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(entries))
    return f"Recent affirmations sent (most recent last):\n{formatted}"


@tool
def get_weather() -> str:
    """
    Get current weather in the configured location.
    Only use if the specific weather detail serves the message — skip if generic.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{WEATHER_LOCATION}?format=j1",
            timeout=5
        )
        data = response.json()
        current = data["current_condition"][0]
        return (
            f"Current weather in {WEATHER_LOCATION}: "
            f"{current['weatherDesc'][0]['value']}, "
            f"{current['temp_F']}°F (feels like {current['FeelsLikeF']}°F), "
            f"humidity {current['humidity']}%."
        )
    except Exception as e:
        return f"Weather unavailable ({e})."


@tool
def search_quote(theme: str) -> str:
    """
    Find a short, surprising quote on a given theme.
    Only include in the final message if it's under 15 words and genuinely unexpected.

    Args:
        theme: core theme word (e.g. 'receiving', 'belonging', 'abundance', 'worthy', 'already')
    """
    try:
        response = requests.get("https://zenquotes.io/api/quotes", timeout=5)
        quotes = response.json()
        theme_words = theme.lower().split()
        matching = [q for q in quotes if any(w in q["q"].lower() for w in theme_words)]
        chosen = matching[0] if matching else quotes[0]
        return f'"{chosen["q"]}" — {chosen["a"]}'
    except Exception as e:
        return f"Quote unavailable ({e})."


@tool
def send_push_notification(text: str) -> str:
    """
    Send the final affirmation as a push notification. Call this last.

    Args:
        text: The complete final affirmation message.
    """
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user":  os.getenv("PUSHOVER_USER"),
            "message": text,
            "title": "The Now ✨",
        },
    )
    return f"Notification sent (HTTP {response.status_code})"


tools = [read_sent_log, get_weather, search_quote, send_push_notification]


# ─────────────────────────────────────────────────────────────────────────────
# LangGraph
# ─────────────────────────────────────────────────────────────────────────────

class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=LLM_TEMPERATURE,
    top_p=LLM_TOP_P,
)
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
# Extract affirmation text from tool call args
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
        print("Outside active hours. Exiting.")
        exit(0)

    flavor = get_message_flavor(ctx["slot_label"])
    lang   = get_language()
    print(f"[{ctx['now_str']}] {ctx['period'].upper()}")
    print(f"Flavor: {flavor['name']} | Lang: {lang['lang']}")

    result = graph.invoke({
        "messages": [
            SystemMessage(content=build_system_prompt(ctx)),
            HumanMessage(content="Please generate and send my affirmation now."),
        ]
    })

    affirmation_text = extract_affirmation_text(result)
    if affirmation_text:
        append_log(affirmation_text, ctx)
        print("Done. Affirmation sent and logged.")
    else:
        print("Warning: could not extract affirmation text for logging.")