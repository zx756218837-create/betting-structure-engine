"""Match-structure classifier.

Rules are heuristic and designed for academic market-structure modelling,
not for actual betting advice.
"""

from __future__ import annotations

import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)

from models import MatchInput, MatchStructure


def classify(input_data: MatchInput) -> MatchStructure:
    """Return the best-fit ``MatchStructure`` for the given odds snapshot.

    Priority order (first match wins):

    1. **STRONG_PRESS** – either side is heavily favoured (< 1.25).
    2. **BALANCED** – draw is tight (2.8-3.2) AND home/away gap < 0.5.
    3. **DEFENSIVE** – low total goals (≤ 2.5) AND near-even handicap.
    4. **DISTRIBUTED** – everything else.
    """

    # 1. Strong press – one side is a clear dominant favourite
    if input_data.home_odds < 1.25 or input_data.away_odds < 1.25:
        return MatchStructure.STRONG_PRESS

    # 2. Balanced – draw is compressed and home/away are close
    if 2.8 <= input_data.draw_odds <= 3.2:
        odds_gap = abs(input_data.home_odds - input_data.away_odds)
        if odds_gap < 0.5:
            return MatchStructure.BALANCED

    # 3. Defensive – low-scoring expectation with negligible handicap
    if input_data.total_goals <= 2.5 and abs(input_data.asian_handicap) <= 0.25:
        return MatchStructure.DEFENSIVE

    # 4. Distributed – everything else
    return MatchStructure.DISTRIBUTED
