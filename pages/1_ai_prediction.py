"""AI Prediction page — advanced AI-powered match analysis."""

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

st.set_page_config(page_title="AI 预测", page_icon="🤖", layout="wide")

st.title("🤖 AI 预测引擎")
st.caption("Advanced AI-powered match analysis with confidence scoring")

col1, col2 = st.columns(2)
with col1:
    home_team = st.text_input("主队", value="France")
with col2:
    away_team = st.text_input("客队", value="Brazil")

if st.button("运行 AI 预测", use_container_width=True):
    predictor = Predictor()
    with st.spinner("Running AI prediction..."):
        result = predictor.predict(home_team, away_team)

    st.divider()

    # Win/Draw/Lose
    st.markdown("### 📊 胜平负概率")
    c1, c2, c3 = st.columns(3)
    c1.metric("主胜", f"{result['win_prob']:.1%}")
    c2.metric("平局", f"{result['draw_prob']:.1%}")
    c3.metric("客胜", f"{result['lose_prob']:.1%}")

    # Top 5 scores
    st.markdown("### 🎯 Top 5 比分")
    scores = result["top_5_scores"]
    cols = st.columns(len(scores))
    for i, s in enumerate(scores):
        cols[i].metric(s["score"], f"{s['probability']:.1%}")

    # Confidence
    st.markdown("### 🧠 置信度")
    conf = result["confidence_score"]
    st.progress(conf)
    st.markdown(f"得分: **{conf:.0%}**")

    # Cold alert
    st.markdown("### ⚠️ 警报")
    ca = result["cold_alert"]
    if ca["cold"]:
        st.warning(ca["message"])
    else:
        st.success(ca["message"])

    # Recommended pick
    st.markdown("### 💡 推荐")
    st.info(result["recommended_pick"])

    # BTTS & OU
    st.markdown("### 📈 附加指标")
    bt1, bt2 = st.columns(2)
    with bt1:
        bt = result["btts"]
        st.metric("BTTS 是", f"{bt['btts_yes']:.1%}")
    with bt2:
        ou = result["over_under"]
        st.metric(f"Over {ou['line']}", f"{ou['over']:.1%}")

    # Realtime simulation
    st.divider()
    st.markdown("### 📡 实时模拟")
    rt = RealtimePredictor(result)
    tick = st.slider("模拟 Tick", 0, 20, 5)
    for _ in range(tick):
        rt.simulate_update(_)
    latest = rt.latest()
    if latest:
        st.json(latest, expanded=False)
