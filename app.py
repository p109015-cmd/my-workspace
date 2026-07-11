import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import feedparser
import os
from datetime import datetime

# ==========================================
# 0. 基礎設定與持久化檔案初始化
# ==========================================
st.set_page_config(
    page_title="Hacker Workstation v2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTE_FILE = "sticky_notes.txt"
KB_FILE = "my_knowledge_base.md"

if not os.path.exists(NOTE_FILE):
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write("這是你的閃電收件匣，隨手記下你的靈感...")

if not os.path.exists(KB_FILE):
    with open(KB_FILE, "w", encoding="utf-8") as f:
        f.write("# 知識管理庫 (PARA)\n\n在這裡建立你的深度第二大腦。")

# ==========================================
# 1. 外部 API 快取與擷取（天氣與新聞）
# ==========================================
@st.cache_data(ttl=600)  # 快取10分鐘，避免被 wttr.in 封鎖 IP
def get_weather():
    try:
        # 抓取雲林古坑天氣資訊
        response = requests.get("https://wttr.in/Gukeng?format=%c+%t+%h+%w", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception:
        pass
    return "⛅ 無法取得即時天氣資訊"

@st.cache_data(ttl=600)  # 快取10分鐘，加快網頁載入
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
    
    # 駭客矩陣雙模切換
    ui_mode = st.radio(
        "切換工作台模式 (或按 F1 鍵)",
        ["正常模式 (Normal)", "駭客模式 (Hacker)"],
        index=0,
        key="ui_mode_select"
    )
    is_hacker = "Hacker" in ui_mode

    st.markdown("---")
    st.subheader("📊 個人能力指標設定")
    val_coding = st.slider("Coding 輸出率", 0, 100, 85)
    val_focus = st.slider("心流專注度", 0, 100, 90)
    val_learn = st.slider("知識內化率", 0, 100, 75)
    val_energy = st.slider("精力續航力", 0, 100, 80)
    val_delivery = st.slider("專案交付率", 0, 100, 95)

# ==========================================
# 3. 駭客模式 全域 CSS 與 F1 JS 注入
# ==========================================
if is_hacker:
    # 注入全暗黑螢光綠 CSS
    st.markdown("""
        <style>
        /* 全域背景與文字顏色變更 */
        .stApp {
            background-color: #0d0d0d !important;
            color: #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        /* 側邊欄黑化 */
        [data-testid="stSidebar"] {
            background-color: #1a1a1a !important;
            color: #00ff66 !important;
            border-right: 1px solid #00ff66;
        }
        /* Bento Grid 卡片黑化與綠色邊框 */
        [data-testid="stMetric"] {
            background-color: #111111 !important;
            border: 1px solid #00ff66 !important;
            border-radius: 8px;
            padding: 10px;
        }
        div[data-testid="stContainer"] {
            border: 1px solid #00ff66 !important;
            background-color: #111111 !important;
            color: #00ff66 !important;
        }
        /* 輸入框黑化 */
        textarea, input {
            background-color: #151515 !important;
            color: #00ff66 !important;
            border: 1px solid #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        /* 按鈕駭客化 */
        button[data-testid="baseButton-secondary"] {
            background-color: #00ff66 !important;
            color: #000000 !important;
            border: 1px solid #00ff66 !important;
            font-weight: bold !important;
        }
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #00cc52 !important;
            color: #000000 !important;
        }
        /* 各種元件顏色修正 */
        p, li, h1, h2, h3, h4, h5, h6, span, label {
            color: #00ff66 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# 注入 JavaScript 監聽 F1 按鍵
st.components.v1.html("""
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'F1') {
            e.preventDefault(); // 阻擋瀏覽器預設說明視窗
            
            // 尋找 Streamlit 側邊欄的 Radio Options
            const radios = doc.querySelectorAll('input[name="ui_mode_select"]');
            if (radios.length >= 2) {
                // 找出目前哪個被選中，並切換到另一個
                if (radios[0].checked) {
                    radios[1].click();
                } else {
                    radios[0].click();
                }
            }
        }
    });
    </script>
