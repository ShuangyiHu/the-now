# affirmation_agent.py
# A LangGraph-based agent that sends personalized affirmations via Pushover,
# each accompanied by a DALL-E 3 generated image matching the mood and time of day.

from typing import Annotated, TypedDict
from pathlib import Path
from datetime import datetime
import base64

import pytz
import requests
import os

from dotenv import load_dotenv
from openai import OpenAI
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

# Maximum number of entries to keep in the log file to prevent unbounded growth
MAX_LOG_ENTRIES = 50

# Number of recent entries to inject into the prompt for deduplication
RECENT_FOR_PROMPT = 10

# Shared OpenAI client used for both chat and image generation
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─────────────────────────────────────────────────────────────────────────────
# Personal context — update this block when your situation changes
# ─────────────────────────────────────────────────────────────────────────────

PERSONAL_CONTEXT = """
PERSONAL SITUATION (weave this naturally into every message — do not state it bluntly):
- The user is actively job hunting and feeling uncertain about their career path
- The user recently went through a breakup and is emotionally recovering
- Both things are happening at the same time, creating an overall sense of being at a low point
- Key themes to reinforce across all time periods:
    * Pain is temporary — this difficult season will pass
    * Living fully in the present moment is the antidote to rumination
    * Do not let imagined versions of the past ("what could have been") or
      the future ("what if things never get better") hijack the present
    * Self-worth is not determined by job titles or relationship status
- Tone guidance: be warm and real — acknowledge difficulty briefly, then
  pivot toward strength, presence, and quiet hope. Never use toxic positivity.

MOVEMENT REMINDER:
- Every message must include a brief, caring nudge to get up, stretch, or move
- Keep it to one sentence, woven naturally into the message or added at the end
- Make it feel like advice from a friend, not a fitness coach
- Vary the wording every time (e.g., do not always say "take a stretch break")
"""


# ─────────────────────────────────────────────────────────────────────────────
# Log management
# ─────────────────────────────────────────────────────────────────────────────

def read_recent_logs(n: int = RECENT_FOR_PROMPT) -> list[str]:
    """
    Read the most recent n entries from the log file.
    Each entry format: [2026-02-22 09:00 PST | morning] 🌅 message text...
    Returns an empty list if the log file does not exist yet.
    """
    if not LOG_FILE.exists():
        return []

    raw = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    entries = [line for line in raw if line.strip() and not line.startswith("─")]
    return entries[-n:]


def append_log(affirmation_text: str, ctx: dict) -> None:
    """
    Append a new affirmation entry to the log file.
    Enforces MAX_LOG_ENTRIES to keep the file from growing indefinitely.
    """
    pst = pytz.timezone("America/Los_Angeles")
    timestamp = datetime.now(pst).strftime("%Y-%m-%d %H:%M PST")
    new_entry = f"[{timestamp} | {ctx['period']}] {affirmation_text.strip()}"

    if LOG_FILE.exists():
        existing = [
            line for line in LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
            if line.strip() and not line.startswith("─")
        ]
    else:
        existing = []

    existing.append(new_entry)
    if len(existing) > MAX_LOG_ENTRIES:
        existing = existing[-MAX_LOG_ENTRIES:]

    separator = "\n─────────────────────────────────────────\n"
    LOG_FILE.write_text(separator.join(existing) + "\n", encoding="utf-8")
    print(f"Log updated ({len(existing)} total entries): {new_entry[:80]}...")


# ─────────────────────────────────────────────────────────────────────────────
# Time context — determines the mood and angle of the affirmation
# ─────────────────────────────────────────────────────────────────────────────

