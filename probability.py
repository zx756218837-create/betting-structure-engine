"""Score-line probability model.

Each structure maps to a fixed set of likely correct scores with heuristic
weights.  Weights are normalised so they sum to 1.0 within the structure.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from .models import MatchStructure


# (score_string, raw_weight) for each structure.
_SCORE_PROFILES: Dict[MatchStructure, List[Tuple[str, float]]] = {
    MatchStructure.STRONG_PRESS: [
        ("2-0", 0.30),
        ("2-1", 0.25),
        ("1-0", 0.25),
        ("3-0", 0.20),
    ],
    MatchStructure.BALANCED: [
        ("1-1", 0.30),
        ("0-0", 0.25),
        ("1-0", 0.25),
        ("0-1", 0.20),
    ],
    MatchStructure.DEFENSIVE: [
        ("0-0", 0.30),
        ("1-1", 0.25),
        ("1-0", 0.25),
        ("0-1", 0.20),
    ],
    MatchStructure.DISTRIBUTED: [
        ("1-2", 0.25),
        ("2-1", 0.25),
        ("1-1", 0.25),
        ("2-2", 0.25),
    ],
}


def compute_score_probs(structure: MatchStructure) -> Dict[str, float]:
    """Return normalised probabilities for each score line in the profile.

    The raw weights are divided by their sum so the result is a proper
    probability distribution.
    """
    profile = _SCORE_PROFILES[structure]
    total = sum(w for _, w in profile)
    return {score: round(weight / total, 4) for score, weight in profile}
