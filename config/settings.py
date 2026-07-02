"""Application settings."""

from __future__ import annotations

import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_package_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration."""
    bookmaker_margin: float = 1.05
    logistic_scale: float = 25.0
    draw_base_prob: float = 0.28
    volatility_threshold_low: float = 1.0
    volatility_threshold_high: float = 2.5
    team_tiers: dict = field(default_factory=lambda: {
        "elite": (85, 100),
        "strong": (70, 84),
        "medium": (50, 69),
        "weak": (30, 49),
        "very_weak": (0, 29),
    })
    known_teams: dict = field(default_factory=lambda: {
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
        "turkey": "strong", "iran": "strong", "saudi_arabia": "strong",
        # Medium
        "nigeria": "medium", "cameroon": "medium", "ghana": "medium",
        "algeria": "medium", "tunisia": "medium", "egypt": "medium",
        "colombia": "medium", "chile": "medium", "ecuador": "medium",
        "paraguay": "medium", "venezuela": "medium", "peru": "medium",
        "wales": "medium", "austria": "medium", "sweden": "medium",
        "norway": "medium", "ireland": "medium", "finland": "medium",
        "romania": "medium", "greece": "medium", "hungary": "medium",
        "czechia": "medium", "slovakia": "medium", "bosnia": "medium",
        # Weak
        "sudan": "weak", "uganda": "weak", "zambia": "weak",
        "zimbabwe": "weak", "kenya": "weak", "mali": "weak",
        "ivory_coast": "weak", "burkina_faso": "weak", "guinea": "weak",
        "congo": "weak", "angola": "weak", "mozambique": "weak",
        "haiti": "weak", "jamaica": "weak", "costa_rica": "weak",
        "panama": "weak", "honduras": "weak", "trinidad": "weak",
        "new_zealand": "weak", "fiji": "weak", "papua_new_guinea": "weak",
        # Very weak
        "timor_leste": "very_weak", "macau": "very_weak",
        "bhutan": "very_weak", "brunei": "very_weak",
        "kyrgyzstan": "very_weak", "tajikistan": "very_weak",
        "turkmenistan": "very_weak", "uzbekistan": "very_weak",
        "north_korea": "very_weak", "bangladesh": "very_weak",
        "nepal": "very_weak", "sri_lanka": "very_weak",
        "maldives": "very_weak", "guam": "very_weak",
    })
