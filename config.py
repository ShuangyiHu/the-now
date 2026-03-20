# config.py
# ─────────────────────────────────────────────────────────────
# Affirmation Agent Configuration (V8)
#
# Key change: Three-way slot split, all time-based (no log counting).
#
# Slot type is determined purely by:
#   slot_index = 0..25  (9:00=0, 9:30=1, ..., 21:30=25)
#   day_of_year = 1..365
#
# Every 3 slots form a cycle:
#   slot_index % 3 == 0  →  LOVE (romantic / emotional)
#   slot_index % 3 == 1  →  GENERAL (career, friends, travel, inner state)
#   slot_index % 3 == 2  →  INTERVIEW (TikTok USDS)
#
# Flavor within each category rotates via (slot_index + day_of_year) % n,
# so the same time slot produces a different flavor on different days.
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# Basic settings
# ─────────────────────────────────────────────────────────────

WEATHER_LOCATION = "Seattle"
MAX_LOG_ENTRIES = 80
RECENT_FOR_PROMPT = 12

LLM_TEMPERATURE = 0.9
LLM_TOP_P = 0.95

LANGUAGE = "English"


# ─────────────────────────────────────────────────────────────
# Scene Bank — LOVE ONLY
# Romantic connection, intimacy, being seen and chosen.
# ─────────────────────────────────────────────────────────────

SCENE_BANK_LOVE = [

    "an evening walk together through a Seattle neighborhood, the conversation unhurried",
    "him noticing something about her that she thought no one saw — saying it simply",
    "losing badly at a game with his friends and laughing anyway, all of them laughing",
    "a slow morning where neither of them has anywhere to be, light through the blinds",
    "the moment she realizes he's been paying attention all along — something small proves it",
    "sitting close without needing to fill the silence, both of them just present",
    "him asking something real about her day and actually waiting for the answer",
    "a small ordinary moment — cooking, existing in the same space, it feeling like home",
    "catching his eye across a room and something passing between them wordlessly",
    "him remembering something minor she said weeks ago, bringing it back casually",
    "the feeling of being chosen — quietly, without drama, without needing to ask",
    "the first easy touch — a hand, a shoulder — that happens without either of them thinking",
    "walking through Fremont in the evening, him saying quietly: 'I can see you've become stronger'",
    "a Sunday morning where the only decision is what to eat, and both of them are unhurried",
    "him texting something small that shows he was thinking about her",

]


# ─────────────────────────────────────────────────────────────
# Scene Bank — GENERAL (career, friends, travel, inner state)
# No romantic content.
# ─────────────────────────────────────────────────────────────

SCENE_BANK_GENERAL = [

    # ── CAREER ───────────────────────────────────────────────
    "arriving at the South Lake Union office, badge in hand, the lobby quiet in the morning",
    "a PR review that ends with approval — the green checkmark, the brief exhale",
    "a design meeting where her solution becomes the one the team builds around",
    "the first morning coffee ritual at a Lake Union café before standup",
    "a walk along Lake Union when the weather finally breaks, thinking about nothing urgent",
    "the notification of a first paycheck — seeing the number, it being real",
    "a teammate referencing her work in a discussion she isn't even part of",
    "shipping something clean and watching it hold — no rollback, no incident",

    # ── TRAVEL ───────────────────────────────────────────────
    "boarding the flight home, the gate behind her, the destination ahead",
    "the airport arrivals hall — her family's faces before they see her",
    "spreading gifts across a table, watching relatives react to each one",
    "a meal with Shenzhen friends where the years between them simply disappear",
    "a train moving through Chinese countryside, the light changing outside the window",
    "standing at a high viewpoint on a mountain, the silence and the scale of it",
    "the suitcase packed with gifts, so full it barely closes",
    "showing her parents the Seattle apartment over FaceTime, turning the camera slowly",

    # ── FRIENDS ──────────────────────────────────────────────
    "a Gas Works Park afternoon with friends, food spread out, nowhere to be",
    "a dinner that wasn't planned, a restaurant that fit everyone, the table loud",
    "golden hour in Seattle with friends, everyone a little reluctant to leave",
    "a group photo taken impulsively — someone says take it, and they do",
    "a Shenzhen reunion where the conversation picks up mid-sentence from years ago",
    "the feeling after a good night with people she loves — full, easy, unhurried",
    "someone in the group saying something that makes everyone lose it simultaneously",

    # ── INNER STATE ───────────────────────────────────────────
    "morning light in the Capitol Hill apartment, no alarm, no urgency",
    "reading by the window while Seattle does its thing outside — being still in it",
    "waking up and noticing: the tightness is gone, replaced by something open",
    "a moment mid-day where she looks up and thinks: this is already the life",
    "the quiet that comes when she stops measuring herself against what she expected",
    "noticing her own calm during something that used to make her anxious",
    "the particular fullness of a day that was ordinary and enough",

]


