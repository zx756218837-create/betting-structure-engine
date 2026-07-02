"""Learning model — tracks and scores prediction accuracy."""

from __future__ import annotations

from typing import Dict, List, Any


class LearningModel:
    """Simple tracking model for prediction accuracy.

    Stores prediction results and computes win rate statistics.
    In a real system this would connect to a database.
    """

    def __init__(self) -> None:
        self._history: List[Dict[str, Any]] = []

    def record(self, prediction: Dict[str, Any], actual_result: Dict[str, int] | None = None) -> None:
        """Record a prediction with optional actual result."""
        entry = {"prediction": prediction}
        if actual_result:
            entry["actual"] = actual_result
            entry["correct"] = self._check_correct(prediction, actual_result)
        self._history.append(entry)

    def accuracy(self) -> float:
        """Return overall accuracy rate."""
        scored = [e for e in self._history if "correct" in e]
        if not scored:
            return 0.0
        return sum(1 for e in scored if e["correct"]) / len(scored)

    def total_predictions(self) -> int:
        return len(self._history)

    @staticmethod
    def _check_correct(prediction: Dict[str, Any], actual: Dict[str, int]) -> bool:
        """Simple accuracy check: did the predicted winner match actual?"""
        rec = prediction.get("recommended_pick", "")
        if rec in ("HOME WIN", "DRAW", "AWAY WIN"):
            mapping = {"HOME WIN": "home", "DRAW": "draw", "AWAY WIN": "away"}
            return actual.get(mapping[rec]) == 1
        return False

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)
