"""History page — view prediction history."""

from __future__ import annotations

import streamlit as st
import sys
import os
import json
import os as _os

_package_root = os.path.dirname(os.path.abspath(__file__))
root_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
history_dir = _os.path.join(root_dir, "history")

st.set_page_config(page_title="历史记录", page_icon="📜", layout="wide")

st.title("📜 历史记录")
st.caption("Saved prediction history")

# Load history files
history_files = []
if _os.path.isdir(history_dir):
    for f in _os.listdir(history_dir):
        if f.endswith(".json"):
            history_files.append(f)

if not history_files:
    st.info("暂无历史记录。在主页进行预测后会自动保存。")
else:
    history_files.sort(reverse=True)
    for hf in history_files[:10]:
        filepath = _os.path.join(history_dir, hf)
        with open(filepath, "r") as fh:
            try:
                data = json.load(fh)
                st.markdown(f"### {hf}")
                st.json(data, expanded=False)
                st.divider()
            except json.JSONDecodeError:
                st.error(f"无法解析 {hf}")
