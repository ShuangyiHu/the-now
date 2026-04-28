# content/scene_banks.py
# ─────────────────────────────────────────────────────────────
# Scene banks, universe order signals, affirmation themes,
# and time-of-day configuration.
#
# Scene bank entries are PROMPTS, not scripts — the LLM should
# invent fresh sensory detail from them, never reproduce verbatim.
# ─────────────────────────────────────────────────────────────


# ═════════════════════════════════════════════════════════════
# SCENE BANKS
# ═════════════════════════════════════════════════════════════

# ── LOVE ──────────────────────────────────────────────────────
# Romantic connection with SP, physical intimacy, life milestones
# (proposal, wedding, pregnancy), and the everyday tenderness of
# being deeply chosen.

SCENE_BANK_LOVE = [

    # ── Greek proposal (signature scene) ──
    "the Santorini proposal — whitewashed walls, the Aegean impossibly blue, him on one knee at a small clifftop chapel, a handful of curious cats wandering past as she says yes",
    "the moment in Greece when he reaches for the ring, and a tiny black-and-white kitten brushes against her ankle as if it knows what's happening",
    "Oia at golden hour, the caldera below, him whispering that he picked this place because it looked the way she makes him feel",
    "the boat ride to the chapel before the proposal — the wind in her hair, his hand at the small of her back, the future already pulling them in",
    "after she says yes — sitting on the warm stone steps, the ring catching the sun, two stray cats curled near her sandals",

    # ── Wedding ──
    "him at the end of the aisle when the doors open — the small breath, the eyes filling, the smile he can't hold back",
    "their first dance — her cheek against his shoulder, his hand spread across her lower back, the room dissolving",
    "the altar moment — him whispering 'you're it for me' against her ear, both of them barely holding it together",
    "her father walking her down the aisle, and the look between her father and her SP when he hands her over",
    "the kiss after the vows — long enough that the room laughs, neither of them caring",

    # ── Pregnancy / future family ──
    "his palm spread across her belly in the dark, both of them awake, neither quite believing how good their life has become",
    "the ultrasound moment — his free hand finding hers without looking, his thumb running over her knuckles",
    "him talking to her belly in the kitchen, low and serious, telling the baby everything they're going to do together",
    "her catching him at the nursery window late at night, just standing there looking at the empty crib like he can already see who'll fill it",
    "a quiet Saturday — her on the couch, his head on her stomach, headphones in, listening",

    # ── Physical intimacy / signature gestures ──
    "their fingers interlacing naturally, without either of them deciding to, walking through Fremont at dusk",
    "him pulling her into a kiss without warning, mid-sentence, both of them laughing into it",
    "her face pressed into his chest, his arms around her, neither of them moving for a long moment",
    "the first kiss after time apart — unhurried, certain, his hand at her jaw like she's something he doesn't want to rush",
    "waking up tangled together, her back against his chest, the room full of morning light neither of them wants to leave",
    "him kissing her forehead in the kitchen, without occasion, the simplest thing in the world",
    "his arms around her from behind as she reads, his chin at her shoulder, the weight of him warm and real",
    "their hands interlaced across the table at dinner, both of them talking to other people, holding on anyway",
    "a slow kiss against the wall of the Capitol Hill apartment, no reason, no destination, just that",
    "falling asleep mid-conversation, her head on his shoulder, him not moving so she can stay",
    "him brushing a strand of hair behind her ear and forgetting what he was saying",
    "her hand finding his under the blanket at 3am, neither of them awake enough to talk, just enough to hold on",
    "him kissing the inside of her wrist before letting go of her hand, every single time",
    "her sitting on the kitchen counter while he cooks, his hand on her knee whenever he passes",
    "him pulling her in by the waist as she walks past, just to slow her down for a kiss",

    # ── Seattle daily life together ──
    "an evening walk together through Capitol Hill, the neighborhood alive around them, neither in a hurry",
    "him noticing something about her that she thought no one saw — saying it simply, at Kerry Park",
    "sitting on the Gas Works lawn together, not talking much, the lake moving below them",
    "walking the Discovery Park bluff trail, the Sound wide ahead, him slowing his pace to match hers",
    "catching his eye across a crowded Capitol Hill bar, something passing between them wordlessly",
    "the South Lake Union walk home from dinner, his arm around her shoulders, the city quiet enough",

    # ── Travel together ──
    "standing at a Yosemite viewpoint together, the valley below, neither of them speaking for a long moment",
    "fog coming through the Golden Gate at dusk, San Francisco glittering below, him standing close",
    "a Sedona afternoon — red rocks glowing, the sky too blue, both of them unhurried",
    "the Grand Teton reflection in the lake, broken by wind, him pointing to something she almost missed",
    "Big Sur — pulled over on Highway 1, the ocean enormous below them, the moment belonging to no one else",
    "Mykonos at midnight — windmills, a glass of wine each, his hand finding hers without either of them looking",
    "a Sunday in Paris that turned into nothing planned, him following her into every bookshop",

    # ── Domestic / quiet intimacy ──
    "a slow Sunday morning in bed, close and warm, neither of them needing to be anywhere",
    "moving to the kitchen together after a slow morning, sunlight in, making breakfast side by side",
    "a lazy Sunday afternoon back home — small moments that need no commentary",
    "him asking something real about her day and actually waiting for the answer",
    "the feeling of being chosen — quietly, without drama, without needing to ask",
    "him bringing her tea in the morning without being asked, every morning",
    "the way he looks at her across the room when she doesn't know he's looking",
    "him saying her name in the dark like it's the only word he needs",
    "walking through Fremont in the evening, him saying quietly: 'I can see you've become stronger'",
    "him texting her in the middle of the day for no reason except that he was thinking about her",
]


