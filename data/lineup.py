"""Lineup provider — mock squad availability data."""

from __future__ import annotations

from typing import Dict, List


class LineupProvider:
    """Mock lineup data provider."""

    def get_lineup(self, team: str) -> Dict[str, List[str]]:
        import hashlib
        h = hashlib.sha256(team.encode()).hexdigest()
        num_starters = 9 + int(h[:2], 16) % 3  # 9-11
        num_subs = 3 + int(h[2:4], 16) % 3  # 3-5

        return {
            "formation": self._formation(num_starters),
            "starter_count": num_starters,
            "substitute_count": num_subs,
            "provider": "mock",
        }

    @staticmethod
    def _formation(count: int) -> str:
        return {9: "4-3-3", 10: "4-4-2", 11: "3-5-2"}.get(count, "4-3-3")
