"""Head-to-head provider — mock historical matchup data."""

from __future__ import annotations

from typing import Dict


class H2HProvider:
    """Mock head-to-head data provider."""

    def get_h2h(self, home: str, away: str) -> Dict[str, object]:
        import hashlib
        seed = f"{home}|{away}"
        h = hashlib.sha256(seed.encode()).hexdigest()
        nums = [int(h[i:i + 2], 16) % 10 for i in range(0, 10, 2)]

        home_wins = sum(1 for n in nums if n >= 6)
        draws = sum(1 for n in nums if 3 <= n < 6)
        away_wins = sum(1 for n in nums if n < 3)

        return {
            "home_wins": home_wins,
            "draws": draws,
            "away_wins": away_wins,
            "total_matches": len(nums),
            "home_win_rate": round(home_wins / len(nums), 2) if nums else 0.0,
            "provider": "mock",
        }
