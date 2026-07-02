"""ELO rating provider — mock data for team ELO ratings."""

from __future__ import annotations

import hashlib
from typing import Dict


class ELOProvider:
    """Mock ELO rating provider.

    Generates deterministic ELO scores from team names.
    Real implementation would plug in an external API.
    """

    # Pre-defined ELO ranges per tier (approximate real-world values)
    _TIER_ELO: Dict[str, tuple[int, int]] = {
        "elite": (1900, 2100),
        "strong": (1750, 1899),
        "medium": (1550, 1749),
        "weak": (1300, 1549),
        "very_weak": (1000, 1299),
    }

    def __init__(self, known_teams: Dict[str, str], tiers: Dict[str, tuple[int, int]]) -> None:
        self._known = {k.lower(): v for k, v in known_teams.items()}
        self._tiers = tiers

    @staticmethod
    def _hash_int(seed: str, lo: int, hi: int) -> int:
        h = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16)
        return lo + h % (hi - lo + 1)

    def get_elo(self, team: str) -> int:
        tier_key = self._known.get(team.strip().lower(), "medium")
        lo, hi = self._TIER_ELO.get(tier_key, (1550, 1749))
        return self._hash_int(team, lo, hi)

    def get_elo_pair(self, home: str, away: str) -> Dict[str, int]:
        return {
            "home_elo": self.get_elo(home),
            "away_elo": self.get_elo(away),
        }
