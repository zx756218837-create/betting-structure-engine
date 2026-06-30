"""Betting Structure Engine v10 — academic market classification."""

from .engine import run
from .models import MatchInput, EngineOutput, MatchStructure, ArbitrageSignal, RiskLevel

__all__ = [
    "run",
    "MatchInput",
    "EngineOutput",
    "MatchStructure",
    "ArbitrageSignal",
    "RiskLevel",
]

__version__ = "10.0.0"
