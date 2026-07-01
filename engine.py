"""Engine — orchestrator that wires all modules together.

This is the public API surface: call ``run()`` with a ``MatchInput``
and get back a fully populated ``EngineOutput``.
"""

from __future__ import annotations

import sys
import os

# Support both: running as a package (CLI) and as a standalone script (Streamlit)
_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)

from models import MatchInput, EngineOutput
from classifier import classify
from probability import compute_score_probs
from risk import estimate_penalty_risk, map_risk_level
from arbitrage import detect_edge
from odds_provider import get_odds_snapshot


def run(inp: MatchInput) -> EngineOutput:
    """Execute the full analysis pipeline.

    Parameters
    ----------
    inp : MatchInput
        Raw odds snapshot.

    Returns
    -------
    EngineOutput
        Classified structure, score probabilities, penalty risk,
        arbitrage signal, and overall risk level.
    """
    structure = classify(inp)
    score_probs = compute_score_probs(structure)
    penalty_risk = estimate_penalty_risk(structure)
    risk_level = map_risk_level(penalty_risk, structure)
    arbitrage = detect_edge(structure, score_probs)

    return EngineOutput(
        structure=structure,
        score_probs=score_probs,
        penalty_risk=penalty_risk,
        arbitrage_signal=arbitrage,
        risk_level=risk_level,
    )


def analyze_match(data: dict) -> dict:
    """Streamlit-friendly entry point.

    Accepts a plain dict (e.g. from ``st.json`` or form inputs),
    runs the full pipeline, and returns a serialisable dict result.

    Parameters
    ----------
    data : dict
        Keys: ``home_odds``, ``draw_odds``, ``away_odds``,
        ``asian_handicap``, ``total_goals``.

    Returns
    -------
    dict
        Same shape as ``EngineOutput.to_dict()``.
    """
    inp = MatchInput.from_dict(data)
    result = run(inp)
    return result.to_dict()


def analyze_match_from_teams(home_team: str, away_team: str) -> dict:
    """Full pipeline from team names → structured analysis result.

    1. Generates realistic odds from team names (via odds_provider).
    2. Runs the existing classification / probability / risk / arbitrage pipeline.
    3. Returns a serialisable dict with all results.

    Parameters
    ----------
    home_team : str
        Name of the home team.
    away_team : str
        Name of the away team.

    Returns
    -------
    dict
        Contains ``generated_odds``, ``strength_data``, ``volatility``,
        ``mismatch_detection``, plus the standard engine output fields
        (``structure``, ``score_probs``, ``penalty_risk``, ``arbitrage``,
        ``risk``).
    """
    # Step 1 — generate odds
    snapshot = get_odds_snapshot(home_team, away_team)
    odds = snapshot["generated_odds"]

    # Step 2 — run existing pipeline
    inp = MatchInput(**{k: float(v) for k, v in odds.items()})
    result = run(inp)

    # Step 3 — merge everything
    output = result.to_dict()
    output["generated_odds"] = odds
    output["strength_data"] = {
        "home": snapshot["home_strength"],
        "away": snapshot["away_strength"],
    }
    output["volatility"] = snapshot["volatility"]
    output["mismatch_detection"] = snapshot["mismatch"]

    return output
