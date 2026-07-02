"""FIFA ranking provider — mock data for FIFA world rankings."""

from __future__ import annotations

from typing import Dict


class FIFAProvider:
    """Mock FIFA ranking provider.

    Returns deterministic rankings based on team name hashing.
    """

    _TIER_RANK_RANGE: Dict[str, tuple[int, int]] = {
        "elite": (1, 10),
        "strong": (11, 30),
        "medium": (31, 70),
        "weak": (71, 120),
        "very_weak": (121, 211),
    }

    def __init__(self, known_teams: Dict[str, str]) -> None:
        self._known = {k.lower(): v for k, v in known_teams.items()}

    def get_rank(self, team: str) -> int:
        tier_key = self._known.get(team.strip().lower(), "medium")
        lo, hi = self._TIER_RANK_RANGE.get(tier_key, (31, 70))
        import hashlib
        h = int(hashlib.sha256(team.encode()).hexdigest()[:8], 16)
        return lo + h % (hi - lo + 1)

    def get_points(self, team: str) -> float:
        rank = self.get_rank(team)
        # Approximate: higher rank = more points, cap at ~1850
        return round(max(1400.0, 1850.0 - (rank - 1) * 5.5), 1)
