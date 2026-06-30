"""Data models and shared types for the betting structure engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Any


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MatchStructure(str, Enum):
    """Classified match market structure."""
    STRONG_PRESS = "STRONG_PRESS"
    BALANCED = "BALANCED"
    DEFENSIVE = "DEFENSIVE"
    DISTRIBUTED = "DISTRIBUTED"


class ArbitrageSignal(str, Enum):
    """Arbitrage / edge detection signal."""
    VALUE_DRAW = "VALUE_DRAW"
    VALUE_HOME = "VALUE_HOME"
    NO_EDGE = "NO_EDGE"


class RiskLevel(str, Enum):
    """Overall output risk level."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


# ---------------------------------------------------------------------------
# Input / Output dataclasses
# ---------------------------------------------------------------------------

@dataclass
class MatchInput:
    """Raw match odds input."""
    home_odds: float
    draw_odds: float
    away_odds: float
    asian_handicap: float
    total_goals: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MatchInput":
        """Construct from a plain dict (e.g. parsed JSON)."""
        return cls(**{k: float(v) for k, v in data.items()})

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:
        return (
            f"MatchInput(home={self.home_odds:.2f}, "
            f"draw={self.draw_odds:.2f}, "
            f"away={self.away_odds:.2f}, "
            f"ah={self.asian_handicap:+.2f}, "
            f"total={self.total_goals:.1f})"
        )


@dataclass
class ScoreProbEntry:
    """Probability for a single correct-score line."""
    score: str
    probability: float

    def to_dict(self) -> Dict[str, Any]:
        return {"score": self.score, "probability": round(self.probability, 4)}


@dataclass
class EngineOutput:
    """Full structured result from the engine."""
    structure: MatchStructure
    score_probs: Dict[str, float] = field(default_factory=dict)
    penalty_risk: float = 0.0
    arbitrage_signal: ArbitrageSignal = ArbitrageSignal.NO_EDGE
    risk_level: RiskLevel = RiskLevel.MEDIUM

    def to_dict(self) -> Dict[str, Any]:
        return {
            "structure": self.structure.value,
            "score_probs": self.score_probs,
            "penalty_risk": round(self.penalty_risk, 4),
            "arbitrage": self.arbitrage_signal.value,
            "risk": self.risk_level.value,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self) -> str:
        return self.to_json(indent=2)
