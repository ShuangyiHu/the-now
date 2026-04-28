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
    MAX_LOG_ENTRIES,
    RECENT_FOR_PROMPT,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LANGUAGE,
    LIFE_SCRIPT_LOVE,
    LIFE_SCRIPT_WORK,
    SCENE_BANK_LOVE,
    SCENE_BANK_WORK,
    ORDER_SIGNALS_LOVE,
    ORDER_SIGNALS_WORK,
    AFFIRMATION_THEMES_LOVE,
    AFFIRMATION_THEMES_WORK,
    PERIOD_ENERGY,
    PERIOD_EMOJI,
    PERIOD_HOURS,
    MESSAGE_FLAVORS,
    LOVE_FLAVOR_INDICES,
    WORK_FLAVOR_INDICES,
    CRAFT_RULES,
    TOOL_INSTRUCTIONS,
)

load_dotenv()

LOG_FILE = Path("sent_log.txt")

# ─────────────────────────────────────────────────────────────────────────────
# Slot index
#
# Maps the current half-hour slot to a deterministic integer 0..25.
# 9:00 → 0, 9:30 → 1, 10:00 → 2, ..., 21:30 → 25
# ─────────────────────────────────────────────────────────────────────────────

def get_slot_index(hour: int, minute: int) -> int:
    half = minute // 30
    return (hour - 9) * 2 + half


# ─────────────────────────────────────────────────────────────────────────────
# Flavor selection — purely time-based, no log counting
#
# Slot category (slot_index % 2):
#   0  →  LOVE
#   1  →  WORK
#
# Flavor within category rotates via (slot_index + day_of_year) % n,
# so the same time slot produces a different flavor on different days.
# ─────────────────────────────────────────────────────────────────────────────

SLOT_CATEGORY_LOVE = 0
SLOT_CATEGORY_WORK = 1


def get_slot_category(slot_index: int) -> int:
    return slot_index % 2


def get_message_flavor(slot_index: int, day_of_year: int) -> tuple[dict, str]:
    """
    Returns (flavor_dict, category_label).
    category_label is one of: "love", "work"
    """
    category = get_slot_category(slot_index)

    if category == SLOT_CATEGORY_LOVE:
        idx = (slot_index + day_of_year) % len(LOVE_FLAVOR_INDICES)
        return MESSAGE_FLAVORS[LOVE_FLAVOR_INDICES[idx]], "love"

    else:  # SLOT_CATEGORY_WORK
        idx = (slot_index + day_of_year) % len(WORK_FLAVOR_INDICES)
        return MESSAGE_FLAVORS[WORK_FLAVOR_INDICES[idx]], "work"


def get_language() -> dict:
    return {"lang": LANGUAGE, "instruction": f"Write entirely in {LANGUAGE}."}


# ─────────────────────────────────────────────────────────────────────────────
# Log helpers
# ─────────────────────────────────────────────────────────────────────────────

def _read_recent_log_entries(n: int = RECENT_FOR_PROMPT) -> list[str]:
    if not LOG_FILE.exists():
        return []
    text = LOG_FILE.read_text(encoding="utf-8")
    # Split on separator lines so multi-line entries are treated as one unit
    entries = [e.strip() for e in text.split("─────────────────────────────────────────") if e.strip()]
    return entries[-n:]


def _count_log_entries() -> int:
    """Count entries by separator — multi-line entries count as one."""
    if not LOG_FILE.exists():
        return 0
    text = LOG_FILE.read_text(encoding="utf-8")
    return len([e for e in text.split("─────────────────────────────────────────") if e.strip()])


def append_log(affirmation_text: str, ctx: dict) -> None:
    pst = pytz.timezone("America/Los_Angeles")
    timestamp = datetime.now(pst).strftime("%Y-%m-%d %H:%M PST")
    new_entry = f"[{timestamp} | {ctx['period']} | {ctx['slot_label']}] {affirmation_text.strip()}"

    existing = []
    if LOG_FILE.exists():
        text = LOG_FILE.read_text(encoding="utf-8")
        existing = [e.strip() for e in text.split("─────────────────────────────────────────") if e.strip()]

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
    day_of_year = now.timetuple().tm_yday

    for period, (start, end) in PERIOD_HOURS.items():
        if start <= hour < end:
            slot_index = get_slot_index(hour, now.minute)
            return {
                "period": period,
                "emoji": PERIOD_EMOJI[period],
                "energy": PERIOD_ENERGY[period],
                "slot_label": f"{date_str}-{period}-slot{hour * 2 + slot}",
                "slot_index": slot_index,
                "day_of_year": day_of_year,
                "now_str": now.strftime("%I:%M %p PST"),
            }
    return None


# ─────────────────────────────────────────────────────────────────────────────
# System prompt builder — two content pools: love / work
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict, flavor: dict, category: str) -> str:
    lang = get_language()

    if category == "love":
        life_script        = LIFE_SCRIPT_LOVE
        scene_bank         = SCENE_BANK_LOVE
        order_signals      = ORDER_SIGNALS_LOVE
        affirmation_themes = AFFIRMATION_THEMES_LOVE
        slot_header        = "LOVE SLOT — write about romantic connection with her SP, intimate gestures, and life milestones (proposal/wedding/family). Always include at least one specific physical/tender gesture."

    else:  # work
        life_script        = LIFE_SCRIPT_WORK
        scene_bank         = SCENE_BANK_WORK
        order_signals      = ORDER_SIGNALS_WORK
        affirmation_themes = AFFIRMATION_THEMES_WORK
        slot_header        = "WORK SLOT — write about her dream job: aligned, light, generously paid, deeply respected. She is always the first choice. No grind, no struggle, no desperation."

    scene_list         = "\n".join(f"- {s}" for s in scene_bank)
    order_list         = "\n".join(f"- {s}" for s in order_signals)
    affirmation_list   = "\n".join(f"- {s}" for s in affirmation_themes)

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
• Avoids repeating the same scenes, milestones, or gestures

For love messages: vary the milestone (proposal / wedding / pregnancy / everyday)
and vary the intimate gesture (kiss / hand / forehead / embrace / glance).
For work messages: vary the angle (offer / pay / recognition / ease / opportunity).

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


tools = [read_sent_log, send_push_notification]


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

    slot_index  = ctx["slot_index"]
    day_of_year = ctx["day_of_year"]
    flavor, category = get_message_flavor(slot_index, day_of_year)
    lang = get_language()

    print(f"[{ctx['now_str']}] {ctx['period'].upper()}")
    print(f"slot_index={slot_index} | day_of_year={day_of_year} | category={category.upper()} | flavor={flavor['name']} | lang={lang['lang']}")

    result = graph.invoke({
        "messages": [
            SystemMessage(content=build_system_prompt(ctx, flavor, category)),
            HumanMessage(content="Please generate and send my affirmation now."),
        ]
    })

    affirmation_text = extract_affirmation_text(result)
    if affirmation_text:
        append_log(affirmation_text, ctx)
        print("Done. Affirmation sent and logged.")
    else:
        print("Warning: could not extract affirmation text for logging.")
