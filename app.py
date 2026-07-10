import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Minimal Workspace", page_icon="💼", layout="wide")

if "todos" not in st.session_state:
    st.session_state.todos = [{"task": "📄 閱讀專案報告", "done": False}]
if "notes" not in st.session_state:
    st.session_state.notes = ""

st.markdown("# 💼 高效個人工作台")
st.caption(f"今天是 {datetime.now().strftime('%Y-%m-%d')} │ 專注當下。")
st.markdown("---")

col_left, col_right = st.columns([7, 3], gap="large")

with col_left:
    st.markdown("### 📝 今日待辦事項")
    with st.form("todo_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            new_todo = st.text_input("", placeholder="準備下午的簡報...", label_visibility="collapsed")
        with col_btn:
            submit_todo = st.form_submit_button("新增", use_container_width=True)
        if submit_todo and new_todo.strip():
            st.session_state.todos.append({"task": new_todo.strip(), "done": False})
            st.rerun()

    if st.session_state.todos:
        updated_todos = []
        for i, todo in enumerate(st.session_state.todos):
            col_check, col_text = st.columns([1, 25])
            with col_check:
                is_done = st.checkbox("", value=todo["done"], key=f"todo_{i}")
            with col_text:
                if is_done:
                    st.markdown(f"~~{todo['task']}~~")
                else:
                    st.markdown(f"**{todo['task']}**")
            updated_todos.append({"task": todo["task"], "done": is_done})
        st.session_state.todos = updated_todos

    if st.button("🧹 清除已完成事項"):
        st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]
        st.rerun()

with col_right:
    st.markdown("### ⏱️ 專注計時器")
    if st.button("⏱️ 開始 25 分鐘專注", use_container_width=True, type="primary"):
        bar = st.progress(0, text="專注中...")
        for p in range(100):
            time.sleep(0.1)
            bar.progress(p + 1, text="專注中...")
        st.balloons()
        st.success("🎉 結束！休息一下吧！")
        
    st.markdown("---")
    st.markdown("### 📓 隨手便利貼")
    memo = st.text_area("寫點什麼...", value=st.session_state.notes, height=200, label_visibility="collapsed")
    st.session_state.notes = memo
