"""Probability model — computes win/draw/lose probabilities from odds."""

from __future__ import annotations


class ProbabilityModel:
    """Converts decimal odds to implied probabilities."""

    @staticmethod
    def compute(
        home_odds: float,
        draw_odds: float,
        away_odds: float,
    ) -> Tuple[float, float, float]:
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
