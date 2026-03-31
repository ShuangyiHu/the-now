# config.py
# ─────────────────────────────────────────────────────────────
# Affirmation Agent Configuration (V9)
#
# Key changes from V8:
#   - LOCATIONS bank: Seattle-area + national landmarks with character details
#   - LIFE_SCRIPT_INTERVIEW: full 4-round interview arc + vivid offer letter moment
#   - LIFE_SCRIPT_LOVE: Sunday morning scene, locations beyond Fremont
#   - LIFE_SCRIPT_GENERAL: walking to work + paycheck scenes
#   - SCENE_BANK_INTERVIEW: next-steps email, each interview round, offer letter
#   - SCENE_BANK_LOVE / GENERAL: location variety, paycheck, Sunday morning
#   - TOOL_INSTRUCTIONS: weather only for Seattle locations
#   - CRAFT_RULES: location rotation note
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
# Locations Bank
#
# Used in LOVE and GENERAL scenes.
# Each entry: (name, character detail)
# LLM should use these as direction — invent fresh sensory detail
# inspired by the character note, never reproduce it verbatim.
#
# Seattle locations → weather tool may be called.
# Non-Seattle locations → assume pleasant, season-appropriate weather.
# ─────────────────────────────────────────────────────────────

LOCATIONS_SEATTLE = [
    ("Gas Works Park",          "rusted industrial towers against open sky, kite flyers, the lake glittering below"),
    ("Discovery Park",          "bluff trail ending at a lighthouse, Puget Sound wide and grey-green, eagles overhead"),
    ("Rattlesnake Ledge",       "the ridge appearing suddenly after the tree line, the lake perfectly still far below"),
    ("Mt. Rainier",             "the volcano filling the windshield on the drive in, meadows of wildflowers at Paradise"),
    ("Olympic Peninsula",       "Hoh Rainforest — moss hanging in silence, the sense of being inside something ancient"),
    ("Chihuly Garden",          "colored glass catching afternoon light among real plants, tourists moving slowly"),
    ("Kerry Park",              "the skyline view at dusk, the Space Needle small against the mountains"),
    ("Lake Union houseboats",   "the floating neighborhood, kayaks passing, smoke from chimneys on cold mornings"),
    ("Snoqualmie Falls",        "the roar before you see it, mist rising above the treeline, the lookout crowded"),
    ("Capitol Hill",            "the neighborhood alive on weekend evenings, neon in bar windows, the hill cresting"),
]

LOCATIONS_NATIONAL = [
    ("Yosemite Valley",         "El Capitan's sheer face in morning shadow, the valley floor green and unhurried"),
    ("Yellowstone",             "the sulfur smell arriving first, the geyser crowd going quiet before the eruption"),
    ("Grand Teton",             "the range rising without foothills, their reflection broken only by a passing elk"),
    ("San Francisco",           "fog rolling through the Golden Gate at dusk, the city lights just beginning below"),
    ("Big Sur",                 "Highway 1 clinging to cliffs, the Pacific enormous and dark to the horizon"),
    ("Zion Canyon",             "the Narrows — water around your ankles, canyon walls blocking the sky to a thin strip"),
    ("Grand Canyon South Rim",  "the first glimpse between trees before the full scale of it opens"),
    ("Acadia, Maine",           "Cadillac Mountain at sunrise, technically the first light in the country, the cold worth it"),
    ("Olympic National Park",   "the coast at Ruby Beach — sea stacks, driftwood, the Pacific cold and indifferent"),
    ("Sedona",                  "red rock formations glowing in late afternoon, the sky an impossible blue above them"),
]

# Combined for convenience
LOCATIONS_ALL = LOCATIONS_SEATTLE + LOCATIONS_NATIONAL


# ─────────────────────────────────────────────────────────────
# Scene Bank — LOVE ONLY
# Romantic connection, intimacy, being seen and chosen.
# ─────────────────────────────────────────────────────────────

