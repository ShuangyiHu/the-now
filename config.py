# config.py
# ─────────────────────────────────────────────────────────────────────────────
# All customizable content lives here.
# affirmation_agent.py does not need to be touched.
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# Basic settings
# ─────────────────────────────────────────────────────────────────────────────

WEATHER_LOCATION  = "Seattle"   # City for weather lookup
MAX_LOG_ENTRIES   = 50          # Max entries kept in sent_log.txt
RECENT_FOR_PROMPT = 10          # How many recent messages to show the LLM
LLM_TEMPERATURE   = 1.3         # Higher = more creative. Recommended: 1.1–1.4
LLM_TOP_P         = 0.95        # Works with temperature to control variety

# Language for all messages. Change to "Chinese" to switch back.
LANGUAGE = "English"


# ─────────────────────────────────────────────────────────────────────────────
# Life Script
# 这是你想要的生活，写成"已经是真的"。
# LLM 会从这里取具体细节写进消息，不会逐字照抄。
# 想改剧本？直接改这里，agent 自动更新。
# ─────────────────────────────────────────────────────────────────────────────

LIFE_SCRIPT = """
DESIRED REALITY (already unfolding — treat as true, use as creative fuel):

WORK & CAREER:
- Software Engineer at a company in Seattle, $150K, OPT sponsorship secured
- Walking along South Lake Union to the office — passing Amazon/Google engineers as a peer, not an outsider
- First PR merged. Contributing to system design discussions. Owning a backend service module.
- Manager called her async job queue design "clean and scalable" in a team meeting
- She presents, she contributes, she belongs

HOME & DAILY LIFE:
- Capitol Hill apartment, Seattle summer light coming through the windows in the morning
- Weekends: Gas Works Park picnics, time to work out, read, walk by the water
- Income that allows comfortable, calm Seattle living — not scrambling, just living

LOVE:
- She and him have reconnected after time apart — both grew during the separation
- Walking through Fremont together at night; he said "I can see you've become stronger"
- Learning to express emotions gently, not as weapons — being loved for exactly who she is
- Taking it slow, but more deeply present with each other

INNER STATE:
- No longer anxious about the future — she has become the person she was trying to be
- The transformation already happened; she's living in the evidence of it
- Grounded, creative, free — a life that feels like hers
"""


# ─────────────────────────────────────────────────────────────────────────────
# 时段能量设定
# 每个时段给 LLM 一个"频率"，不描述困境，只设定这一刻的状态。
# ─────────────────────────────────────────────────────────────────────────────

PERIOD_ENERGY = {
    "morning": "energizing, grounding into the day that is already hers",
    "afternoon": "re-centering, keeping the frequency high",
    "evening": "settling, grateful, trusting that everything continues to arrange itself while she rests",
}

PERIOD_EMOJI = {
    "morning": "🌅",
    "afternoon": "☀️",
    "evening": "🌙",
}

# 时间窗口：(起始小时, 结束小时，不含)
PERIOD_HOURS = {
    "morning":   (9, 13),
    "afternoon": (13, 19),
    "evening":   (19, 23),
}


# ─────────────────────────────────────────────────────────────────────────────
# Message Flavors
# Rotates by slot number mod len(MESSAGE_FLAVORS).
# Add, remove, or edit flavors here — the agent adapts automatically.
# ─────────────────────────────────────────────────────────────────────────────

