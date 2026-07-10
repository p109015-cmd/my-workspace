import streamlit as st
import requests
import feedparser
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. 頁面核心配置
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="多維度個人工作台", 
    page_icon="🧠"
)

# ==========================================
# 2. 雙模式 CSS 注入 (動態切換)
# ==========================================
# 初始化模式狀態
if "workspace_mode" not in st.session_state:
    st.session_state.workspace_mode = "正常模式 📊"

# 駭客模式專用 CSS 樣式
HACKER_CSS = """
<style>
    /* 全域暗色調與綠字 */
    .stApp {
        background-color: #0d0d0d !important;
        color: #00FF00 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #00FF00 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    /* 駭客控制台日誌樣式 */
    .hacker-box {
        font-family: 'Courier New', Courier, monospace !important;
        color: #00FF00 !important;
        background-color: #000000 !important;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 5px;
        font-size: 0.85rem;
        border-left: 3px solid #00AA00;
        border: 1px solid #00FF00;
        box-shadow: 0 0 5px #00FF00;
    }
</style>
"""

# 如果切換到駭客模式，就注入綠色矩陣風格，否則保持 Streamlit 原生簡潔風
if st.session_state.workspace_mode == "駭客模式 ⚡":
    st.markdown(HACKER_CSS, unsafe_allow_html=True)

# ==========================================
# 3. 資料與狀態初始化
# ==========================================
STICKY_FILE = "sticky_notes.txt"

if not os.path.exists(STICKY_FILE):
    with open(STICKY_FILE, "w", encoding="utf-8") as f:
        f.write("💡 系統就緒。\n📌 在此紀錄今日臨時便利貼，關閉網頁亦可留存。")

if "sticky_notes" not in st.session_state:
    with open(STICKY_FILE, "r", encoding="utf-8") as f:
        st.session_state.sticky_notes = f.read()

# 駭客日誌追蹤
if "hacker_logs" not in st.session_state:
    st.session_state.hacker_logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] GRID_INIT // Matrix mode operational.",
        f"[{datetime.now().strftime('%H:%M:%S')}] SECURITY // Local node backup verified."
    ]

def add_log(action, level="INFO"):
    t = datetime.now().strftime('%H:%M:%S')
    st.session_state.hacker_logs.insert(0, f"[{t}] {level} // {action}")
    if len(st.session_state.hacker_logs) > 10:
        st.session_state.hacker_logs.pop()

# ==========================================
# 4. 數據抓取與雷達圖繪製
# ==========================================
def get_weather():
    try:
        response = requests.get("https://wttr.in/Yunlin?format=j1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            return {
                "temp": f"{current['temp_C']} °C", 
                "delta": f"體感 {current['FeelsLikeC']} °C", 
                "desc": current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value'], 
                "humidity": f"{current['humidity']}%"
            }
    except Exception:
        pass
    return {"temp": "無法取得", "delta": "--", "desc": "未知", "humidity": "--"}

def get_news():
    try:
        rss_url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        feed = feedparser.parse(rss_url)
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]
    except Exception:
        return [{"title": "新聞加載失敗。", "link": "#"}]

def draw_radar_chart():
    """繪製個人能力與專案進度雷達圖 (修復版)"""
    categories = ['專案執行力', '程式開發', '資訊吸收', '身心健康', '時間管理']
    values = [85, 90, 75, 80, 70]
    
    is_hacker = st.session_state.workspace_mode == "駭客模式 ⚡"
    line_color = '#00FF00' if is_hacker else '#FF4B4B'
    fill_color = 'rgba(0, 255, 0, 0.2)' if is_hacker else 'rgba(255, 75, 75, 0.2)'
    bg_color = '#000000' if is_hacker else 'rgba(0,0,0,0)'
    text_color = '#00FF00' if is_hacker else '#31333F'

    # 使用正確的 plotly.express (px) 建立
    fig = px.line_polar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        line_close=True
    )
    
    # 優化外觀
    fig.update_traces(fill='toself', fillcolor=fill_color, line_color=line_color)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#444444' if is_hacker else '#E5E5E5'),
            angularaxis=dict(gridcolor='#444444' if is_hacker else '#E5E5E5', tickfont=dict(color=text_color))
        ),
        showlegend=False,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=320,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

