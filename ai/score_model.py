"""Score model — computes and ranks likely correct scores."""

from __future__ import annotations

from typing import Dict, List, Tuple


class ScoreModel:
    """Generates ranked score-line predictions."""

    def top_scores(self, score_probs: Dict[str, float], n: int = 5) -> List[Dict[str, object]]:
        """Return the top N most likely scores.

        Parameters
        ----------
        score_probs : dict
            Mapping of score strings to probabilities.
        n : int
            Number of top scores to return.

        Returns
        -------
        list[dict]
            Each dict has ``score`` and ``probability`` keys.
        """
        sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)
        return [
            {"score": s, "probability": round(p, 4)}
            for s, p in sorted_scores[:n]
        ]

    def expected_goals(self, score_probs: Dict[str, float]) -> Dict[str, float]:
        """Compute expected goals for home and away from score distribution."""
        home_xg = 0.0
        away_xg = 0.0
        for score, prob in score_probs.items():
            parts = score.split("-")
            home_xg += int(parts[0]) * prob
            away_xg += int(parts[1]) * prob
        return {"home_xg": round(home_xg, 2), "away_xg": round(away_xg, 2)}