""", height=0)

# ==========================================
# 4. 主畫面排版 (Main UI Layout)
# ==========================================
st.title("⚡ 高效個人工作台")
st.caption(f"系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 雙模完全體穩定版")

# 第一層：即時情報 Bento Grid (天氣與焦點新聞)
col_info1, col_info2 = st.columns([1, 2])

with col_info1:
    with st.container(border=True):
        st.subheader("📍 即時環境 (雲林古坑)")
        weather_info = get_weather()
        st.metric(label="wttr.in 觀測數據", value=weather_info)

with col_info2:
    with st.container(border=True):
        st.subheader("📰 今日焦點新聞 (Google News)")
        news_list = get_google_news()
        if news_list:
            for i, news in enumerate(news_list, 1):
                st.markdown(f"{i}. [{news['title']}]({news['link']})")
        else:
            st.write("暫時無法載入新聞。")

st.write("") # 間隔

# 第二層：核心工作區 (雙欄排版)
col_left, col_right = st.columns([3, 2])

# --- 左側欄：輸入與處理端 (各自獨立為 Fragment，打字不干擾全局) ---
with col_left:
    
    # 閃電便利貼 Fragment
    @st.fragment
    def render_sticky_notes():
        with st.container(border=True):
            st.subheader("⚡ 閃電收件匣 (Capture)")
            with open(NOTE_FILE, "r", encoding="utf-8") as f:
                current_notes = f.read()
            
            user_notes = st.text_area(
                "隨手記下目前的雜念、任務、待辦，稍後再行 PARA 整理：",
                value=current_notes,
                height=150,
                key="sticky_notes_input"
            )
            
            if st.button("💾 儲存隨身筆記", key="save_notes_btn"):
                with open(NOTE_FILE, "w", encoding="utf-8") as f:
                    f.write(user_notes)
                st.toast("隨身便利貼已安全寫入本地端檔案！", icon="💾")

    # 知識管理庫 Fragment
    @st.fragment
    def render_knowledge_base():
        with st.container(border=True):
            st.subheader("🧠 深度第二大腦 (Knowledge Base)")
            with open(KB_FILE, "r", encoding="utf-8") as f:
                current_kb = f.read()
            
            user_kb = st.text_area(
                "編輯你的 Markdown 知識庫內容：",
                value=current_kb,
                height=250,
                key="kb_input"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💾 更新知識庫", key="save_kb_btn"):
                    with open(KB_FILE, "w", encoding="utf-8") as f:
                        f.write(user_kb)
                    st.toast("知識庫 Markdown 檔案已成功更新！", icon="🧠")
            
            with col_right:
                pass # 留空
            
            st.markdown("---")
            st.markdown("**📄 當前知識庫預覽：**")
            st.markdown(user_kb)

    # 執行渲染
    render_sticky_notes()
    st.write("")
    render_knowledge_base()

# --- 右側欄：輸出與監控端 (雷達圖與日誌流) ---
with col_right:
    
    # Bento Grid: 數據化雷達圖卡片
    with st.container(border=True):
        st.subheader("🎯 心流狀態即時分析")
        
        # 準備雷達圖數據
        categories = ['Coding 輸出率', '心流專注度', '知識內化率', '精力續航力', '專案交付率']
        values = [val_coding, val_focus, val_learn, val_energy, val_delivery]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='當前狀態',
            line=dict(color='#00ff66' if is_hacker else '#FF4B4B', width=2),
            fillcolor='rgba(0, 255, 102, 0.2)' if is_hacker else 'rgba(255, 75, 75, 0.2)'
        ))
        
        # 依據模式動態調整 Plotly 樣式
        radar_theme = dict(
            bgcolor='#111111' if is_hacker else '#ffffff',
            gridcolor='#004411' if is_hacker else '#E5E5E5',
            linecolor='#00ff66' if is_hacker else '#E5E5E5',
            font=dict(
                color='#00ff66' if is_hacker else '#31333F',
                family='Courier New' if is_hacker else 'Arial',
                size=12
            )
        )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor=radar_theme['gridcolor'], linecolor=radar_theme['linecolor']),
                angularaxis=dict(gridcolor=radar_theme['gridcolor'], linecolor=radar_theme['linecolor']),
                bgcolor=radar_theme['bgcolor']
            ),
            showlegend=False,
            paper_bgcolor=radar_theme['bgcolor'],
            font=radar_theme['font'],
            margin=dict(l=40, r=40, t=40, b=40),
            height=320
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Bento Grid: 實時日誌流 (Log Stream)
    with st.container(border=True):
        st.subheader("📟 系統事件日誌流 (Execute)")
        
        log_time = datetime.now().strftime('%H:%M:%S')
        mode_tag = "[CRITICAL_HACKER_MODE]" if is_hacker else "[NORMAL_WORK_MODE]"
        
        logs = [
            f"[{log_time}] {mode_tag} 心流狀態儀表板已成功掛載。",
            f"[{log_time}] [IO_SERVER] 讀取 sticky_notes.txt 與 my_knowledge_base.md 完畢。",
            f"[{log_time}] [NETWORK] wttr.in 天氣與 Google News RSS 解析完畢 (Cache Active)。",
            f"[{log_time}] [JS_KERNEL] F1 鍵盤雙模切換接尾監聽器已就緒。"
        ]
        
        # 駭客模式下用程式碼區塊展現極客感
        if is_hacker:
            log_text = "\n".join(logs)
            st.code(log_text, language="bash")
        else:
            for log in logs:
                st.info(log)
