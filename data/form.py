"""Form provider — mock recent form data."""

from __future__ import annotations

from typing import Dict, List


class FormProvider:
    """Mock recent form data provider."""

    def get_form(self, team: str) -> Dict[str, object]:
        import hashlib
        h = hashlib.sha256(team.encode()).hexdigest()
        nums = [int(h[i:i + 2], 16) % 3 for i in range(0, 10, 2)]
        results = ["W" if n == 2 else "D" if n == 1 else "L" for n in nums]

        wins = results.count("W")
        draws = results.count("D")
        losses = results.count("L")

        return {
            "last_5": results,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "points": wins * 3 + draws,
            "provider": "mock",
        }
