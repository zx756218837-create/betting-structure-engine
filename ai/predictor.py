"""AI prediction engine — orchestrates all sub-models."""

from __future__ import annotations

from typing import Dict, Any

from ..classifier import classify
from ..probability import compute_score_probs
from ..risk import estimate_penalty_risk, map_risk_level
from ..arbitrage import detect_edge
from ..models import MatchInput, MatchStructure, EngineOutput
from .score_model import ScoreModel
from .probability_model import ProbabilityModel
from .confidence import ConfidenceModel
from .learning import LearningModel


class Predictor:
    """High-level prediction engine combining all sub-models.

    Given two team names, generates odds, classifies structure,
    computes score probabilities, and returns a comprehensive
    prediction with confidence scores.
    """

    def __init__(self) -> None:
        self.score_model = ScoreModel()
        self.probability_model = ProbabilityModel()
        self.confidence_model = ConfidenceModel()
        self.learning_model = LearningModel()

    def predict(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Run the full prediction pipeline.

        Returns a dict with:
        - win_prob, draw_prob, lose_prob
        - top_5_scores
        - confidence_score
        - cold_alert
        - recommended_pick
        - btts
        - over_under
        - plus all legacy fields
        """
        # Step 1 — generate odds from teams
        from ..odds_provider import generate_odds
        odds = generate_odds(home_team, away_team)

        # Step 2 — run existing pipeline
        inp = MatchInput(
            home_odds=odds["home_odds"],
            draw_odds=odds["draw_odds"],
            away_odds=odds["away_odds"],
            asian_handicap=odds["asian_handicap"],
            total_goals=odds["total_goals"],
        )
        structure = classify(inp)
        score_probs = compute_score_probs(structure)

        # Step 3 — AI sub-models
        win_prob, draw_prob, lose_prob = self.probability_model.compute(
            home_odds=odds["home_odds"],
            draw_odds=odds["draw_odds"],
            away_odds=odds["away_odds"],
        )

        top5 = self.score_model.top_scores(score_probs, n=5)

        confidence = self.confidence_model.compute(
            structure=structure,
            score_probs=score_probs,
            win_prob=win_prob,
        )

        btts = self._btts(score_probs)
        over_under = self._over_under(odds, score_probs)

        # Cold alert
        cold_alert = self._cold_alert(confidence, structure)

        # Recommended pick
        recommended = self._recommended_pick(confidence, structure, score_probs, win_prob, draw_prob, lose_prob)

        # Legacy fields
        penalty_risk = estimate_penalty_risk(structure)
        risk_level = map_risk_level(penalty_risk, structure)
        arbitrage = detect_edge(structure, score_probs)

        return {
            # AI predictions
            "win_prob": round(win_prob, 4),
            "draw_prob": round(draw_prob, 4),
            "lose_prob": round(lose_prob, 4),
            "top_5_scores": top5,
            "confidence_score": round(confidence, 4),
            "cold_alert": cold_alert,
            "recommended_pick": recommended,
            "btts": btts,
            "over_under": over_under,
            # Legacy
            "structure": structure.value,
            "score_probs": score_probs,
            "penalty_risk": round(penalty_risk, 4),
            "arbitrage": arbitrage.value,
            "risk": risk_level.value,
            "generated_odds": odds,
            "home_team": home_team,
            "away_team": away_team,
        }

    @staticmethod
    def _btts(score_probs: Dict[str, float]) -> Dict[str, object]:
        """Estimate Both Teams To Score probability."""
        btts_yes = sum(p for s, p in score_probs.items() if "-" in s and int(s.split("-")[0]) > 0 and int(s.split("-")[1]) > 0)
        return {
            "btts_yes": round(btts_yes, 4),
            "btts_no": round(1.0 - btts_yes, 4),
        }

    @staticmethod
    def _over_under(odds: Dict[str, float], score_probs: Dict[str, float]) -> Dict[str, object]:
        """Estimate over/under probabilities."""
        line = odds["total_goals"]
        over_scores = [s for s in score_probs if sum(int(x) for x in s.split("-")) > line]
        over_prob = sum(score_probs[s] for s in over_scores)
        return {
            "line": line,
            "over": round(over_prob, 4),
            "under": round(1.0 - over_prob, 4),
        }

    @staticmethod
    def _cold_alert(confidence: float, structure: MatchStructure) -> Dict[str, object]:
        """Generate cold/hot alert."""
        is_cold = confidence < 0.40
        return {
            "cold": is_cold,
            "hot": not is_cold,
            "message": "HOT PICK — High confidence signal" if not is_cold else "COLD ALERT — Low confidence, exercise caution",
        }

    @staticmethod
    def _recommended_pick(
        confidence: float,
        structure: MatchStructure,
        score_probs: Dict[str, float],
        win_prob: float,
        draw_prob: float,
        lose_prob: float,
    ) -> str:
        """Determine recommended pick based on analysis."""
        if confidence < 0.30:
            return "NO BET — Insufficient signal"

        probs = {"home": win_prob, "draw": draw_prob, "away": lose_prob}
        best = max(probs, key=probs.get)  # type: ignore[arg-type]

        if best == "home":
            return "HOME WIN"
        if best == "away":
            return "AWAY WIN"
        return "DRAW"
