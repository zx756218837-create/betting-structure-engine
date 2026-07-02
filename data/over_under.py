"""Over/Under provider — mock total goals line data."""

from __future__ import annotations

from typing import Dict


class OverUnderProvider:
    """Mock over/under total goals provider."""

    def __init__(self, known_teams: Dict[str, str]) -> None:
        self._known = {k.lower(): v for k, v in known_teams.items()}

    def get_line(self, home: str, away: str) -> Dict[str, object]:
        from team_strength import get_strength_score
        hs = get_strength_score(home)
        as_ = get_strength_score(away)
        avg = (hs + as_) / 2

        if avg >= 80:
            total = 3.0
        elif avg >= 60:
            total = 2.5
        elif avg >= 40:
            total = 2.5
        else:
            total = 2.0

        return {
            "line": total,
            "over_probability": round(min(avg / 100.0, 0.75), 2),
            "provider": "mock",
        }