# ─────────────────────────────────────────────────────────────
# Scene Bank — INTERVIEW ONLY
# ─────────────────────────────────────────────────────────────

SCENE_BANK_INTERVIEW = [

    "the moment the coding problem becomes clear — the approach unfolding before she types",
    "her voice steady as she explains her solution, the words coming without effort",
    "closing the laptop when it's over, the room quiet, knowing it went right",
    "the recruiter's email arriving — warm, direct, moving her forward",
    "reading the offer letter, the number real, the location Seattle",
    "badge scanning into the TikTok USDS office for the first time, coffee in hand",
    "settling into her new desk, the morning light coming through the window",
    "the celebration dinner with friends the night the offer arrives",
    "telling him — his reaction, the moment between hearing it and saying anything",
    "her parents' faces on FaceTime when she tells them, the sound of their voices",

]


# ─────────────────────────────────────────────────────────────
# Universe Order Signals — GENERAL (career, friends, travel)
# No love, no TikTok.
# ─────────────────────────────────────────────────────────────

ORDER_SIGNALS_GENERAL = [

    "the right team already has a seat for her",
    "HR is already preparing the paperwork",
    "the hiring manager already expects her",
    "her badge is already printed",
    "her desk already exists in the office",
    "her first project is already waiting",
    "the salary number is already decided",
    "the team is already making room for her contributions",
    "the opportunity is already in motion, moving toward her",

]


# ─────────────────────────────────────────────────────────────
# Universe Order Signals — LOVE ONLY
# ─────────────────────────────────────────────────────────────

ORDER_SIGNALS_LOVE = [

    "he already knows she's someone he doesn't want to lose",
    "the reconnection is already in motion, moving in its own quiet way",
    "the version of her he fell for — he's already remembering her",
    "the door between them is already open, even if neither has walked through yet",
    "the right moment for them is already being prepared",

]


# ─────────────────────────────────────────────────────────────
# Universe Order Signals — INTERVIEW ONLY
# ─────────────────────────────────────────────────────────────

ORDER_SIGNALS_INTERVIEW = [

    "the TikTok USDS interviewer already knows she's the right fit",
    "the TikTok USDS offer is already being prepared",
    "the TikTok USDS team already has her name on the candidate list",
    "the coding round result is already decided — she passed",
    "the TikTok USDS recruiter is already routing her to the next stage",

]


# ─────────────────────────────────────────────────────────────
# Affirmation Themes — LOVE ONLY
# ─────────────────────────────────────────────────────────────

AFFIRMATION_THEMES_LOVE = [

    "loved deeply and uniquely, for exactly who she is",
    "someone whose warmth is remembered and returned",
    "someone whose presence makes people want to stay",
    "someone whose love story is quietly, surely unfolding",
    "worthy of a love that is grounded, chosen, and real",
    "someone who is already being thought about",
    "someone who has always been worth coming back to",

]


# ─────────────────────────────────────────────────────────────
# Affirmation Themes — GENERAL (career, friends, travel, inner state)
# No love themes.
# ─────────────────────────────────────────────────────────────

