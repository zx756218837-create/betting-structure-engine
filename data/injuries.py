"""Injury report provider — mock injury/suspension data."""

from __future__ import annotations

from typing import Dict, List


class InjuryProvider:
    """Mock injury and suspension data provider."""

    def get_status(self, team: str) -> Dict[str, List[str]]:
        import hashlib
        h = hashlib.sha256(team.encode()).hexdigest()
        num_out = int(h[:2], 16) % 4  # 0-3
        num_doubtful = int(h[2:4], 16) % 3  # 0-2

        return {
            "out": num_out,
            "doubtful": num_doubtful,
            "available": 22 - num_out - num_doubtful,
            "provider": "mock",
        }
