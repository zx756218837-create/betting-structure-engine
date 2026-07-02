"""Utility helper functions."""

from __future__ import annotations


def format_odds(value: float) -> str:
    """Format decimal odds for display."""
    return f"{value:.2f}"


def format_prob(value: float) -> str:
    """Format probability as percentage string."""
    return f"{value:.1%}"


def format_pick(value: str) -> str:
    """Format pick label with emoji indicator."""
    mapping = {
        "HOME WIN": "🏠 Home Win",
        "DRAW": "🤝 Draw",
        "AWAY WIN": "✈️ Away Win",
        "NO BET — Insufficient signal": "⛔ No Bet",
    }
    return mapping.get(value, value)
