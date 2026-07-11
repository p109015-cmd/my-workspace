import streamlit as st
import pandas as pd
import numpy as np
import requests
import feedparser
import os
import time
from datetime import datetime
import io

# ==========================================
# 0. 基礎設定與持久化檔案初始化
# ==========================================
st.set_page_config(
    page_title="Cyber Hacker Workstation v4.4",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTE_FILE = "sticky_notes.txt"
KB_FILE = "my_knowledge_base.md"
DOC_FILE = "cyber_document.md"

# 初始化檔案（強制將 Word/PPT 核心文本重置為空字串，確保畫面絕對乾淨）
if "doc_initialized" not in st.session_state:
    with open(DOC_FILE, "w", encoding="utf-8") as f:
        f.write("")
    st.session_state.doc_initialized = True

for file, default_content in [
    (NOTE_FILE, "隨手記下目前的雜念、任務、待辦..."),
    (KB_FILE, "# 知識管理庫 (PARA)\n\n在這裡建立你的深度第二大腦。")
]:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(default_content)

# 初始化 Session 狀態
if "hacker_simulator_unlocked" not in st.session_state:
    st.session_state.hacker_simulator_unlocked = False
if "ppt_page" not in st.session_state:
    st.session_state.ppt_page = 0
if "pomodoro_active" not in st.session_state:
    st.session_state.pomodoro_active = False

# ==========================================
# 1. 外部 API 快取與擷取
# ==========================================
@st.cache_data(ttl=600)
def get_formatted_weather():
    try:
        url = "https://wttr.in/Gukeng?m&lang=zh-tw&format=%c+氣溫+%t+/+濕度+%h++天氣(%C)"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "°C" in response.text:
            return response.text.strip()
    except Exception:
        pass
    return "⛅ 26°C / 86% 濕度 + 天氣(多雲/陰天)"

@st.cache_data(ttl=600)
def get_google_news():
    try:
        feed_url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        feed = feedparser.parse(feed_url)
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]
    except Exception:
        return []

# ==========================================
# 2. 側邊欄控制中心 (Sidebar Control)
# ==========================================
with st.sidebar:
    st.title("🎛️ 控制中心")
    
    ui_mode = st.radio(
        "切換工作台模式 (或按 F1 鍵)",
        ["正常模式 (Normal)", "駭客模式 (Hacker)"],
        index=0,
        key="ui_mode_select"
    )
    is_hacker = "Hacker" in ui_mode

    st.markdown("---")
    st.subheader("⏱️ 賽博脈衝番茄鐘")
    pomo_col1, pomo_col2 = st.columns(2)
    with pomo_col1:
        if st.button("🏁 啟動專注" if not st.session_state.pomodoro_active else "🛑 終止專注"):
            st.session_state.pomodoro_active = not st.session_state.pomodoro_active
    with pomo_col2:
        st.write("🟢 專注中..." if st.session_state.pomodoro_active else "⚪ 待命")
        
    if st.session_state.pomodoro_active:
        st.warning("[LOCK] 進入高強度心流專注狀態")

    st.markdown("---")
    st.subheader("📊 個人能力指標設定")
    val_coding = st.slider("Coding 輸出率", 0, 100, 85)
    val_focus = st.slider("心流專注度", 0, 100, 90)
    val_learn = st.slider("知識內化率", 0, 100, 75)
    val_energy = st.slider("精力續航力", 0, 100, 80)
    val_delivery = st.slider("專案交付率", 0, 100, 95)

radar_data = {"Coding": val_coding, "Focus": val_focus, "Learn": val_learn, "Energy": val_energy, "Delivery": val_delivery}

# ==========================================
# 3. 全域 CSS 強力黑化與 PPT 樣式優化
# ==========================================
hacker_css = ""
if is_hacker:
    hacker_css = """
        header[data-testid="stHeader"], [data-testid="stHeader"] { background-color: #0d0d0d !important; border-bottom: 1px solid #004411 !important; }
        header[data-testid="stHeader"] * { color: #00ff66 !important; fill: #00ff66 !important; }
        .stApp { background-color: #0d0d0d !important; color: #00ff66 !important; font-family: 'Courier New', monospace !important; }
        [data-testid="stSidebar"] { background-color: #1a1a1a !important; color: #00ff66 !important; border-right: 1px solid #00ff66; }
        [data-testid="stMetric"] { background-color: #111111 !important; border: 1px solid #00ff66 !important; border-radius: 8px; padding: 10px; }
        div[data-testid="stContainer"] { border: 1px solid #004411 !important; background-color: #111111 !important; color: #00ff66 !important; }
        textarea, input { background-color: #151515 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; }
        p, li, h1, h2, h3, h4, h5, h6, span, label { color: #00ff66 !important; }
        a { color: #88ccff !important; }
        
        div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button, div[data-testid="stDownloadButton"] a { 
            background-color: #000000 !important; 
            color: #00ff66 !important; 
            border: 1px solid #00ff66 !important; 
            font-weight: bold !important; 
            text-shadow: none !important;
        }
        div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { 
            background-color: #00ff66 !important; 
            color: #000000 !important; 
            box-shadow: 0 0 8px #00ff66 !important; 
        }
        
        div[data-testid="stNotification"], div[data-testid="stAlert"] { background-color: #000000 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; }
    """

ppt_box_bg = "#051a10" if is_hacker else "#f0f4f8"
ppt_box_border = "#00ff66" if is_hacker else "#0070f3"
ppt_text_color = "#00ff66" if is_hacker else "#333333"

st.markdown(f"""
<style>
{hacker_css}
.ppt-slide-box {{
    background-color: {ppt_box_bg};
    border: 2px dashed {ppt_box_border};
    border-radius: 12px;
    padding: 40px;
    min-height: 280px;
    color: {ppt_text_color};
    box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 前端多元鍵盤焦點監聽 (F1 鍵相容層)
# ==========================================
st.components.v1.html("""
    <script>
    const handleF1 = (e) => {
        if (e.key === 'F1') {
            e.preventDefault(); 
            const radios = window.parent.document.querySelectorAll('[data-testid="stSidebar"] input[type="radio"]');
            if (radios.length >= 2) {
                if (radios[0].checked) radios[1].click();
                else radios[0].click();
            }
        }
    };
    window.addEventListener('keydown', handleF1);
    window.parent.document.addEventListener('keydown', handleF1);
    </script>
""", height=0)

# ==========================================
# 5. 主畫面排版 (Main UI Layout)
# ==========================================
st.title("⚡ 高效率個人工作台 v4.4")
st.caption(f"系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 權限模式: {'🟢 高級特工終端' if is_hacker else '⚪ 一般日常終端'}")

# 第一層：即時情報 Bento Grid
col_info1, col_info2 = st.columns([1, 2])
with col_info1:
    with st.container(border=True):
        st.subheader("📍 即時環境 (雲林古坑)")
        st.info(get_formatted_weather())

with col_info2:
    with st.container(border=True):
        st.subheader("📰 今日焦點新聞 (Google News)")
        news_list = get_google_news()
        if news_list:
            for i, news in enumerate(news_list, 1):
                st.markdown(f"{i}. [{news['title']}]({news['link']})")

st.write("") 

# 第二層：核心工作區（左：文書與筆記 / 右：雷達與模擬器）
col_left, col_right = st.columns([3, 2])