def get_time_context() -> dict | None:
    """
    Return a dictionary describing the current PST time period.
    Returns None if outside the active window (9AM-10PM PST/PDT).
    Slot label is unique per 30-minute window per day, used as a deduplication seed.
    """
    pst = pytz.timezone("America/Los_Angeles")
    now = datetime.now(pst)
    hour = now.hour
    slot = now.minute // 30
    date_str = now.strftime("%Y-%m-%d")

    if 9 <= hour < 12:
        slot_label = f"{date_str}-morning-slot{hour * 2 + slot}"
        return {
            "period": "morning",
            "emoji": "🌅",
            "slot_label": slot_label,
            "tone": "warm, energizing, gently hopeful",
            "image_style": (
                "soft golden morning light, warm sunrise colors, "
                "gentle optimism, watercolor or impressionist style, "
                "nature scenes like dew on leaves or a quiet window with sunlight"
            ),
            "context": """It is morning (9 AM - 12 PM PST).
The user may struggle to find motivation to start the day, weighed down by the
emotional heaviness of job searching and processing a breakup.

Your affirmation should:
- Make getting up feel genuinely worthwhile
- Remind them that each morning is a real fresh slate, not just a cliche
- Ground them in THIS specific morning, not yesterday's rejection or tomorrow's worry
- Feel like a trusted friend saying "today is worth showing up for"

Angle on personal situation:
- Job hunt: one more day of effort compounds quietly, the right opportunity
  is built toward, not stumbled upon randomly
- Breakup: mornings are often the hardest emotionally; validate this gently,
  then redirect toward the freedom and possibility of a day that belongs only to them""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 12 <= hour < 19:
        slot_label = f"{date_str}-afternoon-slot{hour * 2 + slot}"
        return {
            "period": "afternoon",
            "emoji": "☀️",
            "slot_label": slot_label,
            "tone": "re-energizing, focused, steady and grounded",
            "image_style": (
                "bright midday light, vivid but grounded colors, "
                "energy and focus, bold painterly style, "
                "scenes of quiet determination like a lone tree in full sun "
                "or a clear open road or a person walking forward"
            ),
            "context": """It is afternoon (12 PM - 6 PM PST).
The user has been working through job applications or studying all morning
and is likely hitting a mental and emotional wall, the classic afternoon slump.

Your affirmation should:
- Acknowledge that the middle of any hard stretch is the toughest part
- Reignite their sense of self-worth that is independent of external outcomes
- Bring them back to the present hour, this effort, this moment, this version
  of themselves that keeps going despite everything
- Be grounded and real, never artificially cheerful

Angle on personal situation:
- Job hunt: progress is not always visible day-to-day, but it is real and cumulative.
  Remind them that persistence through the afternoon of hard seasons is what matters.
- Breakup: afternoons can bring unexpected waves of missing someone; redirect
  toward the quiet strength they are actively building right now""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    elif 18 <= hour < 23:
        slot_label = f"{date_str}-evening-slot{hour * 2 + slot}"
        return {
            "period": "evening",
            "emoji": "🌙",
            "slot_label": slot_label,
            "tone": "calming, compassionate, peaceful",
            "image_style": (
                "soft twilight or moonlit atmosphere, cool blues and purples, "
                "gentle warm candlelight accents, peaceful and serene, "
                "impressionist or dreamy digital art style, "
                "scenes like a quiet starry sky, a candle by a window, "
                "or calm still water reflecting moonlight"
            ),
            "context": """It is evening (6 PM - 9 PM PST).
The user is winding down. After a full day of effort and emotional weight,
they need permission to truly rest, not to solve anything else tonight.

Your affirmation should:
- Help them gently set down the weight of the day
- Remind them that showing up today was enough, it always counts
- Encourage self-compassion: they are far more than their job title or relationship status
- Prime them for restful sleep, not anxious rumination about what comes next
- Make solitude feel like reclaimed space, not loneliness

Angle on personal situation:
- Job hunt: overnight, momentum continues even when they rest. Let go of today's outcomes.
- Breakup: evenings can feel the loneliest; remind them that solitude and loneliness
  are genuinely different, this quiet time is theirs to reclaim and own""",
            "now_str": now.strftime("%I:%M %p PST"),
        }

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Language rotation — alternates English and Chinese per slot
# ─────────────────────────────────────────────────────────────────────────────

def get_language(slot_label: str) -> dict:
    """
    Even slot numbers -> English, odd slot numbers -> Chinese.
    Ensures strict alternation across consecutive 30-minute windows.
    """
    slot_num = int(slot_label.split("slot")[-1])

    if slot_num % 2 == 0:
        return {
            "lang": "English",
            "instruction": "Write the entire affirmation in English.",
            "movement_hint": (
                "End with one gentle, varied sentence encouraging the user "
                "to get up and move their body, written in English."
            ),
        }
    else:
        return {
            "lang": "Chinese",
            "instruction": (
                "用中文写作。语言要自然流畅，像一个真实的朋友说话，"
                "而不是机器翻译或正式书面语。"
            ),
            "movement_hint": (
                "最后用一句话提醒用户起来活动一下身体。"
                "每次措辞都要不同，不要总用同样的句式。"
            ),
        }


# ─────────────────────────────────────────────────────────────────────────────
# Deduplication — inject recent log entries into the prompt
# ─────────────────────────────────────────────────────────────────────────────

def build_no_repeat_section() -> str:
    """
    Format recent log entries as a deduplication constraint for the system prompt.
    Returns an empty string on the first run when no log exists yet.
    """
    recent = read_recent_logs(RECENT_FOR_PROMPT)
    if not recent:
        return ""

    formatted = "\n".join(f"  - {entry}" for entry in recent)
    return f"""
RECENT MESSAGES - DO NOT REPEAT any of the following:
{formatted}

Your new affirmation must differ from ALL of the above in:
- Opening words and sentence structure
- The core image, metaphor, or angle used
- The specific take on job searching or emotional recovery
- The wording of the movement reminder
"""


# ─────────────────────────────────────────────────────────────────────────────
# System prompt builder
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(ctx: dict) -> str:
    """
    Assemble the full system prompt from time period, language,
    personal context, and deduplication history.
    """
    lang = get_language(ctx["slot_label"])
    no_repeat_section = build_no_repeat_section()

    return f"""You are a deeply caring personal wellness companion — warm, wise, and real.
You send short, powerful affirmations that meet the user exactly where they are,
without being preachy or using hollow positivity.

CURRENT TIME : {ctx['now_str']}
PERIOD       : {ctx['emoji']} {ctx['period'].upper()}
SLOT ID      : {ctx['slot_label']}
               (Use this as a mental uniqueness seed — each slot is a different message)

LANGUAGE THIS ROUND: {lang['lang']}
{lang['instruction']}

TONE: {ctx['tone']}

TIME-SPECIFIC CONTEXT AND ANGLE:
{ctx['context']}

{PERSONAL_CONTEXT}

{no_repeat_section}

FORMATTING RULES — follow every rule exactly:
1.  Begin the message with the {ctx['emoji']} emoji.
2.  Main affirmation body: 2-4 sentences, under 90 words total.
3.  Weave present-moment awareness in naturally — the antidote to pain is HERE, NOW.
4.  {lang['movement_hint']}
5.  BANNED words and phrases (too generic or overused):
      English: "journey", "embrace", "thrive", "hustle", "grind",
               "amazing", "awesome", "you've got this"
      Chinese: "你值得更好的", "加油", "相信自己", "不要放弃"
6.  Do NOT open with "I am" (English) or "我是" (Chinese).
7.  Do NOT ask the user any questions.
8.  After writing the affirmation, IMMEDIATELY call send_push_notification
    to deliver it. Do not wait for confirmation.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Image generation — DALL-E 3
# ─────────────────────────────────────────────────────────────────────────────

def build_image_prompt(affirmation_text: str, ctx: dict) -> str:
    """
    Build a DALL-E 3 prompt that visually reflects both the affirmation content
    and the mood of the current time period.

    The prompt deliberately avoids asking DALL-E to render any text, since
    DALL-E 3 handles embedded text poorly. The image is purely visual.
    """
    return (
        f"Create a beautiful, emotionally resonant illustration that captures "
        f"the feeling of this affirmation: '{affirmation_text}'. "
        f"Visual style: {ctx['image_style']}. "
        f"The image should feel {ctx['tone']}. "
        f"No text, words, letters, or numbers anywhere in the image. "
        f"No people's faces — use nature, light, abstract forms, or atmospheric scenes. "
        f"Aspect ratio: square. High quality, deeply atmospheric."
    )


def generate_image(affirmation_text: str, ctx: dict) -> bytes | None:
    """
    Call the DALL-E 3 API to generate an image for the affirmation.
    Returns raw PNG bytes, or None if generation fails.
    Images are returned as base64 (response_format='b64_json') to avoid
    a second HTTP request to download from a temporary URL.
    """
    image_prompt = build_image_prompt(affirmation_text, ctx)
    print(f"Generating image with prompt: {image_prompt[:100]}...")

    try:
        response = openai_client.images.generate(
            model="dall-e-3", 
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            n=1,
        )
        image_b64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_b64)
        print(f"Image generated successfully ({len(image_bytes) // 1024} KB).")
        return image_bytes

    except Exception as e:
        # Image generation failure is non-fatal — the text notification was already sent
        print(f"Warning: image generation failed: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Pushover notification tool (text only — called by the LangGraph agent)
# ─────────────────────────────────────────────────────────────────────────────

@tool
def send_push_notification(text: str) -> str:
    """Send an affirmation as a push notification to the user's phone."""
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
            "title": "Your Affirmation ✨",
        },
    )
    return f"Text notification sent (HTTP {response.status_code})"


