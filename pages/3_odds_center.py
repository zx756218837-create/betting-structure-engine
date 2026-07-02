"""Odds Center — view generated odds and market data."""

from __future__ import annotations

import streamlit as st
import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)
    sys.path.insert(0, os.path.join(_package_root, ".."))

from data.odds import OddsProvider
from data.asian import AsianHandicapProvider
from data.over_under import OverUnderProvider
from config.settings import Settings

settings = Settings()

st.set_page_config(page_title="赔率中心", page_icon="🎰", layout="wide")

st.title("🎰 赔率中心")
st.caption("Market data overview")

home_team = st.text_input("主队", value="France")
away_team = st.text_input("客队", value="Brazil")

if st.button("加载赔率数据", use_container_width=True):
    odds_p = OddsProvider(settings.known_teams, settings.team_tiers)
    ah_p = AsianHandicapProvider(settings.known_teams)
    ou_p = OverUnderProvider(settings.known_teams)

    current = odds_p.get_current(home_team, away_team)
    ah = ah_p.get_line(home_team, away_team)
    ou = ou_p.get_line(home_team, away_team)

    st.divider()
    st.markdown("### 当前赔率")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("主胜", f"{current['home_odds']:.2f}")
    c2.metric("平局", f"{current['draw_odds']:.2f}")
    c3.metric("客胜", f"{current['away_odds']:.2f}")
    c4.metric("让球", f"{current['asian_handicap']:+.1f}")
    c5.metric("大小球", f"{current['total_goals']:.1f}")

    st.divider()
    st.markdown("### 亚盘详情")
    st.json(ah, expanded=False)

    st.divider()
    st.markdown("### 大小球详情")
    st.json(ou, expanded=False)
