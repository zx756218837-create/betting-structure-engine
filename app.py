"""Streamlit web interface for the Betting Structure Engine v3.3.

This file is kept for backward compatibility.  The preferred entry point
is now the multi-page app under ``pages/``.  Run with:

    streamlit run app.py         # legacy single-page mode
    streamlit run pages/0_home.py # multi-page mode (preferred)
"""

from __future__ import annotations

import streamlit as st
import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)

from engine import analyze_match, analyze_match_from_teams  # noqa: E402

st.set_page_config(page_title="盘口结构分析系统", page_icon="⚽", layout="centered")

st.title("⚽ 盘口结构分析系统 v3.3")
st.caption("Professional Edition — 学术建模用途 — 非投注建议")

st.divider()

# --- Mode selector ---
mode = st.radio(
    "选择分析模式",
    ["按球队名称分析 (推荐)", "手动输入赔率"],
    horizontal=True,
)

if mode == "按球队名称分析 (推荐)":
    st.subheader("输入对阵双方")
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.text_input("主队", value="France", placeholder="例: France")
    with col2:
        away_team = st.text_input("客队", value="Brazil", placeholder="例: Brazil")

    if st.button("开始分析", use_container_width=True) and home_team and away_team:
        result = analyze_match_from_teams(home_team, away_team)

        st.divider()
        st.subheader("📊 分析结果")

        st.markdown("### 🎰 生成的赔率数据")
        od = result["generated_odds"]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("主胜", f"{od['home_odds']:.2f}")
        c2.metric("平局", f"{od['draw_odds']:.2f}")
        c3.metric("客胜", f"{od['away_odds']:.2f}")
        c4.metric("让球", f"{od['asian_handicap']:+.1f}")
        c5.metric("大小球", f"{od['total_goals']:.1f}")

        st.markdown("### 💪 球队实力对比")
        sd = result["strength_data"]
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f"**{home_team}**")
            st.progress(sd["home"]["score"] / 100)
            st.caption(f"评分: {sd['home']['score']} | 档次: {sd['home']['tier']}")
        with sc2:
            st.markdown(f"**{away_team}**")
            st.progress(sd["away"]["score"] / 100)
            st.caption(f"评分: {sd['away']['score']} | 档次: {sd['away']['tier']}")

        st.divider()
        st.markdown("### 🔬 核心分析")
        st.markdown(f"**结构类型**: {result['structure']}")
        st.markdown("**比分概率**:")
        for score, prob in result["score_probs"].items():
            st.markdown(f"  - {score}: {prob:.2%}")
        st.markdown(f"**点球风险**: {result['penalty_risk']:.2%}")
        st.markdown(f"**套利信号**: {result['arbitrage']}")
        st.markdown(f"**风险等级**: {result['risk']}")

        st.divider()
        st.json(result, expanded=False)

else:
    # --- OLD: manual odds input ---
    st.subheader("手动输入赔率")
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

        st.divider()
        st.subheader("📊 分析结果")
        st.markdown(f"**结构类型**: {result['structure']}")
        st.markdown("**比分概率**:")
        for score, prob in result["score_probs"].items():
            st.markdown(f"  - {score}: {prob:.2%}")
        st.markdown(f"**点球风险**: {result['penalty_risk']:.2%}")
        st.markdown(f"**套利信号**: {result['arbitrage']}")
        st.markdown(f"**风险等级**: {result['risk']}")

        st.divider()
        st.json(result, expanded=False)
