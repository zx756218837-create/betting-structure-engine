#!/usr/bin/env python3
"""CLI entry point for the betting structure engine.

Usage::

    python main.py --home 1.9 --draw 3.2 --away 4.1 --ah 0 --total 2.5

Outputs structured JSON to stdout.
"""

from __future__ import annotations

import argparse

from .models import MatchInput
from .engine import run


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Betting Structure Engine v10 — academic market classification",
    )
    parser.add_argument("--home", type=float, required=True, help="Home win decimal odds")
    parser.add_argument("--draw", type=float, required=True, help="Draw decimal odds")
    parser.add_argument("--away", type=float, required=True, help="Away win decimal odds")
    parser.add_argument("--ah", type=float, required=True, help="Asian handicap (e.g. -0.5, 0, +0.25)")
    parser.add_argument("--total", type=float, required=True, help="Total goals line (e.g. 2.5)")
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Pretty-print structured JSON output",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    inp = MatchInput(
        home_odds=args.home,
        draw_odds=args.draw,
        away_odds=args.away,
        asian_handicap=args.ah,
        total_goals=args.total,
    )

    output = run(inp)

    if args.json:
        print(output.to_json())
    else:
        print(output)


if __name__ == "__main__":
    main()
