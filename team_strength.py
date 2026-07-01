"""Team strength scoring model.

Maps team names to a strength score (0-100) and tier classification.
Used by ``odds_provider.py`` to generate realistic market odds from
team names alone.
"""

from __future__ import annotations

import hashlib
from typing import Dict, Tuple

# Tier definitions with base strength ranges.
_TIERS: Dict[str, Tuple[int, int]] = {
    "elite": (85, 100),
    "strong": (70, 84),
    "medium": (50, 69),
    "weak": (30, 49),
    "very_weak": (0, 29),
}

# Known teams mapped to tiers.  Add more as needed.
_TIER_MAP: Dict[str, str] = {
    # Elite
    "brazil": "elite", "france": "elite", "germany": "elite",
    "argentina": "elite", "england": "elite", "spain": "elite",
    "portugal": "elite", "netherlands": "elite", "belgium": "elite",
    "italy": "elite", "croatia": "elite", "uruguay": "elite",
    "usa": "elite", "canada": "elite", "mexico": "elite",
    # Strong
    "japan": "strong", "senegal": "strong", "morocco": "strong",
    "korea": "strong", "australia": "strong", "switzerland": "strong",
    "denmark": "strong", "poland": "strong", "scotland": "strong",
    "ukraine": "strong", "serbia": "strong", "turkey": "strong",
    "iran": "strong", "saudi_arabia": "strong", "south_korea": "strong",
    # Medium
    "nigeria": "medium", "cameroon": "medium", "ghana": "medium",
    "algeria": "medium", "tunisia": "medium", "egypt": "medium",
    "colombia": "medium", "chile": "medium", "ecuador": "medium",
    "paraguay": "medium", "venezuela": "medium", "peru": "medium",
    "wales": "medium", "austria": "medium", "czechia": "medium",
    "slovakia": "medium", "hungary": "medium", "greece": "medium",
    "sweden": "medium", "norway": "medium", "ireland": "medium",
    "ukraine": "medium", "finland": "medium", "bosnia": "medium",
    "romania": "medium", "georgia": "medium", "israel": "medium",
    "qatar": "medium", "uae": "medium", "indonesia": "medium",
    "thailand": "medium", "vietnam": "medium", "malaysia": "medium",
    "china": "medium", "chinese_taipei": "medium", "singapore": "medium",
    "philippines": "medium", "myanmar": "medium", "laos": "medium",
    "cambodia": "medium",
    # Weak
    "sudan": "weak", "uganda": "weak", "zambia": "weak",
    "zimbabwe": "weak", "kenya": "weak", "mali": "weak",
    "ivory_coast": "weak", "burkina_faso": "weak", "guinea": "weak",
    "congo": "weak", "angola": "weak", "mozambique": "weak",
    "haiti": "weak", "jamaica": "weak", "costa_rica": "weak",
    "panama": "weak", "honduras": "weak", "trinidad": "weak",
    "new_zealand": "weak", "fiji": "weak", "papua_new_guinea": "weak",
    "mongolia": "weak", "afghanistan": "weak", "palestine": "weak",
    "lebanon": "weak", "syria": "weak", "iraq": "weak",
    "jordan": "weak", "yemen": "weak", "oman": "weak",
    "bahrain": "weak", "kuwait": "weak",
    # Very weak
    "timor_leste": "very_weak", "macau": "very_weak",
    "bhutan": "very_weak", "brunei": "very_weak",
    "kyrgyzstan": "very_weak", "tajikistan": "very_weak",
    "turkmenistan": "very_weak", "uzbekistan": "very_weak",
    "north_korea": "very_weak", "myanmar": "very_weak",
    "laos": "very_weak", "cambodia": "very_weak",
    "bangladesh": "very_weak", "nepal": "very_weak",
    "sri_lanka": "very_weak", "maldives": "very_weak",
    "guam": "very_weak", "macau": "very_weak",
}


def _deterministic_hash(seed: str) -> float:
    """Return a float in [0, 1) deterministically from a seed string."""
    h = hashlib.sha256(seed.encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF


def get_tier(team: str) -> str:
    """Return the tier string for a team name (lowercased)."""
    return _TIER_MAP.get(team.lower().strip(), "medium")


def get_strength_score(team: str) -> int:
    """Return a deterministic strength score 0-100 for a team.

    Uses the team's tier as a range, then hashes the team name for
    a reproducible value within that range.
    """
    tier_key = get_tier(team)
    lo, hi = _TIERS[tier_key]
    rng = _deterministic_hash(team)
    return lo + int(rng * (hi - lo + 1))


def get_team_info(team: str) -> Dict[str, object]:
    """Return a full info dict for a team."""
    score = get_strength_score(team)
    tier = get_tier(team)
    return {
        "name": team,
        "score": score,
        "tier": tier,
    }
