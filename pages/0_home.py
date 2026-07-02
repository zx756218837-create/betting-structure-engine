"""Home page — main prediction interface."""

from __future__ import annotations

import streamlit as st
import sys
import os

# Standalone import support for Streamlit Cloud
_package_root = os.path.dirname(os.path.abspath(__file__))
if _package_root not in sys.path:
    sys.path.insert(0, _package_root)
    sys.path.insert(0, os.path.join(_package_root, ".."))

from ai.predictor import Predictor
from engine import analyze_match, analyze_match_from_teams
from utils.helpers import format_odds, format_prob, format_pick

st.set_page_config(page_title="盘口结构分析系统", page_icon="⚽", layout="wide")

st.title("⚽ 盘口结构分析系统 v3.3")
st.caption("Professional Edition — Academic Market Classification")

# --- Mode selector ---
mode = st.radio(
    "分析模式",
    ["按球队名称分析 (AI)", "手动输入赔率"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "按球队名称分析 (AI)":
    st.subheader("输入对阵双方")
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.text_input("主队", value="France", placeholder="例: France")
    with col2:
        away_team = st.text_input("客队", value="Brazil", placeholder="例: Brazil")

    if st.button("开始预测", use_container_width=True) and home_team and away_team:
        predictor = Predictor()
        with st.spinner("正在分析..."):
            result = predictor.predict(home_team, away_team)

        # --- Win/Draw/Lose probabilities ---
        st.markdown("### 📊 胜平负概率")
        c1, c2, c3 = st.columns(3)
        c1.metric("主胜", format_prob(result["win_prob"]))
        c2.metric("平局", format_prob(result["draw_prob"]))
        c3.metric("客胜", format_prob(result["lose_prob"]))

        # --- Top 5 Scores ---
        st.markdown("### 🎯 前5比分预测")
        scores = result["top_5_scores"]
        cols = st.columns(len(scores))
        for i, s in enumerate(scores):
            cols[i].metric(s["score"], format_prob(s["probability"]))

        # --- Confidence & Alert ---
        st.markdown("### 🧠 置信度与警报")
        ac1, ac2 = st.columns(2)
        with ac1:
            conf = result["confidence_score"]
            bar_color = "🟢" if conf >= 0.5 else "🟡" if conf >= 0.35 else "🔴"
            st.metric("置信度", f"{conf:.0%}")
            st.progress(conf)
        with ac2:
            ca = result["cold_alert"]
            st.markdown(f"**警报**: {ca['message']}")
            if ca["cold"]:
                st.warning("冷信号 — 低置信度")
            else:
                st.success("热信号 — 高置信度")

        # --- Recommended Pick ---
        st.markdown("### 💡 推荐选项")
        pick = result["recommended_pick"]
        st.info(format_pick(pick))

        # --- BTTS & Over/Under ---
        st.markdown("### 📈 附加指标")
        bt1, bt2 = st.columns(2)
        with bt1:
            bt = result["btts"]
            st.metric("BTTS 是", format_prob(bt["btts_yes"]))
            st.caption(f"否: {format_prob(bt['btts_no'])}")
        with bt2:
            ou = result["over_under"]
            st.metric(f"Over {ou['line']}", format_prob(ou["over"]))
            st.caption(f"Under: {format_prob(ou['under'])}")

        # --- Legacy fields ---
        st.divider()
        st.markdown("### 🔬 核心分析")
        l1, l2, l3, l4 = st.columns(4)
        l1.metric("结构类型", result["structure"])
        l2.metric("点球风险", format_prob(result["penalty_risk"]))
        l3.metric("套利信号", result["arbitrage"])
        l4.metric("风险等级", result["risk"])

        # --- Generated odds ---
        st.divider()
        st.markdown("### 🎰 生成赔率")
        od = result["generated_odds"]
        o1, o2, o3, o4, o5 = st.columns(5)
        o1.metric("主胜", format_odds(od["home_odds"]))
        o2.metric("平局", format_odds(od["draw_odds"]))
        o3.metric("客胜", format_odds(od["away_odds"]))
        o4.metric("让球", f"{od['asian_handicap']:+.1f}")
        o5.metric("大小球", f"{od['total_goals']:.1f}")

        # --- Full JSON ---
        with st.expander("📋 完整结果"):
            st.json(result, expanded=False)

else:
    # --- Manual odds mode (backward compatible) ---
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
        st.markdown("### 📊 分析结果")
        st.markdown(f"**结构类型**: {result['structure']}")
        st.markdown("**比分概率**:")
        for score, prob in result["score_probs"].items():
            st.markdown(f"  - {score}: {prob:.2%}")
        st.markdown(f"**点球风险**: {result['penalty_risk']:.2%}")
        st.markdown(f"**套利信号**: {result['arbitrage']}")
        st.markdown(f"**风险等级**: {result['risk']}")

        st.divider()
        st.json(result, expanded=False)
