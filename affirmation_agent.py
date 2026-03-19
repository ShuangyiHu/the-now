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
    LIFE_SCRIPT,
    SCENE_BANK,
    ORDER_SIGNALS,
    AFFIRMATION_THEMES,
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
# Helpers: flavor selection
#
# Rotation pattern (every 3 messages):
#   position 0 → general flavor
#   position 1 → general flavor
#   position 2 → interview flavor
#
# FIX: general_index now tracks only the general-slot count independently,
# so it properly rotates through all 5 general flavors without interference
# from the overall log_entry_count parity.
# ─────────────────────────────────────────────────────────────────────────────

def get_message_flavor(log_entry_count: int) -> dict:
    """
    Returns the flavor dict for the current message.

    Every 3rd message (cycle_position == 2) → interview flavor.
    The two interview flavors alternate each interview slot.
    General slots (positions 0 and 1) → rotate through all GENERAL_FLAVOR_INDICES.

    FIX: general_index is derived from the count of general messages sent so far
    (not from log_entry_count directly), ensuring true rotation through all 5 general
    flavors independent of whether the current slot is position 0 or 1 in the cycle.
    """
    cycle_position = log_entry_count % 3

    if cycle_position == 2:
        # Interview slot — alternate between the two interview flavors
        interview_slot_number = log_entry_count // 3
        interview_index = interview_slot_number % len(INTERVIEW_FLAVOR_INDICES)
        return MESSAGE_FLAVORS[INTERVIEW_FLAVOR_INDICES[interview_index]]
    else:
        # General slot — count how many general messages have been sent so far
        # In every group of 3: positions 0 and 1 are general → 2 general per 3 total
        full_cycles = log_entry_count // 3          # completed full cycles of 3
        general_count = full_cycles * 2 + cycle_position  # general msgs sent so far
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
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict, flavor: dict) -> str:
    lang = get_language()
    directive = flavor["directive"]
    flavor_id = flavor["id"]

    # Hard block: tell LLM explicitly whether interview content is allowed
    is_interview_flavor = flavor_id in ("tiktok_interview", "tiktok_cheerleader")
    if is_interview_flavor:
        interview_block = ""  # interview flavors: no restriction needed
        topic_rule_header = "INTERVIEW MESSAGE — write about TikTok USDS interview only."
    else:
        interview_block = """
⚠️  INTERVIEW CONTENT BLOCK — THIS MESSAGE IS NOT AN INTERVIEW MESSAGE ⚠️

The current flavor is a GENERAL flavor. You MUST NOT write about:
  - TikTok USDS interview, coding round, offer letter
  - Any interview preparation or result
  - Badge-scanning into TikTok USDS for the first time
  - Recruiter emails related to TikTok USDS

If you feel drawn to write about the interview, STOP and pick a completely
different scene from LOVE, TRAVEL, FRIENDS, or INNER STATE instead.
"""
        topic_rule_header = "GENERAL MESSAGE — interview content is BLOCKED for this slot."

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
THIS MESSAGE'S ASSIGNED FLAVOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{topic_rule_header}

Flavor: {flavor['name'].upper()}

{directive}

{interview_block}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIFE SCRIPT (background reality)
Use as inspiration — do NOT quote verbatim.
For general flavors, focus on areas 1–5 below (not area 0).
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
ANTI-REPETITION RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You must call read_sent_log first.

Carefully check the last affirmations and ensure the new message:

• Uses different opening words
• Uses different imagery
• Uses a different emotional tone
• Avoids repeating the same scenes

For interview messages: check which STYLE (A/B/C/D/E) appeared most recently
and pick a different one.

If your draft feels similar to a recent message, rewrite it with a different scene.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOPIC DIVERSITY RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The life script contains SIX areas of life:
  0. TIKTOK USDS INTERVIEW — ONLY used when the flavor is an interview flavor
  1. CAREER — office, coding, engineering, badge, pull requests (non-TikTok)
  2. LOVE — reconnecting with him, walks through Fremont, quiet evenings together
  3. TRAVEL — flight to China, family reunion, summer train trip with friends
  4. FRIENDS — Gas Works Park, spontaneous dinners, laughter, social richness
  5. INNER STATE — calm, grounded, expansive, no longer chasing — just living

For general flavors: you must pick from areas 1–5 only.
Look at recent messages and pick the area least recently covered.

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