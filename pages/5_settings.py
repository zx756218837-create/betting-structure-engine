"""Settings page — configuration panel."""

from __future__ import annotations

import streamlit as st
import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)
    sys.path.insert(0, os.path.join(_package_root, ".."))

from config.settings import Settings

st.set_page_config(page_title="设置", page_icon="⚙️", layout="wide")

st.title("⚙️ 设置")

settings = Settings()

st.markdown("### 系统参数")
st.json({
    "bookmaker_margin": settings.bookmaker_margin,
    "logistic_scale": settings.logistic_scale,
    "draw_base_prob": settings.draw_base_prob,
    "version": "3.3 Professional",
})

st.divider()
st.markdown("### 球队层级")
st.json(settings.team_tiers)

st.divider()
st.markdown("### 已知球队数量")
st.caption(f"Elite: {sum(1 for v in settings.known_teams.values() if v == 'elite')}")
st.caption(f"Strong: {sum(1 for v in settings.known_teams.values() if v == 'strong')}")
st.caption(f"Medium: {sum(1 for v in settings.known_teams.values() if v == 'medium')}")
st.caption(f"Weak: {sum(1 for v in settings.known_teams.values() if v == 'weak')}")
st.caption(f"Very Weak: {sum(1 for v in settings.known_teams.values() if v == 'very_weak')}")
