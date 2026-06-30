"""Engine — orchestrator that wires all modules together.

This is the public API surface: call ``run()`` with a ``MatchInput``
and get back a fully populated ``EngineOutput``.
"""

from __future__ import annotations

from .models import MatchInput, EngineOutput
from .classifier import classify
from .probability import compute_score_probs
from .risk import estimate_penalty_risk, map_risk_level
from .arbitrage import detect_edge


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
    from .models import MatchInput

    inp = MatchInput.from_dict(data)
    result = run(inp)
    return result.to_dict()