# ── WORK ──────────────────────────────────────────────────────
# The dream job: aligned, easy, generously paid, deeply respected.
# She is always the first choice. Doors of abundance keep opening.

SCENE_BANK_WORK = [

    # ── The offer arriving ──
    "the recruiter's email landing in her inbox — the offer number higher than she even asked for",
    "opening the offer letter on her couch, reading the comp line by line, the calm 'of course' settling in",
    "the call from the hiring manager: 'we'd love to make this work — what would it take?'",
    "the moment she realizes three companies are competing for her at once, all of them above her old number",
    "the second email of the week from a recruiter who has clearly studied her work before reaching out",

    # ── The walk to work ──
    "walking to the office on a clear morning, sunlight on her face, her stride easy and unhurried",
    "the South Lake Union lobby in the morning — her badge in hand, the elevator already feeling like hers",
    "the Lake Union walk, water visible between buildings, the stride of someone who knows she belongs here",
    "stepping off the elevator on her floor, the day already feeling effortless",
    "morning coffee in the office kitchen, casual hellos, the easy belonging of being exactly where she fits",

    # ── Light, fun, aligned work ──
    "a task she finishes before lunch that she expected to take all day — the work just keeps being easier than she planned for",
    "the moment in a meeting where her one sentence reframes the whole problem and the room shifts",
    "a design doc that writes itself because she's been thinking this clearly for years",
    "the satisfaction of a clean PR merging on the first review — the green checkmark, the brief exhale",
    "an afternoon spent in flow, headphones in, building something she loves, the hours dissolving",
    "a 1:1 with her manager that turns into laughing about a side project, both of them excited",

    # ── Recognition / respect ──
    "her solution becoming the one the team builds around — without her having to push for it",
    "her teammate referencing her work in a discussion she isn't even part of",
    "her manager calling her design 'clean and scalable' in front of the whole team",
    "a senior engineer DM-ing her after the all-hands: 'that idea you proposed — that's the right call'",
    "skip-level praise landing in her inbox, specific and unprompted",
    "an unsolicited 'we're so glad you're here' from someone whose opinion she actually respects",
    "the moment she realizes everyone in the room defers to her on this — quietly, naturally, without it being weird",

    # ── Money / abundance ──
    "the paycheck notification — the number well above what she used to dream of, settling into her like fact",
    "a bonus deposit she didn't see coming, landing on a Tuesday for no reason except that they wanted to keep her",
    "the equity refresh email — the number higher than the original grant, the message warm",
    "a raise that arrives before she even thought about asking",
    "her bank balance crossing a threshold she remembers being afraid of a year ago",
    "pausing at the deposit notification, feeling the specific calm of money that came from her own work",

    # ── Doors opening / opportunity flow ──
    "an inbound message from a company she'd actually want to work for, written like they've already decided they want her",
    "a contact reaching out about an advisory role, then another, the calendar getting interesting",
    "the LinkedIn DMs piling up — recruiters, founders, people wanting her on their thing",
    "a dream-team conversation that happens because someone she barely knows mentioned her name in the right room",
    "the realization that the next role isn't a question of finding it — it's a question of choosing among them",

    # ── Work-life balance / freedom ──
    "closing the laptop at 5pm because the work is genuinely done — not deferred, not avoided, finished",
    "a Tuesday afternoon walk in the middle of the day because she can, and the work doesn't suffer",
    "a long weekend she takes without guilt because the team is fine and she's earned it many times over",
    "morning light in the Capitol Hill apartment, no alarm, no urgency — and a job that pays her like this",
    "a midweek dinner with him that runs late because nothing about her schedule fights it",
    "the particular fullness of a workday that was light, productive, and over by dinner",

    # ── Inner state ──
    "the moment mid-day where she looks up and thinks: this is already the life",
    "noticing her own calm during something that used to feel like pressure",
    "the version of herself she once imagined in this exact role — she already is her",
]


