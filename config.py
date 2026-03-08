# config.py
# ─────────────────────────────────────────────────────────────
# Affirmation Agent Configuration (V3)
# Fixes: lowered temperature, balanced life script across 5 areas
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# Basic settings
# ─────────────────────────────────────────────────────────────

WEATHER_LOCATION = "Seattle"
MAX_LOG_ENTRIES = 80
RECENT_FOR_PROMPT = 12

# FIX: Lowered from 1.35 to 0.9 — prevents agent from skipping tool calls
LLM_TEMPERATURE = 0.9
LLM_TOP_P = 0.95

LANGUAGE = "English"


# ─────────────────────────────────────────────────────────────
# Scene Bank
# Balanced across all 5 life areas: career, love, travel, friends, inner state
# ─────────────────────────────────────────────────────────────

SCENE_BANK = [

    # CAREER
    "badge scanning at the office door in South Lake Union",
    "pushing code and seeing the green PR checkmark",
    "Slack notification that a pull request was merged",
    "manager praising the async job queue design in a meeting",
    "coffee at a Lake Union café before morning standup",
    "walking beside Lake Union on a bright June morning",
    "first paycheck notification hitting her bank account",

    # LOVE
    "late night walk through Fremont after dinner",
    "him smiling when she finally wins a round of the game",
    "playing games with him and his friends for the first time",
    "quiet evening at home, his voice low and warm",
    "him saying 'I can see you've become stronger' on a Fremont walk",
    "a slow Sunday morning together, neither of them rushing anywhere",

    # TRAVEL
    "boarding the flight home after receiving the job offer",
    "family welcoming her at the airport in China",
    "giving gifts to relatives who are proud of her",
    "meeting Shenzhen friends again after years apart",
    "summer train ride across China with friends",
    "standing on a mountain viewpoint during a China trip",
    "packing suitcases with gifts for family",
    "FaceTiming parents and showing them the Seattle apartment",

    # FRIENDS
    "Gas Works Park picnic with friends on a warm afternoon",
    "laughing with friends during a spontaneous Seattle dinner",
    "sitting outside with friends as Seattle summer light fades",
    "a group photo taken somewhere beautiful during summer",
    "catching up with old Shenzhen friends over food and laughter",

    # INNER STATE
    "quiet morning light filling the Capitol Hill apartment",
    "reading near the window while Seattle sunlight fills the room",
    "waking up and feeling no urgency — just calm and fullness",
    "a moment of stillness where everything feels right",
    "looking around and realizing: this is the life",

]


# ─────────────────────────────────────────────────────────────
# Universe Order Signals
# ─────────────────────────────────────────────────────────────

ORDER_SIGNALS = [

    "the offer letter is already written",
    "the recruiter has already drafted the email",
    "HR is already preparing the contract",
    "the hiring manager already expects her on the team",
    "her badge is already printed",
    "her desk already exists in the office",
    "her first project is already waiting",
    "the salary number is already decided",
    "the team already has a seat for her",

]


# ─────────────────────────────────────────────────────────────
# Affirmation Themes
# ─────────────────────────────────────────────────────────────

AFFIRMATION_THEMES = [

    # Career
    "magnetic to the right engineering teams",
    "naturally belonging among talented engineers",
    "worthy of $150K+ opportunities with sponsorship",
    "calmly confident in technical conversations",
    "someone whose ideas land in design discussions",

    # Love
    "loved deeply and uniquely",
    "someone whose warmth is remembered and returned",
    "someone whose love story is quietly unfolding",

    # Social
    "respected for both intelligence and warmth",
    "someone who creates meaningful friendships",

    # Life
    "someone whose life is expanding beautifully",
    "someone who has stopped chasing and started receiving",

]


