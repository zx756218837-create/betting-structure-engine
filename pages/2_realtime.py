"""Realtime Prediction page — streaming-style updates."""

from __future__ import annotations

import streamlit as st
import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)
    sys.path.insert(0, os.path.join(_package_root, ".."))

from ai.predictor import Predictor
from ai.realtime import RealtimePredictor

st.set_page_config(page_title="实时预测", page_icon="📡", layout="wide")

st.title("📡 实时预测")
st.caption("Simulated market movement tracking")

home_team = st.text_input("主队", value="France")
away_team = st.text_input("客队", value="Brazil")

if st.button("初始化", use_container_width=True):
    predictor = Predictor()
    result = predictor.predict(home_team, away_team)
    rt = RealtimePredictor(result)

    st.session_state["rt"] = rt
    st.session_state["base"] = result
    st.success("初始化完成")

rt = st.session_state.get("rt")
base = st.session_state.get("base")

if rt and base:
    st.divider()
    st.markdown("### 模拟市场变动")

    tick = st.slider("Tick 数", 0, 50, 10)
    cols = st.columns(4)
    for i in range(tick):
        rt.simulate_update(i)

    latest = rt.latest()
    if latest:
        c1, c2, c3, c4 = cols
        c1.metric("主胜", f"{latest.get('win_prob', base['win_prob']):.1%}")
        c2.metric("平局", f"{latest.get('draw_prob', base['draw_prob']):.1%}")
        c3.metric("客胜", f"{latest.get('lose_prob', base['lose_prob']):.1%}")
        c4.metric("Tick", tick)

    # Chart-like display of updates
    history = rt.history()
    if history:
        st.markdown("### 变动轨迹")
        for h in history[-10:]:
            st.caption(
                f"win={h.get('win_prob', 0):.4f} "
                f"draw={h.get('draw_prob', 0):.4f} "
                f"lose={h.get('lose_prob', 0):.4f}"
            )
