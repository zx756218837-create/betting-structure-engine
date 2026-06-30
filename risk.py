"""Penalty-shootout risk estimator.

Heuristic mapping from match structure to an estimated probability that
the match will end 0-0 or 1-1 after extra time (i.e. require penalties).
"""

from __future__ import annotations

from .models import MatchStructure, RiskLevel


# Base penalty-risk probability per structure.
_PENALTY_RISK_MAP = {
    MatchStructure.BALANCED: 0.45,
    MatchStructure.DEFENSIVE: 0.45,
    MatchStructure.DISTRIBUTED: 0.30,
    MatchStructure.STRONG_PRESS: 0.10,
}


def estimate_penalty_risk(structure: MatchStructure) -> float:
    """Return the estimated probability of a penalty shootout."""
    return _PENALTY_RISK_MAP[structure]


def map_risk_level(penalty_risk: float, structure: MatchStructure) -> RiskLevel:
    """Derive a human-readable risk label from the numeric penalty risk.

    Rules:
    - penalty_risk >= 0.40 → VERY_HIGH
    - penalty_risk >= 0.30 → HIGH
    - penalty_risk >= 0.15 → MEDIUM
    - otherwise → LOW
    """
    if penalty_risk >= 0.40:
        return RiskLevel.VERY_HIGH
    if penalty_risk >= 0.30:
        return RiskLevel.HIGH
    if penalty_risk >= 0.15:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW
