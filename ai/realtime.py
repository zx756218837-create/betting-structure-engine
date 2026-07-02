"""Realtime prediction module — supports streaming-style updates."""

from __future__ import annotations

from typing import Dict, Any, Optional


class RealtimePredictor:
    """Simulates realtime prediction updates.

    In a real system this would connect to a WebSocket or SSE stream.
    Here it provides incremental confidence updates based on simulated
    market movement.
    """

    def __init__(self, initial_prediction: Dict[str, Any]) -> None:
        self._prediction = initial_prediction
        self._updates: list[Dict[str, Any]] = []

    def simulate_update(self, tick: int) -> Dict[str, Any]:
        """Simulate a market update tick.

        Parameters
        ----------
        tick : int
            Current tick number (0-based).

        Returns
        -------
        dict
            Updated prediction state.
        """
        import hashlib
        h = hashlib.sha256(f"{tick}|{self._prediction.get('home_team', '')}".encode()).hexdigest()
        drift = (int(h[:4], 16) % 100 - 50) / 10000.0  # tiny drift

        updated = dict(self._prediction)
        if "win_prob" in updated:
            updated["win_prob"] = round(max(0.01, min(0.99, updated["win_prob"] + drift)), 4)
        if "draw_prob" in updated:
            updated["draw_prob"] = round(max(0.01, min(0.99, updated["draw_prob"] - drift * 0.5)), 4)
        if "lose_prob" in updated:
            updated["lose_prob"] = round(max(0.01, min(0.99, updated["lose_prob"] + drift * 0.3)), 4)

        self._updates.append(updated)
        return updated

    def latest(self) -> Optional[Dict[str, Any]]:
        """Return the most recent update."""
        return self._updates[-1] if self._updates else None

    def history(self) -> list[Dict[str, Any]]:
        return list(self._updates)
