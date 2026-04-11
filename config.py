# config.py
# ─────────────────────────────────────────────────────────────
# Runtime parameters only.
# All content (scripts, scenes, flavors, etc.) lives in content/
#
# affirmation_agent.py imports from here — do not rename this file.
# ─────────────────────────────────────────────────────────────

# ── Agent / log settings ──────────────────────────────────────
WEATHER_LOCATION  = "Seattle"
MAX_LOG_ENTRIES   = 80
RECENT_FOR_PROMPT = 12

# ── LLM settings ─────────────────────────────────────────────
LLM_TEMPERATURE = 0.9
LLM_TOP_P       = 0.95

# ── Language ──────────────────────────────────────────────────
LANGUAGE = "English"

# ── Re-export everything from the content package ─────────────
# affirmation_agent.py does `from config import X` — this keeps that working.
from content import *  # noqa: F401, F403, E402