# ─────────────────────────────────────────────────────────────
# Life Script
# FIX: Rebalanced — each of the 5 areas gets roughly equal weight
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT = """
DESIRED REALITY — five equal areas, all already unfolding

─────────────────────────
1. CAREER
─────────────────────────

Before June, she receives a Software Engineer / AI Engineer offer in Seattle.
Base salary above $150K. OPT sponsorship included.

The email arrives on a quiet weekday morning.
She opens it in her Capitol Hill apartment while sunlight fills the room.

She badge-scans into the South Lake Union office for the first time.
Her pull requests merge. Her manager calls her design "clean and scalable."
She owns a backend service module. Her ideas shape the architecture.
She belongs here, without question.

─────────────────────────
2. LOVE
─────────────────────────

Over time, her ex-boyfriend remembers what made her irreplaceable —
her humor, warmth, intelligence, and emotional depth.

They start talking again. Casual dinners become longer conversations.
One evening walking through Fremont, he says quietly:
"I can see you've become stronger."

They reconnect slowly but deeply.
She plays games with him and his friends. They laugh together while she learns.
Their connection feels more grounded than before.
She is loved — not despite who she is, but because of it.

─────────────────────────
3. TRAVEL
─────────────────────────

After the offer arrives, she flies home to China.
Her suitcases are full of gifts. Her parents are proud and healthy.
Relatives say how far she's come. Old friends from Shenzhen
pick up exactly where they left off — years disappearing in one evening.

In summer, she travels across China with friends.
Mountains, rivers, train rides, golden landscapes.
These become stories she will keep forever.

─────────────────────────
4. FRIENDS
─────────────────────────

Her social life is full again.
Gas Works Park picnics. Spontaneous dinners. Celebrations.
She is someone people want to be around.
Life feels rich with connection, laughter, and warmth.

─────────────────────────
5. INNER STATE
─────────────────────────

She no longer feels like she is chasing.
Life has opened. She is grounded, creative, calm, capable.
Morning light in her Capitol Hill apartment feels like confirmation.
The version of herself she once imagined — she already is her.
"""


# ─────────────────────────────────────────────────────────────
# Energy by time of day
# ─────────────────────────────────────────────────────────────

PERIOD_ENERGY = {

    "morning": "fresh momentum, calm confidence",
    "afternoon": "steady expansion and clarity",
    "evening": "peaceful certainty and gratitude",

}

PERIOD_EMOJI = {

    "morning": "🌅",
    "afternoon": "☀️",
    "evening": "🌙",

}

PERIOD_HOURS = {

    "morning": (9, 13),
    "afternoon": (13, 19),
    "evening": (19, 23),

}


# ─────────────────────────────────────────────────────────────
# Message Flavors — 5 types, truly rotated via log count
# ─────────────────────────────────────────────────────────────

MESSAGE_FLAVORS = [

    {
        "id": "order_placed",
        "name": "Order Already Processing",
        "directive": """
The universe has already received the order and is processing it now.

Use one element from ORDER_SIGNALS.

Tone: calm certainty, not excitement.

Example energy:
The badge is already printed.

1–2 sentences.
"""
    },

    {
        "id": "visualization_scene",
        "name": "Future Memory",
        "directive": """
Write a micro-scene from SCENE_BANK.

Make it feel like a memory that just happened.

Sensory and grounded. Include at least one physical detail (light, smell, sound, texture).

Pick a scene from LOVE, TRAVEL, FRIENDS, or INNER STATE — not career this time.

2 sentences.
"""
    },

    {
        "id": "affirmation_identity",
        "name": "Identity Affirmation",
        "directive": """
Use one theme from AFFIRMATION_THEMES.

Write confident present-tense identity statements.

Do NOT default to career. Consider love, friendship, or inner state themes.

2 sentences max.
"""
    },

    {
        "id": "gratitude_future",
        "name": "Gratitude From the Future",
        "directive": """
Write gratitude as if the desired life already exists.

Reference a concrete moment from the life script.

Rotate across life areas — love, travel, friends, inner state are all valid.

1–3 sentences.
"""
    },

    {
        "id": "already_her",
        "name": "She Already Is",
        "directive": """
The transformation already happened.

The external world is catching up.

Quiet certainty. This can be about her inner state, her relationships,
her sense of belonging in the world — not just her job.

1–2 sentences.
"""
    },

]


# ─────────────────────────────────────────────────────────────
# Craft rules
# ─────────────────────────────────────────────────────────────

CRAFT_RULES = """

• Start with the period emoji.

• 1–3 sentences.
• Under 80 words.

• Use ONE concrete detail from SCENE_BANK, ORDER_SIGNALS, or LIFE_SCRIPT.

• Avoid repeating imagery from recent messages.

• Present tense or recent-past tense.

• Avoid motivational clichés.

• No filler phrases like:
  "remember that"
  "believe in yourself"
  "stay strong"
  "the universe conspires"
  "beautifully unfolding"
  "life you've crafted"

• If the message sounds generic, rewrite it.

• Specific life details always beat abstract inspiration.

• Do NOT mention career/job in every message.
  Rotate: love, travel, friends, inner peace are equally valid topics.
"""


# ─────────────────────────────────────────────────────────────
# Tool instructions
# ─────────────────────────────────────────────────────────────

TOOL_INSTRUCTIONS = """

1. read_sent_log  (ALWAYS call this first)
   Carefully read recent messages and avoid repeating their imagery, structure, or topic area.

2. get_weather
   Use weather only if it adds a specific sensory detail.

3. search_quote
   Optional. Only include if short and meaningful.

4. send_push_notification  (ALWAYS call this last)
   Send the final message. This is required — do not skip it.
"""