SCENE_BANK_LOVE = [

    # ── SEATTLE ───────────────────────────────────────────────
    "an evening walk together through Capitol Hill, the neighborhood alive around them, neither in a hurry",
    "him noticing something about her that she thought no one saw — saying it simply, at Kerry Park",
    "sitting on the Gas Works lawn, not talking much, the lake moving below them",
    "walking the Discovery Park bluff trail, the Sound wide ahead, him slowing his pace to match hers",
    "catching his eye across a crowded Capitol Hill bar, something passing between them wordlessly",

    # ── TRAVEL / OTHER PLACES ─────────────────────────────────
    "standing at a Yosemite viewpoint together, the valley below, neither of them speaking for a long moment",
    "fog coming through the Golden Gate at dusk, San Francisco glittering below, him standing close",
    "a Sedona afternoon — red rocks glowing, the sky too blue, both of them unhurried",
    "the Grand Teton reflection in the lake, broken by wind, him pointing to something she almost missed",
    "Big Sur — pulled over on Highway 1, the ocean enormous below them, the moment belonging to no one else",

    # ── DOMESTIC / INTIMATE ───────────────────────────────────
    "a slow Sunday morning in bed, close and warm, neither of them needing to be anywhere",
    "moving to the kitchen together after a slow morning, sunlight in, making breakfast side by side",
    "a lazy Sunday afternoon back home — playing games, sharing small moments that need no commentary",
    "him asking something real about her day and actually waiting for the answer",
    "a small ordinary moment — cooking, existing in the same space, it feeling like home",
    "the first easy touch — a hand, a shoulder — that happens without either of them thinking",
    "him remembering something minor she said weeks ago, bringing it back casually",
    "the feeling of being chosen — quietly, without drama, without needing to ask",
    "a Sunday morning where the only decision is what to eat, and both of them are unhurried",
    "him texting something small that shows he was thinking about her",
    "losing badly at a game with his friends and laughing anyway, all of them laughing",
    "walking through Fremont in the evening, him saying quietly: 'I can see you've become stronger'",

]


# ─────────────────────────────────────────────────────────────
# Scene Bank — GENERAL (career, friends, travel, inner state)
# No romantic content.
# ─────────────────────────────────────────────────────────────

SCENE_BANK_GENERAL = [

    # ── CAREER ───────────────────────────────────────────────
    "arriving at the South Lake Union office, badge in hand, the lobby quiet in the morning",
    "walking to the office on a clear morning, sunlight on her face, her stride easy and unhurried",
    "the walk to work along Lake Union — fresh air, water visible between buildings, feeling exactly placed",
    "a PR review that ends with approval — the green checkmark, the brief exhale",
    "a design meeting where her solution becomes the one the team builds around",
    "a teammate referencing her work in a discussion she isn't even part of",
    "shipping something clean and watching it hold — no rollback, no incident",
    "the paycheck notification — $6,000 appearing in the account, the number settling into her like fact",
    "pausing at the paycheck deposit, feeling the specific calm satisfaction of money that came from her own work",

    # ── TRAVEL ───────────────────────────────────────────────
    "boarding the flight home, the gate behind her, the destination ahead",
    "the airport arrivals hall — her family's faces before they see her",
    "spreading gifts across a table, watching relatives react to each one",
    "a meal with Shenzhen friends where the years between them simply disappear",
    "the suitcase packed with gifts, so full it barely closes",
    "showing her parents the Seattle apartment over FaceTime, turning the camera slowly",
    "standing at the Yosemite Valley floor, El Capitan filling the sky, nothing urgent anywhere",
    "the Yellowstone crowd going silent just before the eruption, the anticipation collective",
    "Zion Narrows — cold water around her ankles, the canyon walls narrowing above her",
    "the Grand Canyon rim — the first gap in the trees before the full scale of it opens",
    "Rattlesnake Ledge — the ridge appearing, the lake perfectly still far below, the climb worth it",

    # ── FRIENDS ──────────────────────────────────────────────
    "a Gas Works Park afternoon with friends, food spread out, nowhere to be",
    "a dinner that wasn't planned, a restaurant that fit everyone, the table loud",
    "golden hour in Seattle with friends, everyone a little reluctant to leave",
    "a group photo taken impulsively — someone says take it, and they do",
    "a Shenzhen reunion where the conversation picks up mid-sentence from years ago",
    "the feeling after a good night with people she loves — full, easy, unhurried",
    "someone in the group saying something that makes everyone lose it simultaneously",
    "a Discovery Park afternoon with friends, the lighthouse visible at the end of the trail",

    # ── INNER STATE ───────────────────────────────────────────
    "morning light in the Capitol Hill apartment, no alarm, no urgency",
    "reading by the window while Seattle does its thing outside — being still in it",
    "waking up and noticing: the tightness is gone, replaced by something open",
    "a moment mid-day where she looks up and thinks: this is already the life",
    "the quiet that comes when she stops measuring herself against what she expected",
    "noticing her own calm during something that used to make her anxious",
    "the particular fullness of a day that was ordinary and enough",
    "standing at Kerry Park at dusk, the skyline below, the sense of belonging to this city",
    "a solo morning hike on Rattlesnake Ridge — the silence at the top, the whole valley hers",

]