AFFIRMATION_THEMES_GENERAL = [

    # Career
    "magnetic to the right engineering teams",
    "naturally belonging among talented engineers",
    "worthy of $150K+ opportunities with sponsorship",
    "calmly confident in technical conversations",
    "someone whose ideas land in design discussions",

    # Social / Travel
    "respected for both intelligence and warmth",
    "someone who creates meaningful friendships that last across years and distance",
    "someone people genuinely want around",

    # Inner state
    "someone whose life is expanding in ways she didn't have to force",
    "someone who has stopped chasing and started receiving",
    "grounded, creative, calm, and already the version of herself she once imagined",

]


# ─────────────────────────────────────────────────────────────
# Affirmation Themes — INTERVIEW ONLY
# ─────────────────────────────────────────────────────────────

AFFIRMATION_THEMES_INTERVIEW = [

    "technically sharp and ready for any coding challenge",
    "someone who thinks clearly under pressure",
    "someone the TikTok USDS team will immediately want on board",
    "calm, focused, and precise in every interview moment",
    "someone whose problem-solving instincts are already fully activated",

]


# ─────────────────────────────────────────────────────────────
# Life Script — LOVE ONLY
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT_LOVE = """
DESIRED REALITY — love and connection

Over time, her ex-boyfriend remembers what made her irreplaceable —
her humor, warmth, intelligence, and emotional depth.

They start talking again. Casual dinners become longer conversations.
One evening walking through Fremont, he says quietly:
"I can see you've become stronger."

They reconnect slowly but deeply.
She plays games with him and his friends. They laugh together.
Their connection feels more grounded than before.

She is loved — not despite who she is, but because of it.
She is chosen — quietly, without drama, without having to ask.
"""


# ─────────────────────────────────────────────────────────────
# Life Script — GENERAL
# Career, friends, travel, inner state. No love. No TikTok.
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT_GENERAL = """
DESIRED REALITY — already unfolding

─────────────────────────
1. CAREER
─────────────────────────

Before June, she receives a Software Engineer / AI Engineer offer in Seattle.
Base salary above $150K. OPT sponsorship included.

She badge-scans into the South Lake Union office for the first time.
Her pull requests merge. Her manager calls her design "clean and scalable."
She owns a backend service module. Her ideas shape the architecture.
She belongs here, without question.

─────────────────────────
2. TRAVEL
─────────────────────────

After the offer arrives, she flies home to China.
Her suitcases are full of gifts. Her parents are proud and healthy.
Relatives say how far she's come. Old friends from Shenzhen
pick up exactly where they left off — years disappearing in one evening.

In summer, she travels across China with friends.
Mountains, rivers, train rides, golden landscapes.
These become stories she will keep forever.

─────────────────────────
3. FRIENDS
─────────────────────────

Her social life is full again.
Gas Works Park picnics. Spontaneous dinners. Celebrations.
She is someone people want to be around.
Life feels rich with connection, laughter, and warmth.

─────────────────────────
4. INNER STATE
─────────────────────────

She no longer feels like she is chasing.
Life has opened. She is grounded, creative, calm, capable.
Morning light in her Capitol Hill apartment feels like confirmation.
The version of herself she once imagined — she already is her.
"""


# ─────────────────────────────────────────────────────────────
# Life Script — INTERVIEW ONLY
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT_INTERVIEW = """
TIKTOK USDS INTERVIEW — the next 10 days

She is interviewing for a Software Engineer role at TikTok USDS in Seattle.
The coding round is coming within the next ten days.

She walks into the interview — or opens the screen — with calm certainty.
Her hands are steady. Her thinking is clear. The problems unfold naturally.
She has done this before. She belongs in rooms like this.

She finishes the coding round feeling grounded and clean.
The solution was elegant. The explanation was clear. She knew it went well
before she closed the laptop.

Days later, the email arrives: the recruiter's message, warm and direct.
She moves to the next round. Then the offer.

She celebrates with friends over dinner — laughter, champagne, disbelief turning into joy.
She tells him. He pulls her close. "I knew you would," he says quietly.

She badge-scans into the TikTok USDS Seattle office on her first morning.
Coffee in hand. A new desk. The life she built, finally arrived.
"""


