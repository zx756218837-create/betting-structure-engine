"""Streamlit web interface for the Betting Structure Engine."""

from __future__ import annotations

import streamlit as st
from engine import analyze_match  # noqa: E402  — runs standalone, not as package

st.set_page_config(page_title="盘口结构分析系统", page_icon="⚽", layout="centered")

st.title("⚽ 盘口结构分析系统 v10")
st.caption("学术建模用途 — 非投注建议")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    home = st.number_input("主胜赔率", value=1.9, format="%.2f")
with col2:
    draw = st.number_input("平局赔率", value=3.2, format="%.2f")
with col3:
    away = st.number_input("客胜赔率", value=4.0, format="%.2f")

col4, col5 = st.columns(2)
with col4:
    ah = st.number_input("亚洲让球", value=0.0, format="%.2f")
with col5:
    total = st.number_input("大小球", value=2.5, format="%.1f")

if st.button("开始分析", use_container_width=True):
    result = analyze_match({
        "home_odds": home,
        "draw_odds": draw,
        "away_odds": away,
        "asian_handicap": ah,
        "total_goals": total,
    })

    st.subheader("📊 分析结果")

    st.markdown(f"**结构类型**: {result['structure']}")
    st.markdown(f"**比分概率**:")
    for score, prob in result["score_probs"].items():
        st.markdown(f"  - {score}: {prob:.2%}")
    st.markdown(f"**点球风险**: {result['penalty_risk']:.2%}")
    st.markdown(f"**套利信号**: {result['arbitrage']}")
    st.markdown(f"**风险等级**: {result['risk']}")

    st.divider()
    st.json(result, expanded=False)
