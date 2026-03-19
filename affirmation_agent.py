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
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import (
    WEATHER_LOCATION,
    MAX_LOG_ENTRIES,
    RECENT_FOR_PROMPT,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LANGUAGE,
    # Split content pools — agent injects the right set per flavor type
    LIFE_SCRIPT_GENERAL,
    LIFE_SCRIPT_INTERVIEW,
    SCENE_BANK_GENERAL,
    SCENE_BANK_INTERVIEW,
    ORDER_SIGNALS_GENERAL,
    ORDER_SIGNALS_INTERVIEW,
    AFFIRMATION_THEMES_GENERAL,
    AFFIRMATION_THEMES_INTERVIEW,
    PERIOD_ENERGY,
    PERIOD_EMOJI,
    PERIOD_HOURS,
    MESSAGE_FLAVORS,
    GENERAL_FLAVOR_INDICES,
    INTERVIEW_FLAVOR_INDICES,
    CRAFT_RULES,
    TOOL_INSTRUCTIONS,
)

load_dotenv()

LOG_FILE = Path("sent_log.txt")


# ─────────────────────────────────────────────────────────────────────────────
# Flavor selection
#
# Rotation pattern (every 3 messages):
#   position 0 → general flavor
#   position 1 → general flavor
#   position 2 → interview flavor
# ─────────────────────────────────────────────────────────────────────────────

def get_message_flavor(log_entry_count: int) -> dict:
    cycle_position = log_entry_count % 3

    if cycle_position == 2:
        interview_slot_number = log_entry_count // 3
        interview_index = interview_slot_number % len(INTERVIEW_FLAVOR_INDICES)
        return MESSAGE_FLAVORS[INTERVIEW_FLAVOR_INDICES[interview_index]]
    else:
        full_cycles = log_entry_count // 3
        general_count = full_cycles * 2 + cycle_position
        general_index = general_count % len(GENERAL_FLAVOR_INDICES)
        return MESSAGE_FLAVORS[GENERAL_FLAVOR_INDICES[general_index]]


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


def _count_log_entries() -> int:
    if not LOG_FILE.exists():
        return 0
    raw = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    return sum(1 for line in raw if line.strip() and not line.startswith("─"))


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
# System prompt
#
# KEY CHANGE (V7): The prompt is built from two completely separate content
# pools. Interview content (TikTok, coding round, offer, recruiter) is
# PHYSICALLY ABSENT from the general-slot prompt — not just warned against.
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict, flavor: dict) -> str:
    lang = get_language()
    flavor_id = flavor["id"]
    is_interview = flavor_id in ("tiktok_interview", "tiktok_cheerleader")

    # Select the right content pools
    if is_interview:
        life_script    = LIFE_SCRIPT_INTERVIEW
        scene_bank     = SCENE_BANK_INTERVIEW
        order_signals  = ORDER_SIGNALS_INTERVIEW
        affirmation_themes = AFFIRMATION_THEMES_INTERVIEW
        slot_header    = "INTERVIEW SLOT — write about TikTok USDS interview only."
        diversity_rule = ""
    else:
        life_script    = LIFE_SCRIPT_GENERAL
        scene_bank     = SCENE_BANK_GENERAL
        order_signals  = ORDER_SIGNALS_GENERAL
        affirmation_themes = AFFIRMATION_THEMES_GENERAL
        slot_header    = "GENERAL SLOT — write from the life areas below (career, love, travel, friends, or inner state)."
        diversity_rule = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOPIC DIVERSITY RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The life script has five areas: CAREER, LOVE, TRAVEL, FRIENDS, INNER STATE.

After reading the log, identify which area appeared LEAST recently.
Write about that area.

Do not write about the same area two general messages in a row.
"""

    scene_list      = "\n".join(f"- {s}" for s in scene_bank)
    order_list      = "\n".join(f"- {s}" for s in order_signals)
    affirmation_list = "\n".join(f"- {s}" for s in affirmation_themes)

    return f"""
You are a manifestation companion — not a wellness coach and not a therapist.

Your job is to generate ONE powerful affirmation message and send it via push notification.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLOT TYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{slot_header}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIME CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current time: {ctx['now_str']}
Energy tone: {ctx['energy']}
Emoji: {ctx['emoji']}
Language: {lang['lang']} — {lang['instruction']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THIS MESSAGE'S FLAVOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flavor: {flavor['name'].upper()}

{flavor['directive']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIFE SCRIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{life_script}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE BANK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{scene_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ORDER SIGNALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{order_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AFFIRMATION THEMES
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
ANTI-REPETITION RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Call read_sent_log first.

Ensure the new message:
• Uses different opening words
• Uses different imagery
• Uses a different emotional tone
• Avoids repeating the same scenes

For interview messages: check which STYLE (A/B/C/D/E) appeared recently — pick a different one.
{diversity_rule}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Short, vivid, emotionally specific. Like a future memory or a confirmation from the universe.

Now generate the affirmation and send it.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tools
# ─────────────────────────────────────────────────────────────────────────────

@tool
def read_sent_log() -> str:
    """
    Read recent affirmations to avoid repeating theme, imagery, or emotional angle.
    """
    entries = _read_recent_log_entries(RECENT_FOR_PROMPT)
    if not entries:
        return "No previous affirmations. This is the first — be bold and creative."
    formatted = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(entries))
    return f"Recent affirmations (most recent last):\n{formatted}"


@tool
def get_weather() -> str:
    """
    Get current weather. Only use if the detail specifically serves the message.
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
def send_push_notification(text: str) -> str:
    """
    Send the final affirmation as a push notification. Always call this last.
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


tools = [read_sent_log, get_weather, send_push_notification]


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

llm_force_send = llm.bind_tools(
    tools,
    tool_choice={"type": "function", "function": {"name": "send_push_notification"}},
)


def _notification_was_sent(state: State) -> bool:
    for msg in state["messages"]:
        if not isinstance(msg, AIMessage):
            continue
        if not hasattr(msg, "tool_calls") or not msg.tool_calls:
            continue
        for tc in msg.tool_calls:
            if tc.get("name") == "send_push_notification":
                return True
    return False


def chatbot(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def force_send_node(state: State) -> dict:
    print("⚠️  Agent did not call send_push_notification — forcing send now.")
    forced_msg = llm_force_send.invoke(state["messages"])
    return {"messages": [forced_msg]}


def after_chatbot_router(state: State):
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and getattr(last_msg, "tool_calls", None):
        return "tools"
    if _notification_was_sent(state):
        return END
    return "force_send"


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_node("force_send", force_send_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", after_chatbot_router)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("force_send", "tools")

graph = graph_builder.compile()


# ─────────────────────────────────────────────────────────────────────────────
# Extract affirmation text
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

    log_count = _count_log_entries()
    flavor = get_message_flavor(log_count)
    lang = get_language()

    cycle_pos = log_count % 3
    is_interview = cycle_pos == 2
    flavor_label = flavor['name'] if not is_interview else f"INTERVIEW — {flavor['name']}"

    print(f"[{ctx['now_str']}] {ctx['period'].upper()}")
    print(f"Entry #{log_count} | Cycle pos {cycle_pos}/3 | Flavor: {flavor_label} | Lang: {lang['lang']}")

    result = graph.invoke({
        "messages": [
            SystemMessage(content=build_system_prompt(ctx, flavor)),
            HumanMessage(content="Please generate and send my affirmation now."),
        ]
    })

    affirmation_text = extract_affirmation_text(result)
    if affirmation_text:
        append_log(affirmation_text, ctx)
        print("Done. Affirmation sent and logged.")
    else:
        print("Warning: could not extract affirmation text for logging.")