"""Arbitrage / edge detection.

Given a classified structure and its score-line probabilities, determine
whether any market inefficiency is flagged by the heuristic rules.
"""

from __future__ import annotations

from typing import Dict

from .models import MatchStructure, ArbitrageSignal


def detect_edge(
    structure: MatchStructure,
    score_probs: Dict[str, float],
) -> ArbitrageSignal:
    """Return the best-fit arbitrage signal.

    Rules:

    1. **BALANCED** + top score is 1-1 → ``VALUE_DRAW`` (draw is mispriced).
    2. **STRONG_PRESS** + 2-0 probability > 0.25 → ``VALUE_HOME``.
    3. **DISTRIBUTED** → ``NO_EDGE``.
    4. Everything else → ``NO_EDGE``.
    """

    # Rule 1 – balanced markets with 1-1 as the most likely score
    if structure == MatchStructure.BALANCED:
        top_score = max(score_probs, key=score_probs.get)  # type: ignore[arg-type]
        if top_score == "1-1":
            return ArbitrageSignal.VALUE_DRAW

    # Rule 2 – strong press with 2-0 heavily weighted
    if structure == MatchStructure.STRONG_PRESS:
        if score_probs.get("2-0", 0.0) > 0.25:
            return ArbitrageSignal.VALUE_HOME

    # Rule 3 – distributed markets carry no edge
    if structure == MatchStructure.DISTRIBUTED:
        return ArbitrageSignal.NO_EDGE

    # Default
    return ArbitrageSignal.NO_EDGE
