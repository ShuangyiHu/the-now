# config.py
# ─────────────────────────────────────────────────────────────
# Affirmation Agent Configuration (V2)
# Expanded scene bank + manifestation signals + richer life script
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# Basic settings
# ─────────────────────────────────────────────────────────────

WEATHER_LOCATION = "Seattle"
MAX_LOG_ENTRIES = 80
RECENT_FOR_PROMPT = 12

LLM_TEMPERATURE = 1.35
LLM_TOP_P = 0.95

LANGUAGE = "English"


# ─────────────────────────────────────────────────────────────
# Scene Bank
# These are concrete life moments the LLM can use.
# Using them prevents repetitive generic affirmations.
# ─────────────────────────────────────────────────────────────

SCENE_BANK = [

"badge scanning at the office door in South Lake Union",
"pushing code and seeing the green PR checkmark",
"Slack notification that a pull request was merged",
"manager praising the async job queue design in a meeting",
"coffee at a Lake Union café before morning standup",
"walking beside Lake Union on a bright June morning",
"first paycheck notification hitting her bank account",
"booking a flight to visit her parents in China",
"packing suitcases with gifts for family",
"FaceTiming parents and showing them the Seattle apartment",
"Gas Works Park picnic with friends on a warm afternoon",
"laughing with friends during a spontaneous Seattle dinner",
"late night walk through Fremont after dinner",
"playing games with him and his friends for the first time",
"him smiling when she finally wins a round",
"quiet morning light filling the Capitol Hill apartment",
"reading near the window while Seattle sunlight fills the room",
"boarding the flight home after receiving the job offer",
"family welcoming her at the airport in China",
"giving gifts to relatives who are proud of her",
"meeting Shenzhen friends again after years apart",
"summer train ride across China with friends",
"standing on a mountain viewpoint during a China trip",
"taking photos together during summer travels",
]


# ─────────────────────────────────────────────────────────────
# Universe Order Signals
# Makes manifestation messages more concrete
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
# Rotated to prevent repetition
# ─────────────────────────────────────────────────────────────

AFFIRMATION_THEMES = [

"magnetic to the right engineering teams",
"naturally belonging among talented engineers",
"worthy of $150K+ opportunities with sponsorship",
"calmly confident in technical conversations",
"someone whose ideas land in design discussions",
"loved deeply and uniquely",
"respected for both intelligence and warmth",
"someone who creates meaningful friendships",
"someone whose life is expanding beautifully",
]


# ─────────────────────────────────────────────────────────────
# Life Script
# Rich detail = richer messages
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT = """
DESIRED REALITY (already unfolding — treat as true)

CAREER

Before June, she receives an offer for a Seattle-based Software Engineer / AI Engineer role with a base salary above $150K and OPT sponsorship.

The email arrives on a quiet weekday morning.

She opens it slowly in her Capitol Hill apartment while sunlight fills the room.

Now her life includes:

Walking along South Lake Union on bright Seattle mornings.

Passing Amazon and Google engineers and recognizing herself as one of them.

Badge scanning into the office for the first time.

A green checkmark appearing when her pull request merges.

Slack notifications saying “Merged” and “Nice work”.

In a team meeting, her manager describes her async job queue design as “clean and scalable”.

She participates in system design discussions.

Her ideas become part of the architecture.

She owns a backend service module and contributes with quiet confidence.

FINANCIAL LIFE

Her income allows a calm and comfortable Seattle life.

Weekend mornings begin slowly in her Capitol Hill apartment with sunlight through the windows.

Sometimes she walks to a café near Lake Union before work.

Weekends include:

Picnics at Gas Works Park.

Long walks by the water.

Reading outside in summer light.

Spontaneous dinners with friends.

Money is no longer stress — it simply supports the life she enjoys.

LOVE

Over time, her ex-boyfriend remembers more and more about what made her unique.

Her warmth, humor, intelligence, and emotional depth stay in his mind.

They begin talking again.

They see each other more often.

Casual dinners become longer conversations.

One evening walking through Fremont, he says quietly:

“I can see you've become stronger.”

They take things slowly but reconnect deeply.

She learns to play games with him and his friends.

They laugh together while she learns.

Their connection feels even more grounded than before.

FRIENDS

She spends more time with friends.

They meet for dinners, celebrations, and weekends together.

Life feels socially rich again.

TRAVEL

After receiving the job offer she flies back to China.

Her suitcases are filled with gifts.

Her parents are proud and healthy.

Relatives and family friends say how proud they are of her.

She reconnects with old friends from Shenzhen.

Years apart disappear in one evening of laughter.

During summer she travels across China with friends.

Mountains, rivers, train rides, and beautiful landscapes.

These memories become stories she will keep forever.

INNER STATE

She no longer feels like she is chasing life.

Life has opened.

She feels grounded, creative, calm, and capable.

The version of her she once imagined already exists.

And she is living as her now.
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
# Message Flavors
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

Sensory and grounded.

2 sentences.
"""
},

{
"id": "affirmation_identity",
"name": "Identity Affirmation",
"directive": """
Use one theme from AFFIRMATION_THEMES.

Write confident present-tense identity statements.

2 sentences max.
"""
},

{
"id": "gratitude_future",
"name": "Gratitude From the Future",
"directive": """
Write gratitude as if the desired life already exists.

Reference a concrete moment from the life script.

1–3 sentences.
"""
},

{
"id": "already_her",
"name": "She Already Is",
"directive": """
The transformation already happened.

The external world is catching up.

Quiet certainty.

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

• If the message sounds generic, rewrite it.

• Specific life details always beat abstract inspiration.
"""


# ─────────────────────────────────────────────────────────────
# Tool instructions
# ─────────────────────────────────────────────────────────────

TOOL_INSTRUCTIONS = """

1. read_sent_log
Carefully read recent messages and avoid repeating their imagery or structure.

2. get_weather
Use weather only if it adds a specific sensory detail.

3. search_quote
Optional. Only include if short and meaningful.

4. send_push_notification
Send the final message.
"""