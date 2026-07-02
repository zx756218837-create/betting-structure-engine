"""Betting Structure Engine v3.3 Professional Edition."""

from .engine import run, analyze_match, analyze_match_from_teams
from .models import MatchInput, EngineOutput, MatchStructure, ArbitrageSignal, RiskLevel
from .odds_provider import generate_odds, get_odds_snapshot
from .team_strength import get_strength_score, get_team_info
from .ai.predictor import Predictor
from .ai.score_model import ScoreModel
from .ai.probability_model import ProbabilityModel
from .ai.confidence import ConfidenceModel
from .ai.learning import LearningModel
from .ai.realtime import RealtimePredictor

__all__ = [
    # Core
    "run",
    "analyze_match",
    "analyze_match_from_teams",
    "MatchInput",
    "EngineOutput",
    "MatchStructure",
    "ArbitrageSignal",
    "RiskLevel",
    # Odds / Strength
    "generate_odds",
    "get_odds_snapshot",
    "get_strength_score",
    "get_team_info",
    # AI
    "Predictor",
    "ScoreModel",
    "ProbabilityModel",
    "ConfidenceModel",
    "LearningModel",
    "RealtimePredictor",
]

__version__ = "3.3.0"
