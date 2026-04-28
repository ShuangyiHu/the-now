# content/locations.py
# ─────────────────────────────────────────────────────────────
# Location banks used in LOVE and WORK scene generation.
#
# Each entry: (name, character detail)
# The character detail is a direction for the LLM — it should
# invent fresh sensory detail inspired by it, never reproduce verbatim.
# ─────────────────────────────────────────────────────────────

LOCATIONS_SEATTLE = [
    ("Gas Works Park",        "rusted industrial towers against open sky, kite flyers, the lake glittering below"),
    ("Discovery Park",        "bluff trail ending at a lighthouse, Puget Sound wide and grey-green, eagles overhead"),
    ("Rattlesnake Ledge",     "the ridge appearing suddenly after the tree line, the lake perfectly still far below"),
    ("Mt. Rainier",           "the volcano filling the windshield on the drive in, meadows of wildflowers at Paradise"),
    ("Olympic Peninsula",     "Hoh Rainforest — moss hanging in silence, the sense of being inside something ancient"),
    ("Chihuly Garden",        "colored glass catching afternoon light among real plants, tourists moving slowly"),
    ("Kerry Park",            "the skyline view at dusk, the Space Needle small against the mountains"),
    ("Lake Union houseboats", "the floating neighborhood, kayaks passing, smoke from chimneys on cold mornings"),
    ("Snoqualmie Falls",      "the roar before you see it, mist rising above the treeline, the lookout crowded"),
    ("Capitol Hill",          "the neighborhood alive on weekend evenings, neon in bar windows, the hill cresting"),
]

LOCATIONS_NATIONAL = [
    ("Yosemite Valley",        "El Capitan's sheer face in morning shadow, the valley floor green and unhurried"),
    ("Yellowstone",            "the sulfur smell arriving first, the geyser crowd going quiet before the eruption"),
    ("Grand Teton",            "the range rising without foothills, their reflection broken only by a passing elk"),
    ("San Francisco",          "fog rolling through the Golden Gate at dusk, the city lights just beginning below"),
    ("Big Sur",                "Highway 1 clinging to cliffs, the Pacific enormous and dark to the horizon"),
    ("Zion Canyon",            "the Narrows — water around your ankles, canyon walls blocking the sky to a thin strip"),
    ("Grand Canyon South Rim", "the first glimpse between trees before the full scale of it opens"),
    ("Acadia, Maine",          "Cadillac Mountain at sunrise, technically the first light in the country, the cold worth it"),
    ("Olympic National Park",  "the coast at Ruby Beach — sea stacks, driftwood, the Pacific cold and indifferent"),
    ("Sedona",                 "red rock formations glowing in late afternoon, the sky an impossible blue above them"),
]

LOCATIONS_ALL = LOCATIONS_SEATTLE + LOCATIONS_NATIONAL