# ==========================================
# 5. 🎛️ 側邊欄控制中心
# ==========================================
with st.sidebar:
    st.subheader("⚙️ 工作台控制中心")
    
    selected_mode = st.radio(
        "切換工作台人格：",
        ["正常模式 📊", "駭客模式 ⚡"],
        index=0 if st.session_state.workspace_mode == "正常模式 📊" else 1
    )
    
    if selected_mode != st.session_state.workspace_mode:
        st.session_state.workspace_mode = selected_mode
        st.rerun()

    st.markdown("---")
    
    if st.session_state.workspace_mode == "正常模式 📊":
        st.markdown("📈 **今日個人狀態維度**")
        st.plotly_chart(draw_radar_chart(), use_container_width=True)
    else:
        st.markdown("💻 **MATRIX LOG STREAM**")
        for log in st.session_state.hacker_logs:
            st.markdown(f'<div class="hacker-box">{log}</div>', unsafe_allow_html=True)
        if st.button("🧹 PURGE LOGS", use_container_width=True):
            st.session_state.hacker_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] LOGS PURGED."]
            st.rerun()

# ==========================================
# 6. 主網頁排版渲染 (st.fragment 保持流暢)
# ==========================================
st.title("💼 我的高效個人工作台")
st.caption(f"📅 當前時間緯度：{datetime.now().strftime('%Y-%m-%d')} | 當前模式：{st.session_state.workspace_mode}")
st.markdown("---")

# 【上半部：情報站（天氣/新聞）】
@st.fragment
def render_info_station():
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("🌡️ ☀️ 即時天氣情報")
            weather = get_weather()
            st.metric(label=f"雲林古坑 ({weather['desc']})", value=weather['temp'], delta=weather['delta'])
            st.caption(f"💧 環境濕度：{weather['humidity']}")
            if st.button("🔄 刷新天氣", use_container_width=True):
                add_log("Synced geolocation environmental matrix.", "WEATHER")
                st.toast("天氣已更新")
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("🌐 📰 今日焦點新聞")
            news_items = get_news()
            for item in news_items:
                st.markdown(f"• [{item['title']}]({item['link']})")
            if st.button("🔄 刷新新聞", use_container_width=True):
                add_log("Intercepted public RSS data feed.", "NETWORK")
                st.toast("新聞已更新")
                st.rerun()

# 【下半部：核心工作區（便利貼/筆記）】
@st.fragment
def render_notes_system():
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("📝 📌 隨身便利貼")
            updated_sticky = st.text_area("貼紙內容", value=st.session_state.sticky_notes, height=180, label_visibility="collapsed")
            st.session_state.sticky_notes = updated_sticky
            if st.button("💾 儲存便利貼", type="primary", use_container_width=True):
                with open(STICKY_FILE, "w", encoding="utf-8") as f:
                    f.write(updated_sticky)
                add_log(f"Sector write successful to {STICKY_FILE}", "SECURITY")
                st.toast("便利貼已儲存！")
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("✍️ 📓 知識深度筆記")
            note_title = st.text_input("筆記標題", value=f"{datetime.now().strftime('%Y-%m-%d')} 工作日誌")
            long_note = st.text_area("內文 (支援 Markdown)", height=115, placeholder="在此輸入結構化思維...")
            if st.button("🚀 一鍵歸檔至本地知識庫 (.md)", use_container_width=True):
                if long_note.strip() != "":
                    with open("my_knowledge_base.md", "a", encoding="utf-8") as f:
                        f.write(f"\n\n## {note_title}\n* 📅 時間：{datetime.now().strftime('%H:%M:%S')}\n\n{long_note}")
                    add_log("Compiled Markdown segment into database matrix.", "KNOWLEDGE")
                    st.success("筆記已歸檔！")
                    st.rerun()

# 呼叫渲染
render_info_station()
st.markdown("<br>", unsafe_allow_html=True)
render_notes_system()