# ─────────────────────────────────────────────────────────────
# Scene Bank — INTERVIEW ONLY
# Full arc: each round + offer letter + first day
# ─────────────────────────────────────────────────────────────

SCENE_BANK_INTERVIEW = [

    # ── NEXT STEPS EMAIL ──────────────────────────────────────
    "the recruiter's email arriving after round one — warm, direct, confirming next steps: three more rounds",
    "reading the next-steps email: coding round scheduled, then hiring manager, then skip-level — the path clear",
    "the calendar invite landing for the coding round, the date real, the preparation already done",

    # ── CODING ROUND ─────────────────────────────────────────
    "the moment the coding problem becomes clear — the approach unfolding before she types",
    "her voice steady as she explains her solution, the words coming without effort",
    "closing the laptop when the coding round is over, the room quiet, knowing it went right",
    "the specific calm after the coding round — not relief, something more settled than that",

    # ── HIRING MANAGER ROUND ──────────────────────────────────
    "the hiring manager round — a real conversation, her answers landing, being genuinely seen",
    "the HM asking a behavioral question and her answer surprising even herself with its clarity",
    "the tech discussion with the hiring manager flowing like a conversation between equals",

    # ── SKIP-LEVEL ROUND ─────────────────────────────────────
    "the skip-level round — showing how she thinks about systems, her vision landing clearly",
    "the skip manager asking about her approach to scale, her answer unhurried and precise",
    "the final round ending with the interviewer saying: 'we'll be in touch very soon'",

    # ── OFFER LETTER ─────────────────────────────────────────
    "reading the offer letter line by line, the number real, the location Seattle — the excitement settling into 'of course'",
    "the heart beating faster as the offer letter opens, then the deep calm landing: this has always been mine",
    "the offer letter moment — not surprise, but recognition. A quiet: yes. This.",
    "the celebration dinner with friends the night the offer arrives — laughter, champagne, disbelief turning into joy",
    "telling him — his reaction, the moment between hearing it and saying anything",

    # ── FIRST DAY ─────────────────────────────────────────────
    "badge scanning into the TikTok USDS office for the first time, coffee in hand",
    "settling into her new desk, the morning light coming through the window, the city below",
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
    "the $6,000 is already being processed, two weeks at a time",

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
    "the Sunday morning that belongs to both of them is already on its way",

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
    "the offer letter number is already written — she just hasn't read it yet",
    "the next-steps email is already in the recruiter's drafts",

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
    "someone who feels safe, held, and at home in love",
    "someone who can have everything she wants and feel deserving of it",

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
    "someone whose work earns real money and real stability",

    # Social / Travel
    "respected for both intelligence and warmth",
    "someone who creates meaningful friendships that last across years and distance",
    "someone people genuinely want around",
    "someone who moves through the world with ease and curiosity",

    # Inner state
    "someone whose life is expanding in ways she didn't have to force",
    "someone who has stopped chasing and started receiving",
    "grounded, creative, calm, and already the version of herself she once imagined",
    "someone who feels safe, abundant, and free",
    "someone who knows she can have what she wants — and feels joyful receiving it",

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
    "someone who moves through each interview round with ease and certainty",
    "someone who already knows she passed before the result arrives",

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

They reconnect slowly but deeply, in Seattle and beyond —
a weekend in San Francisco, a hike at Rattlesnake Ridge,
an afternoon at Kerry Park watching the skyline.

On a Sunday morning, they're in bed, close and warm,
neither of them needing to be anywhere.
They move into the kitchen together, sunlight pouring in,
making breakfast side by side without a plan.

In the afternoon, back home — games, small moments,
the easy rhythm of two people who have stopped performing for each other.
A steady happiness, not intense, not fleeting. Grounded and lasting.

She feels safe. She feels held. She feels like herself.

She plays games with him and his friends. They laugh together.
She is loved — not despite who she is, but because of it.
She is chosen — quietly, without drama, without having to ask.

She can have everything she wants. She knows this now.
And it feels like joy, not relief.
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

She walks to the office on clear mornings — sunlight on her face,
Lake Union visible between buildings, her stride easy and unhurried.
She belongs here before she even badges in.

Her pull requests merge. Her manager calls her design "clean and scalable."
She owns a backend service module. Her ideas shape the architecture.

Every two weeks, $6,000 lands in her account.
She pauses. Takes it in. Feels the specific calm satisfaction
of money that came from her own work. This is stability.
This is abundance. This is the natural result of who she is.

─────────────────────────
2. TRAVEL
─────────────────────────

After the offer arrives, she flies home to China.
Her suitcases are full of gifts. Her parents are proud and healthy.
Old friends from Shenzhen pick up exactly where they left off.

In summer, she travels — Yosemite, Yellowstone, the Grand Canyon,
Big Sur, Zion, San Francisco, Sedona.
Mountains, coastlines, canyons, golden light.
These become stories she will keep forever.

─────────────────────────
3. FRIENDS
─────────────────────────

Her social life is full again.
Gas Works Park picnics. Discovery Park afternoons.
Spontaneous dinners. Celebrations at Kerry Park.
She is someone people want to be around.
Life feels rich with connection, laughter, and warmth.

─────────────────────────
4. INNER STATE
─────────────────────────

She no longer feels like she is chasing.
Life has opened. She is grounded, creative, calm, capable.

She feels safe. She feels abundant. She feels free.
She knows she can have what she wants — and she feels joyful receiving it.

Morning light in her Capitol Hill apartment feels like confirmation.
The version of herself she once imagined — she already is her.
"""


# ─────────────────────────────────────────────────────────────
# Life Script — INTERVIEW ONLY
# Full 4-round arc: coding → HM → skip-level → offer
# ─────────────────────────────────────────────────────────────

LIFE_SCRIPT_INTERVIEW = """
TIKTOK USDS INTERVIEW — the full arc

She has completed round one. Three rounds remain:
  1. Coding round
  2. Hiring manager — technical & behavioral
  3. Skip-level manager — technical & behavioral

Each round, she shows up with calm certainty.
Her hands are steady. Her thinking is clear.
She has done this before. She belongs in rooms like this.

─────────────────────────
CODING ROUND
─────────────────────────

The problem becomes clear before she finishes reading it.
Her approach unfolds naturally — she explains as she goes,
her voice steady, her reasoning clean.

She closes the laptop when it's over.
The room is quiet. Not relief — something more settled.
She already knows.

─────────────────────────
HIRING MANAGER ROUND
─────────────────────────

The conversation flows like she imagined.
Her behavioral answers surprise even herself with their clarity.
The technical discussion feels like two engineers talking,
not a test. The hiring manager is nodding.

─────────────────────────
SKIP-LEVEL ROUND
─────────────────────────

She talks about systems, scale, her way of thinking about hard problems.
Her vision lands. The skip manager listens closely.
At the end, quietly: "we'll be in touch very soon."

─────────────────────────
THE OFFER LETTER
─────────────────────────

She picks up her phone and sees it — "Congratulations." "Offer Letter."
Her heart beats faster, a strong vivid pulse.
She opens it and reads line by line, the number real, the location Seattle.

The excitement settles into something deeper.
Calm. Grounded joy. A quiet: of course.
Gratitude rises gently, filling her chest.

She smiles — not because she's surprised,
but because she recognizes this moment.
This is mine. This has always been mine.

─────────────────────────
FIRST DAY
─────────────────────────

She badge-scans into the TikTok USDS Seattle office.
Coffee in hand. Morning light through the window.
Her new desk, the city below.

The life she built — finally arrived.
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

Use a location from LOCATIONS_ALL where it fits naturally.
Vary the location — check recent messages and pick somewhere not used recently.

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
Choose ONE scene from SCENE_BANK_LOVE as your starting point.

Do NOT reproduce the scene's wording. Build outward from it:
invent one specific sensory detail — a texture, a sound, the temperature,
something he does with his hands, a half-heard word.

Make it feel like a memory that already happened, not a wish.

Use a location from LOCATIONS_ALL where it fits naturally.
Vary the location — check recent messages and pick somewhere not used recently.
Seattle-area locations: you may call get_weather if weather adds something specific.
Non-Seattle locations: assume pleasant, season-appropriate weather — do not call get_weather.

2 sentences.
"""
    },

    {
        "id": "love_identity",
        "name": "Love — She Is Already Loved",
        "directive": """
Use one theme from AFFIRMATION_THEMES_LOVE.

Write present-tense identity statements about who she is in love —
how she is loved, how she is seen, how she is chosen.

Include the feeling of safety and deserving — she can have everything she wants.

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
someone worth returning to. Include the sense that she feels safe
and joyful receiving love — not waiting for it, already in it.

1–2 sentences. Third person. Warm certainty.
"""
    },

    # ── INTERVIEW FLAVORS (indices 9–10) ───────────────────────

    {
        "id": "tiktok_interview",
        "name": "TikTok USDS Interview — Already Won",
        "directive": """
She is interviewing for a Software Engineer role at TikTok USDS in Seattle.
There are four rounds total. Round one is complete. Remaining: coding round,
hiring manager round (tech & behavioral), skip-level round (tech & behavioral).

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
She picks up her phone. "Congratulations." "Offer Letter."
Her heart beats faster. She reads line by line. The number is real.
The excitement settles into calm grounded joy — a quiet: of course.
This has always been mine. Reference a specific celebration scene.

STYLE E — First day at TikTok USDS:
She badge-scans in. Sensory details: lobby, badge, coffee, new desk, morning light.
She belongs here. This is the life that was always coming.

STYLE F — Next steps / between rounds:
The recruiter's email arrived confirming the next round.
The path is clear: coding → HM → skip-level → offer.
Each step is already decided in her favor.

STYLE G — HM or skip-level round (vivid scene):
The conversation flows like equals talking.
Her answers land — technical clarity, behavioral depth, vision.
Write from inside the round, specific and grounded.

Tone: calm certainty. Not hype. Already done.

1–3 sentences.
"""
    },

    {
        "id": "tiktok_cheerleader",
        "name": "TikTok USDS Interview — You've Got This",
        "directive": """
She is interviewing for a Software Engineer role at TikTok USDS in Seattle.
Four rounds total — round one done. Remaining: coding, hiring manager, skip-level.

Write warm, direct encouragement — like a trusted friend looking her in the eyes
before she walks in. Right-now belief, not after-the-fact certainty.

Use "you" (second person). Present tense.

Make it SPECIFIC: TikTok USDS Seattle, software/AI engineering,
her personal qualities (sharp thinking, calm under pressure, persistence,
clear communication). Reference whichever round feels most immediate.

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

• LOCATION ROTATION: Check recent messages. Pick a location not used recently.
  Use LOCATIONS_ALL for variety — Seattle neighborhoods, national parks,
  other cities. Every message doesn't need a location, but when one fits,
  make it specific and varied.

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
   Note which locations have appeared recently — pick a different one.
   For interview messages: check which STYLE (A/B/C/D/E/F/G) appeared recently — pick a different one.

2. get_weather
   Call ONLY if the scene is set in Seattle or the immediate Seattle area
   (Capitol Hill, South Lake Union, Gas Works Park, Discovery Park, etc.)
   AND the weather detail adds something specific to the message.

   For all other locations (Yosemite, San Francisco, Yellowstone, Sedona, etc.):
   DO NOT call get_weather. Assume pleasant, season-appropriate weather
   and invent a specific atmospheric detail yourself.

3. send_push_notification  (ALWAYS call this last)
   Required. Do not skip.
"""