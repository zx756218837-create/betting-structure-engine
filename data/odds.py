"""Odds provider — mock historical and current odds data."""

from __future__ import annotations

from typing import Dict, Any


class OddsProvider:
    """Mock odds data provider.

    Returns deterministic odds snapshots based on team names.
    Real implementation would connect to an odds API (e.g. TheOddsApi, OddsPortal).
    """

    def __init__(self, known_teams: Dict[str, str], tiers: Dict[str, tuple[int, int]]) -> None:
        self._known = {k.lower(): v for k, v in known_teams.items()}
        self._tiers = tiers

    def get_current(self, home: str, away: str) -> Dict[str, Any]:
        """Return a mock current odds snapshot."""
        from team_strength import get_strength_score
        hs = get_strength_score(home)
        as_ = get_strength_score(away)
        diff = hs - as_

        import math
        logistic = 1.0 / (1.0 + math.exp(-diff / 25.0))
        p_home = logistic * 0.75 + 0.125
        p_away = (1 - logistic) * 0.75 + 0.125
        p_draw = 1.0 - p_home - p_away
        total_p = p_home + p_draw + p_away
        p_home, p_draw, p_away = p_home / total_p, p_draw / total_p, p_away / total_p

        margin = 1.05
        return {
            "home_odds": round(margin / p_home, 2),
            "draw_odds": round(margin / p_draw, 2),
            "away_odds": round(margin / p_away, 2),
            "asian_handicap": self._handicap_from_diff(diff),
            "total_goals": 2.5 if (hs + as_) / 2 >= 50 else 2.0,
            "provider": "mock",
            "timestamp": "2025-01-01T00:00:00Z",
        }

    @staticmethod
    def _handicap_from_diff(diff: float) -> float:
        if diff >= 30:
            return -1.5
        if diff >= 15:
            return -1.0
        if diff >= 5:
            return -0.5
        if diff >= -5:
            return 0.0
        if diff >= -15:
            return 0.5
        if diff >= -30:
            return 1.0
        return 1.5