# ─────────────────────────────────────────────────────────────
# Energy by time of day
# ─────────────────────────────────────────────────────────────

PERIOD_ENERGY = {
    "morning":   "fresh momentum, calm confidence",
    "afternoon": "steady expansion and clarity",
    "evening":   "peaceful certainty and gratitude",
}

PERIOD_EMOJI = {
    "morning":   "🌅",
    "afternoon": "☀️",
    "evening":   "🌙",
}

PERIOD_HOURS = {
    "morning":   (9, 13),
    "afternoon": (13, 19),
    "evening":   (19, 23),
}


# ─────────────────────────────────────────────────────────────
# Message Flavors
#
# THREE CATEGORIES:
#   LOVE flavors     → LOVE_FLAVOR_INDICES
#   GENERAL flavors  → GENERAL_FLAVOR_INDICES
#   INTERVIEW flavors → INTERVIEW_FLAVOR_INDICES
# ─────────────────────────────────────────────────────────────

MESSAGE_FLAVORS = [

    # ── GENERAL FLAVORS (indices 0–4) ──────────────────────────

    {
        "id": "order_placed",
        "name": "Order Already Processing",
        "directive": """
The universe has already received the order and is processing it now.

Use one element from ORDER_SIGNALS as the anchor.

Topics: career, travel, friends, or inner state only.

Tone: calm certainty, not excitement.

1–2 sentences.
"""
    },

    {
        "id": "visualization_scene",
        "name": "Future Memory",
        "directive": """
Choose ONE scene from SCENE_BANK as your starting point.

The scene entry is a direction, not a script — do NOT reproduce its wording.
Instead, build outward from it: invent a specific detail the scene doesn't mention.
A sound. A texture. Something someone does with their hands. The quality of the light.
The temperature. A half-heard word. A specific small action.

Make it feel like a memory that just happened, not a description of a future hope.

Pick a scene from CAREER, TRAVEL, FRIENDS, or INNER STATE only.

2 sentences.
"""
    },

    {
        "id": "affirmation_identity",
        "name": "Identity Affirmation",
        "directive": """
Use one theme from AFFIRMATION_THEMES.

Write confident present-tense identity statements.

Topics: career, friendship, or inner state only. Not love.

2 sentences max.
"""
    },

    {
        "id": "gratitude_future",
        "name": "Gratitude From the Future",
        "directive": """
Write gratitude as if the desired life already exists.

Reference a concrete moment from the life script.

Topics: travel, friends, career, or inner state only. Not love.

1–3 sentences.
"""
    },

    {
        "id": "already_her",
        "name": "She Already Is",
        "directive": """
The transformation already happened. The external world is catching up.

Quiet certainty. Write about her inner state, her sense of belonging
in the world, or her professional identity.

Not love.

1–2 sentences.
"""
    },

    # ── LOVE FLAVORS (indices 5–8) ─────────────────────────────

    {
        "id": "love_order_placed",
        "name": "Love — Already in Motion",
        "directive": """
The reconnection is already happening, in its own quiet way.

Use one element from ORDER_SIGNALS as the anchor.

Tone: warm certainty, unhurried. Not desperate, not wishful — settled.

1–2 sentences.
"""
    },

    {
        "id": "love_scene",
        "name": "Love — Future Memory",
        "directive": """
Choose ONE scene from SCENE_BANK as your starting point.

Do NOT reproduce the scene's wording. Build outward from it:
invent one specific sensory detail — a texture, a sound, the temperature,
something he does with his hands, a half-heard word.

Make it feel like a memory that already happened, not a wish.

2 sentences.
"""
    },

    {
        "id": "love_identity",
        "name": "Love — She Is Already Loved",
        "directive": """
Use one theme from AFFIRMATION_THEMES.

Write present-tense identity statements about who she is in love —
how she is loved, how she is seen, how she is chosen.

Quiet, warm, certain. Not yearning.

2 sentences max.
"""
    },

    {
        "id": "love_already_her",
        "name": "Love — She Already Is That Woman",
        "directive": """
The woman he fell for — she already is her, and more.

The reconnection isn't something she has to earn or manufacture.
It's already moving toward her because of who she already is.

Write about her inner state, her growth, the quiet way she has become
someone worth returning to.

1–2 sentences. Third person. Warm certainty.
"""
    },

    # ── INTERVIEW FLAVORS (indices 9–10) ───────────────────────

    {
        "id": "tiktok_interview",
        "name": "TikTok USDS Interview — Already Won",
        "directive": """
She is preparing for her TikTok USDS coding interview, happening within 10 days.

Write ONE of these styles (check the recent log and pick whichever hasn't appeared):

STYLE A — Pre-interview confidence:
She is already the engineer TikTok USDS wants. Her skills are real.
When she opens that coding problem, her mind will be clear and her fingers
will move with certainty. Write as if the interview is a formality.

STYLE B — During the interview (vivid scene):
Her hands on the keyboard, the problem unfolding, her explanation clean and confident.
The interviewer is nodding. Sensory detail — the light on the screen, her voice.

STYLE C — After the coding round (already passed):
The interview just ended. She closes the laptop. She knows.
The solution was clean. The explanation was clear. It went exactly right.

STYLE D — The offer arrives:
The TikTok USDS recruiter's email is already being written.
Reference a specific celebration scene — make it vivid and concrete.

STYLE E — First day at TikTok USDS:
She badge-scans in. Sensory details: lobby, badge, coffee, new desk.
She belongs here. This is the life that was always coming.

Tone: calm certainty. Not hype. Already done.

1–3 sentences.
"""
    },

    {
        "id": "tiktok_cheerleader",
        "name": "TikTok USDS Interview — You've Got This",
        "directive": """
She is preparing for her TikTok USDS coding interview, happening within 10 days.

Write warm, direct encouragement — like a trusted friend looking her in the eyes
before she walks in. Right-now belief, not after-the-fact certainty.

Use "you" (second person). Present tense.

Make it SPECIFIC: TikTok USDS Seattle, software/AI engineering, coding round,
her personal qualities (sharp thinking, calm under pressure, persistence).

No clichés. No "believe in yourself." No "stay strong."

DO NOT start with the period emoji — start directly with the words.
Add the period emoji at the END.

2–3 sentences.
"""
    },

]

