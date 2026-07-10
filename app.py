import streamlit as st
import requests
import feedparser
import os
from datetime import datetime

st.set_page_config(layout="wide", page_title="我的高效個人工作台", page_icon="🚀")

# 確保本地有儲存便利貼的檔案
STICKY_FILE = "sticky_notes.txt"
if not os.path.exists(STICKY_FILE):
    with open(STICKY_FILE, "w", encoding="utf-8") as f:
        f.write("💡 歡迎使用全新工作台！\n📌 這是一張永久儲存的便利貼。")

# 將檔案內容讀入 Streamlit 記憶體
if "sticky_notes" not in st.session_state:
    with open(STICKY_FILE, "r", encoding="utf-8") as f:
        st.session_state.sticky_notes = f.read()

# --- 💡 核心功能函數 ---

# 1. 抓取即時天氣 (免 Key 爬取 wttr.in)
def get_weather():
    try:
        # 指定雲林古坑 (可自行修改，如 Taipei, Taichung 等)
        response = requests.get("https://wttr.in/Yunlin?format=j1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
            humidity = current['humidity']
            return {"temp": f"{temp} °C", "delta": f"體感 {feels_like} °C", "desc": desc, "humidity": f"濕度 {humidity}%"}
    except:
        pass
    return {"temp": "無法取得", "delta": "請檢查網路", "desc": "未明", "humidity": "--%"}

# 2. 抓取 Google 新聞 RSS
def get_news():
    try:
        # Google 新聞台灣焦點
        rss_url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        feed = feedparser.parse(rss_url)
        news_list = []
        for entry in feed.entries[:5]: # 只拿前 5 條最新焦點
            news_list.append({"title": entry.title, "link": entry.link})
        return news_list
    except:
        return [{"title": "新聞加載失敗，請稍後重試。", "link": "#"}]

# --- 🎯 畫面渲染 (運用 st.fragment 局部刷新) ---

st.title("💼 我的高效個人工作台")
st.caption(f"📅 今日日期：{datetime.now().strftime('%Y-%m-%d')}")
st.markdown("---")

# 區塊 A：即時情報站
@st.fragment
def render_info_station():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.subheader("☀️ 即時天氣情報", icon="🌡️")
            weather = get_weather()
            st.metric(label=f"目前位置：雲林 ({weather['desc']})", value=weather['temp'], delta=weather['delta'])
            st.caption(f"💧 環境濕度：{weather['humidity']}")
            if st.button("🔄 刷新天氣", use_container_width=True):
                st.toast("天氣數據已同步最新狀態！")

    with col2:
        with st.container(border=True):
            st.subheader("📰 今日焦點新聞 (Google News)", icon="🌐")
            news_items = get_news()
            for item in news_items:
                # 這裡過濾掉太長的標題，並提供超連結
                st.markdown(f"• [{item['title']}]({item['link']})")
            if st.button("🔄 刷新焦點新聞", use_container_width=True):
                st.toast("已拉取最新焦點新聞！")

# 區塊 B：筆記與便利貼
@st.fragment
def render_notes_system():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.subheader("📌 隨身便利貼", icon="📝")
            # 使用者輸入文字
            updated_sticky = st.text_area(
                "貼紙內容", 
                value=st.session_state.sticky_notes, 
                height=180,
                label_visibility="collapsed"
            )
            st.session_state.sticky_notes = updated_sticky
            
            # 點擊儲存，除了更新記憶體，也直接寫入硬碟文字檔！下次開機還在！
            if st.button("💾 儲存便利貼", type="primary", use_container_width=True):
                with open(STICKY_FILE, "w", encoding="utf-8") as f:
                    f.write(updated_sticky)
                st.toast("便利貼已永久儲存至硬碟！", icon="💾")

    with col2:
        with st.container(border=True):
            st.subheader("📓 知識深度筆記", icon="✍️")
            note_title = st.text_input("筆記標題", value=f"{datetime.now().strftime('%Y-%m-%d')} 工作日誌")
            long_note = st.text_area("內文 (支援 Markdown 語法)", height=115, placeholder="在這裡寫下今天學到了什麼，或是會議的詳細結論...")
            
            if st.button("🚀 一鍵歸檔至本地資料庫", use_container_width=True):
                # 這裡可以用 append 模式直接寫進一個大筆記檔（如同 Obsidian 的日記）
                with open("my_knowledge_base.md", "a", encoding="utf-8") as f:
                    f.write(f"\n\n## {note_title}\n* 建立時間：{datetime.now().strftime('%H:%M:%S')}\n{long_note}")
                st.success(f"成功！筆記已累積歸檔至 my_knowledge_base.md")

# 呼叫渲染
render_info_station()
st.markdown("<br>", unsafe_allow_html=True)
render_notes_system()
