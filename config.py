# config.py
# ─────────────────────────────────────────────────────────────
# Affirmation Agent Configuration (V6)
# Fix: interview section moved to end of LIFE_SCRIPT to reduce
#      LLM attention bias toward interview content in general slots.
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
# Scene Bank
# Balanced across all 5 life areas + TikTok USDS interview
# ─────────────────────────────────────────────────────────────

SCENE_BANK = [

    # ── CAREER (general) ──────────────────────────────────────
    "arriving at the South Lake Union office, badge in hand, the lobby quiet in the morning",
    "a PR review that ends with approval — the green checkmark, the brief exhale",
    "a design meeting where her solution becomes the one the team builds around",
    "the first morning coffee ritual at a Lake Union café before standup",
    "a walk along Lake Union when the weather finally breaks, thinking about nothing urgent",
    "the notification of a first paycheck — seeing the number, it being real",
    "a teammate referencing her work in a discussion she isn't even part of",
    "shipping something clean and watching it hold — no rollback, no incident",

    # ── TIKTOK USDS INTERVIEW ─────────────────────────────────
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

    # ── LOVE ─────────────────────────────────────────────────
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
    "the quiet certainty that she is not waiting anymore — it's already begun",
    "noticing her own calm during something that used to make her anxious",
    "the particular fullness of a day that was ordinary and enough",

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

    # TikTok USDS specific
    "the TikTok USDS interviewer already knows she's the right fit",
    "the TikTok USDS offer is already being prepared",
    "the TikTok USDS team already has her name on the candidate list",
    "the coding round result is already decided — she passed",
    "the TikTok USDS recruiter is already routing her to the next stage",

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

    # TikTok USDS interview
    "technically sharp and ready for any coding challenge",
    "someone who thinks clearly under pressure",
    "someone the TikTok USDS team will immediately want on board",
    "calm, focused, and precise in every interview moment",
    "someone whose problem-solving instincts are already fully activated",

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
#
# FIX (V6): TIKTOK USDS INTERVIEW section moved to the END.
# Reason: LLM attention is biased toward content that appears early
# in the prompt. When interview content led the life script, the LLM
# defaulted to interview scenes even in general (non-interview) slots.
# Moving it to the end reduces that bias.
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT = """
DESIRED REALITY — six equal areas, all already unfolding

─────────────────────────
1. CAREER (broader)
─────────────────────────

Before June, she receives a Software Engineer / AI Engineer offer in Seattle.
Base salary above $150K. OPT sponsorship included.

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

─────────────────────────
0. TIKTOK USDS INTERVIEW (active now, next 10 days)
─────────────────────────

NOTE: This section is ONLY for messages with an interview flavor assigned.
General flavors must not draw from this section.

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
#
# ROTATION LOGIC (handled in affirmation_agent.py):
#   Every 3 messages → 1 interview flavor + 2 general flavors
#   Interview flavor index = 5 (tiktok_interview)
#   General flavors = indices 0–4, rotated among themselves
# ─────────────────────────────────────────────────────────────

MESSAGE_FLAVORS = [

    # ── GENERAL FLAVORS (indices 0–4) ──────────────────────────

    {
        "id": "order_placed",
        "name": "Order Already Processing",
        "directive": """
The universe has already received the order and is processing it now.

Use one element from ORDER_SIGNALS. Avoid TikTok-specific signals in this slot
unless the recent log shows no interview messages have appeared in a while.

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

Pick a scene from LOVE, TRAVEL, FRIENDS, or INNER STATE — not career or interview.

2 sentences.
"""
    },

    {
        "id": "affirmation_identity",
        "name": "Identity Affirmation",
        "directive": """
Use one theme from AFFIRMATION_THEMES (non-interview themes).

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
Avoid interview content in this slot.

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
her sense of belonging in the world — not her job or interview.

1–2 sentences.
"""
    },

    # ── INTERVIEW FLAVOR (index 5) ─────────────────────────────

    {
        "id": "tiktok_interview",
        "name": "TikTok USDS Interview — Already Won",
        "directive": """
She is preparing for her TikTok USDS coding interview, happening within 10 days.

Write ONE of these styles (vary based on recent log):

STYLE A — Pre-interview confidence:
She is already the engineer TikTok USDS wants. Her skills are real.
Her preparation has been real. When she opens that coding problem,
her mind will be clear and her fingers will move with certainty.
Write as if the interview is a formality confirming what's already true.

STYLE B — During the interview (vivid scene):
Write a micro-scene: her hands on the keyboard, the problem unfolding,
her explanation clean and confident. The interviewer is nodding.
Sensory detail — the light on the screen, the steadiness of her voice.

STYLE C — After the coding round (already passed):
The interview just ended. She closes the laptop. She knows.
The solution was clean. The explanation was clear. It went exactly right.

STYLE D — The offer arrives:
The TikTok USDS recruiter's email is already being written.
Reference a specific celebration scene — friends at dinner, him pulling her close,
her parents on FaceTime — make it vivid and concrete.

STYLE E — First day at TikTok USDS:
She badge-scans into the TikTok USDS Seattle office.
Sensory details: the lobby, the badge in her hand, coffee, her new desk.
She belongs here. This is the life that was always coming.

Pick the style that hasn't appeared recently. Use ONE concrete scene from SCENE_BANK.

Tone: calm certainty. Not hype. Not "you can do it." — already done.

1–3 sentences.
"""
    },

    # ── INTERVIEW CHEERLEADER FLAVOR (index 6) ────────────────────

    {
        "id": "tiktok_cheerleader",
        "name": "TikTok USDS Interview — You've Got This",
        "directive": """
She is preparing for her TikTok USDS coding interview, happening within 10 days.

Write unconditional, warm, direct encouragement — the kind a best friend or mentor
would say looking her in the eyes before she walks in.

This flavor is DIFFERENT from the other interview flavor:
  • That one speaks from after-the-fact certainty ("it already happened")
  • THIS one speaks from right-now belief ("you are ready, go get it")

Tone: warm, direct, energizing. Personal. Like someone who knows her well
and has zero doubt in their mind.

Use "you" voice (second person). Present tense.

Write something that feels like:
  "You have the skills. You've done the work. Walk in there and show them."
  "Every hard problem you've solved led to this moment — you are ready."
  "This is exactly the kind of challenge you were built for."

But make it SPECIFIC to her situation — reference:
  - TikTok USDS, Seattle
  - Her background as a software / AI engineer
  - The coding round specifically
  - Or her personal qualities: sharp thinking, calm under pressure, her persistence

No clichés. No "believe in yourself." No "stay strong."
Just direct, specific, warm certainty from someone who knows her.

DO NOT start with the period emoji — start directly with the words.
Add the period emoji at the END instead (after the final sentence).

2–3 sentences.
"""
    },

]

# Indices of general flavors vs interview flavors
GENERAL_FLAVOR_INDICES = [0, 1, 2, 3, 4]
INTERVIEW_FLAVOR_INDICES = [5, 6]  # tiktok_interview (calm certainty) + tiktok_cheerleader (warm encouragement)


# ─────────────────────────────────────────────────────────────
# Craft rules
# ─────────────────────────────────────────────────────────────

CRAFT_RULES = """

• Start with the period emoji.

• 1–3 sentences.
• Under 80 words.

• SCENE BANK entries are prompts for imagination, not scripts to quote.
  Use a scene as a starting point — invent your own sensory details,
  a specific gesture, a sound, a quality of light, a temperature.
  Never reproduce the exact wording from the scene bank.
  The goal is a moment that feels lived-in, not retrieved.

• Use ONE scene or signal as an anchor. Build outward from it.

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
  "you can do this"
  "you've got this"
  "calm certainty"

• If the message sounds generic, rewrite it.

• Specific invented detail always beats quoted source material.

• For interview flavor "Already Won": write from certainty, not encouragement.
  Third person. It already happened.

• For interview flavor "You've Got This": write direct warm encouragement.
  Second person ("you"). DO NOT start with the period emoji — put it at the end.
"""


# ─────────────────────────────────────────────────────────────
# Tool instructions
# ─────────────────────────────────────────────────────────────

TOOL_INSTRUCTIONS = """

1. read_sent_log  (ALWAYS call this first)
   Carefully read recent messages and avoid repeating their imagery, structure, or topic area.
   For interview messages: check which STYLE (A/B/C/D/E) was used recently and pick a different one.

2. get_weather
   Use weather only if it adds a specific sensory detail to the message.

3. send_push_notification  (ALWAYS call this last)
   Send the final message. This is required — do not skip it.
"""