# ═════════════════════════════════════════════════════════════
# UNIVERSE ORDER SIGNALS
# ═════════════════════════════════════════════════════════════

ORDER_SIGNALS_LOVE = [
    "he already knows she's the one — the only one he can imagine a life with",
    "he already thinks about her more than he lets on, more than he shows",
    "the proposal is already written into the timeline — the ring already chosen",
    "the version of her he fell for — he's already remembering, already coming back",
    "the door between them is already open, the rest is just timing",
    "the Sunday morning that belongs to both of them is already on its way",
    "her wedding day is already a date in someone's calendar, somewhere in the field",
    "the family they'll build is already moving toward them",
    "she is already his first choice — has been for longer than he realized",
    "the universe has already lined up the love that's coming, exactly the way she wanted it",
]

ORDER_SIGNALS_WORK = [
    "the dream-job offer is already written — she just hasn't read it yet",
    "the right team already has a seat reserved for her",
    "the hiring manager already knows she's the one",
    "her badge is already printed, her desk already exists",
    "the comp number is already decided in her favor — and it's higher than she expected",
    "the recruiter who'll change her trajectory is already drafting the email",
    "doors of abundance are already opening — she just walks through",
    "the high-paying, easy, soul-aligned opportunity is already on its way to her",
    "she's already been chosen — the paperwork is just catching up",
    "the universe has already filed the offer; she'll be holding it soon",
]


# ═════════════════════════════════════════════════════════════
# AFFIRMATION THEMES
# ═════════════════════════════════════════════════════════════

AFFIRMATION_THEMES_LOVE = [
    "irresistibly herself — beautiful, sharp, warm, and impossible to forget",
    "the most desirable, magnetic, and irresistible woman her SP has ever known",
    "the kind of woman whose presence rewires a room — and whose absence is felt for years",
    "deeply loved, physically desired, prioritized, and chosen with full certainty",
    "the love of her SP's life — the only one he desires, the one he can't stop thinking about",
    "the woman he chose to build a future with — the one he can't imagine his life without",
    "cherished, adored, prioritized — showered with love and affection without ever asking",
    "always the first choice in love — naturally, inevitably, every time",
    "the perfect match, the person he's always dreamed of, finally his",
    "a woman who is strikingly beautiful, wickedly intelligent, and effortlessly warm",
    "someone who gets exactly the love she wants — because she is genuinely that worthy of it",
    "the kind of woman whose love story includes a Greek proposal, a wedding she'll remember forever, and a family that already feels like home",
]

AFFIRMATION_THEMES_WORK = [
    "effortlessly aligned with the dream job — every day feels like play",
    "the ideal candidate for every role she desires — skills, taste, and presence unmatched",
    "the obvious first choice — always, in every hiring loop she enters",
    "a magnet for high-paying, easy, fun, soul-aligned opportunities",
    "generously paid, deeply respected, and recognized for excellence",
    "someone whose work is light, joyful, and brings out the best in her",
    "the kind of engineer companies fight to keep — and pay accordingly",
    "someone who commands a salary far above market because her work is worth every dollar",
    "doors of abundance, success, and visibility constantly opening for her",
    "rewarded in ways that exceed her wildest dreams — bonuses, equity, raises arriving on schedule and beyond it",
    "thriving in every possible way — career, money, balance, and inner ease",
    "always chosen for the role she actually wants — never the consolation prize",
]


# ═════════════════════════════════════════════════════════════
# TIME-OF-DAY CONFIGURATION
# ═════════════════════════════════════════════════════════════

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

# Each value: (start_hour_inclusive, end_hour_exclusive)
PERIOD_HOURS = {
    "morning":   (9, 13),
    "afternoon": (13, 19),
    "evening":   (19, 24),
}
