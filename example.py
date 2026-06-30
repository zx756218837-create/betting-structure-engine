"""Example usage of the betting structure engine.

Runs four representative scenarios covering each match structure.
"""

from __future__ import annotations

from .models import MatchInput
from .classifier import classify
from .probability import compute_score_probs
from .risk import estimate_penalty_risk, map_risk_level
from .arbitrage import detect_edge


def run_example(label: str, data: dict) -> None:
    """Run the full pipeline and print a formatted result."""
    inp = MatchInput(**{k: float(v) for k, v in data.items()})
    structure = classify(inp)
    score_probs = compute_score_probs(structure)
    penalty_risk = estimate_penalty_risk(structure)
    risk_level = map_risk_level(penalty_risk, structure)
    arbitrage = detect_edge(structure, score_probs)

    print(f"{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    print(f"  Input : {inp}")
    print(f"  Structure : {structure.value}")
    print(f"  Score probs : {score_probs}")
    print(f"  Penalty risk  : {penalty_risk:.2%}")
    print(f"  Risk level    : {risk_level.value}")
    print(f"  Arbitrage     : {arbitrage.value}")
    print()


def main() -> None:
    """Run four example scenarios."""

    # 1. STRONG_PRESS – home team is a heavy favourite
    run_example(
        "STRONG_PRESS example",
        {
            "home_odds": 1.15,
            "draw_odds": 7.0,
            "away_odds": 15.0,
            "asian_handicap": -1.5,
            "total_goals": 3.0,
        },
    )

    # 2. BALANCED – evenly matched, tight draw
    run_example(
        "BALANCED example",
        {
            "home_odds": 2.10,
            "draw_odds": 3.00,
            "away_odds": 2.40,
            "asian_handicap": 0.0,
            "total_goals": 2.5,
        },
    )

    # 3. DEFENSIVE – low-scoring, negligible handicap
    run_example(
        "DEFENSIVE example",
        {
            "home_odds": 2.00,
            "draw_odds": 3.10,
            "away_odds": 3.80,
            "asian_handicap": 0.0,
            "total_goals": 2.0,
        },
    )

    # 4. DISTRIBUTED – everything else
    run_example(
        "DISTRIBUTED example",
        {
            "home_odds": 1.80,
            "draw_odds": 3.50,
            "away_odds": 4.50,
            "asian_handicap": 0.5,
            "total_goals": 3.0,
        },
    )


if __name__ == "__main__":
    main()
