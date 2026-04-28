# content/__init__.py
# ─────────────────────────────────────────────────────────────
# Re-exports all public names from the content sub-modules.
#
# affirmation_agent.py does `from config import X`.
# config.py does `from content import *`.
# This file is the bridge — it must export every name that
# affirmation_agent.py imports from config.
# ─────────────────────────────────────────────────────────────

from content.locations import (
    LOCATIONS_SEATTLE,
    LOCATIONS_NATIONAL,
    LOCATIONS_ALL,
)

from content.life_scripts import (
    LIFE_SCRIPT_LOVE,
    LIFE_SCRIPT_WORK,
)

from content.scene_banks import (
    # Scene banks
    SCENE_BANK_LOVE,
    SCENE_BANK_WORK,
    # Order signals
    ORDER_SIGNALS_LOVE,
    ORDER_SIGNALS_WORK,
    # Affirmation themes
    AFFIRMATION_THEMES_LOVE,
    AFFIRMATION_THEMES_WORK,
    # Time-of-day config
    PERIOD_ENERGY,
    PERIOD_EMOJI,
    PERIOD_HOURS,
)

from content.flavors import (
    MESSAGE_FLAVORS,
    LOVE_FLAVOR_INDICES,
    WORK_FLAVOR_INDICES,
    CRAFT_RULES,
    TOOL_INSTRUCTIONS,
)

__all__ = [
    # locations
    "LOCATIONS_SEATTLE",
    "LOCATIONS_NATIONAL",
    "LOCATIONS_ALL",
    # life scripts
    "LIFE_SCRIPT_LOVE",
    "LIFE_SCRIPT_WORK",
    # scene banks
    "SCENE_BANK_LOVE",
    "SCENE_BANK_WORK",
    # order signals
    "ORDER_SIGNALS_LOVE",
    "ORDER_SIGNALS_WORK",
    # affirmation themes
    "AFFIRMATION_THEMES_LOVE",
    "AFFIRMATION_THEMES_WORK",
    # time-of-day
    "PERIOD_ENERGY",
    "PERIOD_EMOJI",
    "PERIOD_HOURS",
    # flavors
    "MESSAGE_FLAVORS",
    "LOVE_FLAVOR_INDICES",
    "WORK_FLAVOR_INDICES",
    "CRAFT_RULES",
    "TOOL_INSTRUCTIONS",
]