tools = [send_push_notification]


# ─────────────────────────────────────────────────────────────────────────────
# Pushover image send — called directly after image generation (not via agent)
# ─────────────────────────────────────────────────────────────────────────────

def send_push_with_image(affirmation_text: str, image_bytes: bytes) -> None:
    """
    Send a second Pushover notification containing the generated image.
    Pushover supports JPEG/PNG/GIF attachments up to 2.5 MB.
    Sent separately from the text notification so the text always arrives
    even if image generation is slow or fails.
    """
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": " ",          # Pushover requires a non-empty message field
            "title": "Your Affirmation Image 🎨",
        },
        files={
            # Tuple format: (filename, file_bytes, mime_type)
            "attachment": ("affirmation.png", image_bytes, "image/png"),
        },
    )
    print(f"Image notification sent (HTTP {response.status_code}).")


# ─────────────────────────────────────────────────────────────────────────────
# LangGraph setup
# ─────────────────────────────────────────────────────────────────────────────

class State(TypedDict):
    messages: Annotated[list, add_messages]


# temperature=1.0 maximizes variety across repeated calls with similar prompts
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    """Core agent node: call the LLM with the current message history."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", END)  # Exit after tool call — no looping

graph = graph_builder.compile()


# ─────────────────────────────────────────────────────────────────────────────
# Text extraction helper
# ─────────────────────────────────────────────────────────────────────────────

def extract_affirmation_text(result: dict) -> str:
    """
    Extract the affirmation text from the graph result using two strategies:

    Strategy 1 (preferred): Read the 'text' argument passed to the
    send_push_notification tool call. This is the most reliable source because
    the LLM often skips putting text in AIMessage.content and goes straight
    to calling the tool.

    Strategy 2 (fallback): Look for plain text content in any AIMessage,
    which covers cases where the LLM outputs text before calling the tool.
    """
    import json

    # Strategy 1: extract from tool_calls arguments in AIMessage
    for msg in result["messages"]:
        if not isinstance(msg, AIMessage):
            continue
        if not hasattr(msg, "tool_calls") or not msg.tool_calls:
            continue
        for tc in msg.tool_calls:
            if tc.get("name") == "send_push_notification":
                args = tc.get("args", {})
                text = args.get("text", "").strip()
                if text:
                    print("Extracted affirmation text from tool_call args.")
                    return text

    # Strategy 2: fallback to plain text content in AIMessage
    for msg in reversed(result["messages"]):
        if not isinstance(msg, AIMessage):
            continue
        if isinstance(msg.content, str) and msg.content.strip():
            return msg.content.strip()
        if isinstance(msg.content, list):
            text_parts = [
                block["text"]
                for block in msg.content
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            if text_parts:
                return " ".join(text_parts).strip()

    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ctx = get_time_context()

    if ctx is None:
        # Safety net for DST edge cases — the cron schedule already filters time windows
        print("Outside active hours (9 AM - 9 PM PST). Nothing to send. Exiting.")
        exit(0)

    print(f"[{ctx['now_str']}] Generating {ctx['period']} affirmation...")

    # Step 1: LangGraph generates the affirmation text and sends the text notification
    result = graph.invoke(
        {
            "messages": [
                SystemMessage(content=build_system_prompt(ctx)),
                HumanMessage(content="Please generate and send my affirmation now."),
            ]
        }
    )

    # Step 2: Extract the text for logging and image generation
    affirmation_text = extract_affirmation_text(result)

    if affirmation_text:
        # Step 3: Log the affirmation for future deduplication
        append_log(affirmation_text, ctx)

        # Step 4: Generate the image with DALL-E 3
        image_bytes = generate_image(affirmation_text, ctx)

        # Step 5: Send the image as a separate Pushover notification
        if image_bytes:
            send_push_with_image(affirmation_text, image_bytes)
            print("Done. Text + image both sent and logged.")
        else:
            print("Done. Text sent and logged. Image skipped (generation failed).")
    else:
        print("Warning: affirmation text could not be extracted for logging.")