MESSAGE_FLAVORS = [
    {
        "id": "order_placed",
        "name": "Order Placed with the Universe",
        "directive": """
Write as if an order has already been placed and is being fulfilled RIGHT NOW.
The universe received the request. Delivery is in progress. No question marks, no conditions.
Use language like: already done / already mine / already on the way / the universe has this.
Tone: calm certainty, not excited hope. Present or present-continuous tense.
Example energy (do NOT copy): "The offer letter is already written. I'm just waiting for the date."
Draw from the life script — one specific detail (a number, a place, a moment) makes it feel real.
Two sentences max.
""",
    },
    {
        "id": "living_in_the_end",
        "name": "Living in the End",
        "directive": """
Neville Goddard's core technique: she is already there. Not going there — already arrived.
Write a micro-scene: one moment from the desired life, described as happening now or as a recent memory.
Use the life script as source material. Pick ONE moment: the walk to work, the team meeting,
the Fremont walk at night, the Capitol Hill morning light.
Make it feel like a memory she's already made, not a dream she's reaching for.
2-3 sentences. Present tense or recent-past tense (recounting something that just happened).
""",
    },
    {
        "id": "i_am_magnetic",
        "name": "I Am Magnetic",
        "directive": """
Classic Law of Attraction "I AM" declarations — present tense, declarative, no hedging.
These are STATEMENTS of fact about who she is RIGHT NOW, not who she hopes to become.
Make them specific using the life script:
  - magnetic to the right engineering teams
  - worthy of $150K and OPT sponsorship
  - the kind of person who walks into a room and belongs
  - someone who loves and is loved well
Write 2-3 "I am" statements woven into 1-2 sentences. Powerful, not preachy.
""",
    },
    {
        "id": "worthiness_as_fact",
        "name": "Worthiness Is a Given",
        "directive": """
Worthiness without conditions. She doesn't earn it. She was born with it.
Not "you've worked so hard therefore you deserve it" — that makes worth conditional on effort.
Go for: she qualifies simply by existing. The good things are looking for her as much as she's looking for them.
The job is looking for its person. The love is looking for where it belongs.
This should feel like stating an obvious, settled truth — not motivating, not comforting. Just: true.
Under 40 words. One clean idea.
""",
    },
    {
        "id": "visualization_flash",
        "name": "Visualization Flash",
        "directive": """
One sharp, sensory flash from the desired life. Specific, not abstract.
Pick one of these and make it vivid:
  - Walking to work in South Lake Union on a June morning, lake light, other engineers
  - The quiet satisfaction of pushing code to production for the first time
  - A Saturday at Gas Works Park — not hustling, just being
  - The Fremont walk at dusk, the specific quality of light on water
  - Waking up in the Capitol Hill apartment knowing exactly where you belong
Make the reader FEEL it for 3 seconds. Like a preview from their own future.
2 sentences. Sensory. Grounded.
""",
    },
    {
        "id": "gratitude_as_if",
        "name": "Gratitude From the Future",
        "directive": """
Write a message of gratitude as if the desired life has already fully arrived.
Not "I will be grateful when..." but "I am grateful for..."
The gratitude should feel warm, specific, already earned. Like a thank-you note to the universe.
Draw from the life script: the job, the stability, the rekindled relationship, the morning light.
Example energy: "Thank you for the offer that came at exactly the right time."
1-3 sentences. Specific. Warm. Present tense.
""",
    },
    {
        "id": "already_her",
        "name": "She Already Is",
        "directive": """
The transformation already happened. She is not becoming — she already is.
The version of her that has the job, the confidence, the love — that person exists NOW.
Not "you'll get there" — "you're already there and the external world is catching up."
Draw from the life script: walking among SLU engineers as a peer, presenting in the team meeting,
being told "I can see you've become stronger."
1-2 sentences. Quiet certainty. Present tense.
""",
    },
    {
        "id": "permission_to_receive",
        "name": "Permission to Receive",
        "directive": """
A lot of what blocks manifestation is not believing you're allowed to have it.
This message gives explicit permission: it's okay to want this. It's okay to receive it.
The good things are not too much to ask for. She is not asking for more than she deserves.
The $150K job. The love. The stable, creative, comfortable life. These are not too much.
They were always hers. She's just remembering that.
Write it like an unlocking, not a pep talk. Under 40 words. Clear and freeing.
""",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Craft rules
# Controls output style. Rarely needs changing.
# ─────────────────────────────────────────────────────────────────────────────

CRAFT_RULES = """
• Start with the period emoji, then the message body.
• 1–3 sentences. Under 50 words. Shorter usually hits harder.
• Present tense for manifestation/I AM types. Sensory present or recent-past for visualization.
• ONE idea per message. Never cram multiple angles in.
• MOVEMENT NUDGE: skip unless the flavor is grounding/settling AND it arises naturally.
  Half a sentence max, casual, skip if even slightly forced.
• DO NOT: explain the situation, name the hardship, or pivot from pain to hope.
  Just arrive at the truth directly.
• DO NOT open with "I am" or "我是" as the literal first words (emoji comes first; fine after).
• DO NOT use: "journey", "embrace", "thrive", "加油", "相信自己", "不要放弃",
  "remember that", "it's okay to feel", "you've got this", "pain is temporary".
• SURPRISE OVER SAFETY: if your draft sounds like something you've heard before — rewrite it.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tool instructions (passed to the LLM)
# ─────────────────────────────────────────────────────────────────────────────

TOOL_INSTRUCTIONS = """
Use tools in this order:

1. read_sent_log
   Scan the last 10 messages carefully.
   Your message must differ from all recent ones in: opening words, central image,
   emotional register, and sentence rhythm.
   Note which flavors were used recently — yours must feel different.
   If your draft resembles anything in the log — scrap it and approach from a new angle.

2. get_weather
   Only weave in if it adds a SPECIFIC and unexpected detail relevant to this flavor.
   Skip entirely if it's generic or doesn't serve the message.

3. search_quote
   Theme: choose a word tightly linked to this flavor's core idea.
   e.g. for "order placed" → "receiving" / for "living in the end" → "already" / for "worthiness" → "deserve"
   Only include the quote if it's under 15 words AND feels genuinely surprising.
   Cut entirely if it sounds like something on a motivational poster.

4. send_push_notification
   Write and send the final message.
"""
