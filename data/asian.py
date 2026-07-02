"""Asian handicap provider — mock AH line data."""

from __future__ import annotations

from typing import Dict


class AsianHandicapProvider:
    """Mock Asian handicap data provider."""

    def __init__(self, known_teams: Dict[str, str]) -> None:
        self._known = {k.lower(): v for k, v in known_teams.items()}

    def get_line(self, home: str, away: str) -> Dict[str, object]:
        from team_strength import get_strength_score
        hs = get_strength_score(home)
        as_ = get_strength_score(away)
        diff = hs - as_

        if diff >= 30:
            line = -1.5
        elif diff >= 15:
            line = -1.0
        elif diff >= 5:
            line = -0.5
        elif diff >= -5:
            line = 0.0
        elif diff >= -15:
            line = 0.5
        elif diff >= -30:
            line = 1.0
        else:
            line = 1.5

        return {
            "line": line,
            "home_coverage": round((1.0 / (1.0 + abs(diff) / 50.0)), 2),
            "provider": "mock",
        }
