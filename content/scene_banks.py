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
# Romantic connection, physical intimacy, being seen and chosen.

SCENE_BANK_LOVE = [

    # Physical intimacy
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

    # Seattle
    "an evening walk together through Capitol Hill, the neighborhood alive around them, neither in a hurry",
    "him noticing something about her that she thought no one saw — saying it simply, at Kerry Park",
    "sitting on the Gas Works lawn, not talking much, the lake moving below them",
    "walking the Discovery Park bluff trail, the Sound wide ahead, him slowing his pace to match hers",
    "catching his eye across a crowded Capitol Hill bar, something passing between them wordlessly",

    # Travel
    "standing at a Yosemite viewpoint together, the valley below, neither of them speaking for a long moment",
    "fog coming through the Golden Gate at dusk, San Francisco glittering below, him standing close",
    "a Sedona afternoon — red rocks glowing, the sky too blue, both of them unhurried",
    "the Grand Teton reflection in the lake, broken by wind, him pointing to something she almost missed",
    "Big Sur — pulled over on Highway 1, the ocean enormous below them, the moment belonging to no one else",

    # Domestic / quiet intimacy
    "a slow Sunday morning in bed, close and warm, neither of them needing to be anywhere",
    "moving to the kitchen together after a slow morning, sunlight in, making breakfast side by side",
    "a lazy Sunday afternoon back home — games, small moments that need no commentary",
    "him asking something real about her day and actually waiting for the answer",
    "the feeling of being chosen — quietly, without drama, without needing to ask",
    "losing badly at a game with his friends and laughing anyway, all of them laughing",
    "walking through Fremont in the evening, him saying quietly: 'I can see you've become stronger'",
]


# ── GENERAL ───────────────────────────────────────────────────
# Career, friends, travel, inner state. No romantic content.

SCENE_BANK_GENERAL = [

    # Career
    "arriving at the South Lake Union office, badge in hand, the lobby quiet in the morning",
    "walking to the office on a clear morning, sunlight on her face, her stride easy and unhurried",
    "the walk to work along Lake Union — fresh air, water visible between buildings, feeling exactly placed",
    "a PR review that ends with approval — the green checkmark, the brief exhale",
    "a design meeting where her solution becomes the one the team builds around",
    "a teammate referencing her work in a discussion she isn't even part of",
    "shipping something clean and watching it hold — no rollback, no incident",
    "the paycheck notification — $6,000 appearing in the account, the number settling into her like fact",
    "pausing at the paycheck deposit, feeling the specific calm satisfaction of money that came from her own work",

    # Travel
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

    # Friends
    "a Gas Works Park afternoon with friends, food spread out, nowhere to be",
    "a dinner that wasn't planned, a restaurant that fit everyone, the table loud",
    "golden hour in Seattle with friends, everyone a little reluctant to leave",
    "a group photo taken impulsively — someone says take it, and they do",
    "a Shenzhen reunion where the conversation picks up mid-sentence from years ago",
    "the feeling after a good night with people she loves — full, easy, unhurried",
    "someone in the group saying something that makes everyone lose it simultaneously",
    "a Discovery Park afternoon with friends, the lighthouse visible at the end of the trail",

    # Inner state
    "morning light in the Capitol Hill apartment, no alarm, no urgency",
    "reading by the window while Seattle does its thing outside — being still in it",
    "waking up and noticing: the tightness is gone, replaced by something open",
    "a moment mid-day where she looks up and thinks: this is already the life",
    "noticing her own calm during something that used to make her anxious",
    "the particular fullness of a day that was ordinary and enough",
    "standing at Kerry Park at dusk, the skyline below, the sense of belonging to this city",
    "a solo morning hike on Rattlesnake Ridge — the silence at the top, the whole valley hers",
]


# ── INTERVIEW ─────────────────────────────────────────────────
# TikTok USDS arc. Coding done. Remaining: HM + skip-level + offer.

