"""Betting Structure Engine v10 — academic market classification."""

from .engine import run, analyze_match, analyze_match_from_teams
from .models import MatchInput, EngineOutput, MatchStructure, ArbitrageSignal, RiskLevel
from .odds_provider import generate_odds, get_odds_snapshot
from .team_strength import get_strength_score, get_team_info

__all__ = [
    "run",
    "analyze_match",
    "analyze_match_from_teams",
    "generate_odds",
    "get_odds_snapshot",
    "MatchInput",
    "EngineOutput",
    "MatchStructure",
    "ArbitrageSignal",
    "RiskLevel",
    "get_strength_score",
    "get_team_info",
]

__version__ = "10.0.0"