GENERAL_FLAVOR_INDICES   = [0, 1, 2, 3, 4]
LOVE_FLAVOR_INDICES      = [5, 6, 7, 8]
INTERVIEW_FLAVOR_INDICES = [9, 10]


# ─────────────────────────────────────────────────────────────
# Craft rules
# ─────────────────────────────────────────────────────────────

CRAFT_RULES = """

• Start with the period emoji (EXCEPT tiktok_cheerleader: put emoji at end).

• 1–3 sentences. Under 80 words.

• SCENE BANK entries are prompts, not scripts.
  Invent your own sensory detail: a gesture, a sound, the quality of light,
  a temperature, a specific small action. Never reproduce the bank's wording.

• Use ONE scene or signal as an anchor. Build outward from it.

• Avoid repeating imagery from recent messages.

• Present tense or recent-past tense.

• No filler phrases:
  "the universe conspires" / "beautifully unfolding" / "life you've crafted"
  "calm certainty" / "already unfolding" / "envelops you"
  "confirms that" / "affirms that" / "assures you"

• If the message sounds generic, rewrite it with a more specific invented detail.

• For "Already Won" / love certainty flavors: third person, settled, already done.
• For "You've Got This" flavor: second person, warm, direct.
"""


# ─────────────────────────────────────────────────────────────
# Tool instructions
# ─────────────────────────────────────────────────────────────

TOOL_INSTRUCTIONS = """

1. read_sent_log  (ALWAYS call this first)
   Check recent messages. Avoid repeating their imagery, structure, or topic.
   For interview messages: check which STYLE (A/B/C/D/E) appeared recently — pick a different one.

2. get_weather
   Only use if the weather detail adds something specific to the message.

3. send_push_notification  (ALWAYS call this last)
   Required. Do not skip.
"""