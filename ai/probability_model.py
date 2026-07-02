"""Probability model — computes win/draw/lose probabilities from odds."""

from __future__ import annotations

import sys
import os

# Standalone import support (Streamlit Cloud pages mode)
_package_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_package_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)


class ProbabilityModel:
    """Converts decimal odds to implied probabilities."""

    @staticmethod
    def compute(
        home_odds: float,
        draw_odds: float,
        away_odds: float,
    ):
        """Return (home_win_prob, draw_prob, away_win_prob).

        Removes bookmaker margin (implied probability normalisation).
        """
        inv_home = 1.0 / home_odds
        inv_draw = 1.0 / draw_odds
        inv_away = 1.0 / away_odds
        total = inv_home + inv_draw + inv_away

        return (
            inv_home / total,
            inv_draw / total,
            inv_away / total,
        )
