"""Confidence model — evaluates prediction confidence."""

from __future__ import annotations

import sys
import os
from typing import Dict

# Standalone import support (Streamlit Cloud pages mode)
_package_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_package_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from models import MatchStructure


class ConfidenceModel:
    """Computes a confidence score (0-1) for a prediction."""

    def compute(
        self,
        structure: MatchStructure,
        score_probs: Dict[str, float],
        win_prob: float,
    ) -> float:
        """Return confidence score between 0 and 1.

        Factors:
        - Structure clarity (stronger signals = higher confidence)
        - Top score probability concentration
        - Win probability dominance
        """
        # Base confidence from structure
        base = {
            MatchStructure.STRONG_PRESS: 0.75,
            MatchStructure.BALANCED: 0.45,
            MatchStructure.DEFENSIVE: 0.50,
            MatchStructure.DISTRIBUTED: 0.40,
        }
        confidence = base.get(structure, 0.50)

        # Score concentration bonus
        max_prob = max(score_probs.values()) if score_probs else 0.0
        confidence += (max_prob - 0.25) * 0.3

        # Win probability dominance bonus
        dominance = max(win_prob, 1.0 - win_prob)
        confidence += (dominance - 0.5) * 0.2

        return max(0.0, min(1.0, confidence))
