"""Odds provider — generates realistic market odds from team names.

Uses the internal team strength model to produce odds that reflect
the relative strength of each side, plus some simulated market noise.
"""

from __future__ import annotations

import math
from typing import Dict, Any

import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)

from team_strength import get_strength_score, get_team_info


def generate_odds(home_team: str, away_team: str) -> Dict[str, float]:
    """Generate a full odds snapshot from two team names.

    Parameters
    ----------
    home_team : str
        Name of the home team.
    away_team : str
        Name of the away team.

    Returns
    -------
    dict
        Keys: ``home_odds``, ``draw_odds``, ``away_odds``,
        ``asian_handicap``, ``total_goals``.
    """
    home_info = get_team_info(home_team)
    away_info = get_team_info(away_team)

    home_score = home_info["score"]  # type: ignore[union-attr]
    away_score = away_info["score"]  # type: ignore[union-attr]

    # Strength differential (-100 .. +100)
    diff = home_score - away_score

    # Convert diff to implied probabilities using a logistic function
    # Higher diff → higher home win probability
    logistic = 1.0 / (1.0 + math.exp(-diff / 25.0))

    # Home win and away win probabilities (draw ~25-30%)
    p_home = logistic * 0.75 + 0.125
    p_away = (1 - logistic) * 0.75 + 0.125
    p_draw = 1.0 - p_home - p_away

    # Clamp probabilities to valid range
    p_home = max(0.05, min(p_home, 0.85))
    p_away = max(0.05, min(p_away, 0.85))
    p_draw = max(0.05, min(p_draw, 0.45))

    # Normalise to sum to 1
    total_p = p_home + p_draw + p_away
    p_home /= total_p
    p_draw /= total_p
    p_away /= total_p

    # Convert probabilities to decimal odds (with bookmaker margin ~5%)
    margin = 1.05
    home_odds = round(margin / p_home, 2)
    draw_odds = round(margin / p_draw, 2)
    away_odds = round(margin / p_away, 2)

    # Asian handicap from strength diff
    # diff > 20 → home favours -0.5 to -1.5
    # diff < -20 → away favours +0.5 to +1.5
    if diff >= 30:
        ah = -1.5
    elif diff >= 15:
        ah = -1.0
    elif diff >= 5:
        ah = -0.5
    elif diff >= -5:
        ah = 0.0
    elif diff >= -15:
        ah = 0.5
    elif diff >= -30:
        ah = 1.0
    else:
        ah = 1.5

    # Total goals from combined strength
    avg_strength = (home_score + away_score) / 2
    if avg_strength >= 80:
        total = 3.0
    elif avg_strength >= 60:
        total = 2.5
    elif avg_strength >= 40:
        total = 2.5
    else:
        total = 2.0

    return {
        "home_odds": home_odds,
        "draw_odds": draw_odds,
        "away_odds": away_odds,
        "asian_handicap": ah,
        "total_goals": total,
    }


def get_odds_snapshot(home_team: str, away_team: str) -> Dict[str, Any]:
    """Full snapshot including generated odds and team strength data."""
    odds = generate_odds(home_team, away_team)
    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_strength": get_team_info(home_team),
        "away_strength": get_team_info(away_team),
        "generated_odds": odds,
        "volatility": _estimate_volatility(odds),
        "mismatch": _detect_mismatch(home_team, away_team, odds),
    }


def _estimate_volatility(odds: Dict[str, float]) -> str:
    """Estimate market volatility from odds spread."""
    spread = max(odds["home_odds"], odds["away_odds"]) - min(
        odds["home_odds"], odds["away_odds"]
    )
    if spread < 1.0:
        return "LOW"
    if spread < 2.5:
        return "MEDIUM"
    return "HIGH"


def _detect_mismatch(home_team: str, away_team: str, odds: Dict[str, float]) -> Dict[str, Any]:
    """Detect gap between team strength and market odds."""
    home_score = get_team_info(home_team)["score"]  # type: ignore[union-attr]
    away_score = get_team_info(away_team)["score"]  # type: ignore[union-attr]
    strength_diff = home_score - away_score

    # Implied probability from odds
    home_implied = 1.0 / odds["home_odds"]
    away_implied = 1.0 / odds["away_odds"]
    total_implied = home_implied + 0.28 + away_implied  # ~28% draw

    home_prob = home_implied / total_implied
    away_prob = away_implied / total_implied

    # Strength-based probability
    strength_ratio = (strength_diff + 100) / 200.0
    strength_gap = abs(strength_ratio - home_prob)

    if strength_gap > 0.15:
        direction = "HOME_OVERVALUED" if strength_ratio > home_prob else "AWAY_OVERVALUED"
        severity = "SIGNIFICANT" if strength_gap > 0.25 else "MODERATE"
    else:
        direction = "MARKET_FAIR"
        severity = "NONE"

    return {
        "strength_ratio": round(strength_ratio, 3),
        "market_probability": round(home_prob, 3),
        "gap": round(strength_gap, 3),
        "direction": direction,
        "severity": severity,
    }