SCENE_BANK_INTERVIEW = [

    # Hiring manager round
    "the hiring manager round opening — she's already warmed up, already sharp, nothing left to prove",
    "the HM asking a behavioral question and her answer surprising even herself with its precision",
    "the tech discussion with the hiring manager flowing like a conversation between two engineers who think alike",
    "the moment the HM stops typing notes and just listens — because what she's saying is that good",
    "the hiring manager round ending, her voice steady, the interviewer's tone warm and decisive",

    # Skip-level round
    "the skip-level round — showing how she thinks about systems, her vision landing with authority",
    "the skip manager asking about her approach to scale, her answer unhurried and surgically precise",
    "the skip-level conversation shifting from interview to genuine dialogue — two people who see the same future",
    "the final round ending with the skip manager saying: 'we'll be in touch very soon' — and meaning it",
    "closing the laptop after the skip-level, the apartment quiet, the certainty already settled in her chest",

    # Offer letter
    "reading the offer letter line by line, the number real, the location Seattle — excitement settling into 'of course'",
    "the heart beating faster as the offer letter opens, then the deep calm landing: this has always been mine",
    "the offer letter moment — not surprise, but recognition. A quiet: yes. This.",
    "the celebration dinner with friends the night the offer arrives — laughter, champagne, disbelief turning into joy",
    "telling him — his reaction, the moment between hearing it and saying anything",

    # First day
    "badge scanning into the TikTok USDS office for the first time, coffee in hand",
    "settling into her new desk, the morning light coming through the window, the city below",
    "her parents' faces on FaceTime when she tells them, the sound of their voices",
]


# ═════════════════════════════════════════════════════════════
# UNIVERSE ORDER SIGNALS
# ═════════════════════════════════════════════════════════════

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

ORDER_SIGNALS_LOVE = [
    "he already knows she's someone he doesn't want to lose",
    "the reconnection is already in motion, moving in its own quiet way",
    "the version of her he fell for — he's already remembering her",
    "the door between them is already open, even if neither has walked through yet",
    "the right moment for them is already being prepared",
    "the Sunday morning that belongs to both of them is already on its way",
    "he already thinks about her more than he lets on",
]

ORDER_SIGNALS_INTERVIEW = [
    "the TikTok USDS offer is already written — she just hasn't read it yet",
    "the hiring manager already knows she's the one",
    "the skip-level manager is already expecting someone impressive — and she will be",
    "the TikTok USDS team already has her name circled",
    "the offer letter number is already decided in her favor",
    "the next-steps email confirming her advance is already drafted",
    "the headcount is already reserved for her",
]


# ═════════════════════════════════════════════════════════════
# AFFIRMATION THEMES
# ═════════════════════════════════════════════════════════════

AFFIRMATION_THEMES_LOVE = [
    "irresistibly herself — beautiful, sharp, warm, and impossible to forget",
    "the kind of woman men remember years later and regret letting go",
    "someone whose love is a privilege, not a given — and he knows it",
    "deeply loved, physically desired, and chosen with full certainty",
    "someone so magnetic that the reconnection was never really a question",
    "a woman who is strikingly beautiful, wickedly intelligent, and effortlessly warm",
    "someone who makes him feel more alive just by being in the room",
    "worthy of a love that is passionate, grounded, chosen, and physical",
    "someone who gets everything she wants in love — because she deserves it and she knows it",
    "a woman who can have any love she wants, and she has chosen well",
]

AFFIRMATION_THEMES_GENERAL = [
    # Career / money
    "a genuinely exceptional engineer — not almost, not someday, right now",
    "someone who commands $150K+ because her work is worth every dollar",
    "the kind of engineer teams fight to keep once they have her",
    "someone whose technical instincts are sharper than most people in the room",
    "someone who gets the offer because she is simply that good",
    # Identity / self-concept
    "beautiful, brilliant, and wildly capable — all three, all at once, always",
    "someone who gets what she wants because she decides she will",
    "a person who is lucky in the deepest sense: the right things find her",
    "someone whose wishes come true — not by accident, but because she is the kind of person they come true for",
    "unstoppable in the quietest, most certain way",
    "someone who has always been exceptional — the world is just catching up",
    # Social / life
    "someone people are genuinely lucky to know",
    "someone whose life keeps expanding because she refuses to settle for small",
    "grounded, radiant, and already living the life — right now, today",
    "someone who can have anything she wants and feels completely at ease receiving it",
]

AFFIRMATION_THEMES_INTERVIEW = [
    "one of the sharpest engineering candidates TikTok USDS will interview this year",
    "someone who makes interviewers wish the round didn't have to end",
    "technically brilliant and impossible to rattle under pressure",
    "the exact profile TikTok USDS built this role for",
    "someone who walks into that room and immediately shifts the energy",
    "so prepared, so sharp, so clear — the offer was never in doubt",
    "someone who doesn't just pass interviews — she makes them memorable",
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
