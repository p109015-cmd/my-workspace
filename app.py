import streamlit as st
import requests
import feedparser
import os
from datetime import datetime

# ==========================================
# 1. 頁面核心配置 (全寬模式 + 標題)
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="高效個人工作台", 
    page_icon="💼"
)

# ==========================================
# 2. 資料初始化與持久化設定
# ==========================================
STICKY_FILE = "sticky_notes.txt"

# 檢查本地是否有便利貼檔案，若無則初始化
if not os.path.exists(STICKY_FILE):
    with open(STICKY_FILE, "w", encoding="utf-8") as f:
        f.write("💡 歡迎使用全新升級的工作台！\n📌 這裡寫下的內容點擊儲存後會永久保留。")

# 將硬碟資料讀入 Streamlit 的 session_state 記憶體
if "sticky_notes" not in st.session_state:
    with open(STICKY_FILE, "r", encoding="utf-8") as f:
        st.session_state.sticky_notes = f.read()

# ==========================================
# 3. 核心 API 數據抓取函數
# ==========================================
def get_weather():
    """抓取即時天氣 (免 Key 爬取 wttr.in 數據)"""
    try:
        # 預設為雲林 (可依需求改為 Taipei, Taichung 等)
        response = requests.get("https://wttr.in/Yunlin?format=j1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
            humidity = current['humidity']
            return {
                "temp": f"{temp} °C", 
                "delta": f"體感 {feels_like} °C", 
                "desc": desc, 
                "humidity": f"濕度 {humidity}%"
            }
    except Exception:
        pass
    return {"temp": "無法取得", "delta": "請檢查網路", "desc": "未明", "humidity": "--%"}

def get_news():
    """抓取 Google 新聞台灣焦點 RSS"""
    try:
        rss_url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        feed = feedparser.parse(rss_url)
        news_list = []
        for entry in feed.entries[:5]:  # 僅精選前 5 條最新焦點
            news_list.append({"title": entry.title, "link": entry.link})
        return news_list
    except Exception:
        return [{"title": "📰 新聞加載失敗，請稍後點擊刷新重試。", "link": "#"}]

# ==========================================
# 4. 網頁前端排版渲染 (使用 st.fragment 避免全網頁刷新卡頓)
# ==========================================

# 主標題區
st.title("💼 我的高效個人工作台")
st.caption(f"📅 今日日期：{datetime.now().strftime('%Y-%m-%d')} | ⚡ 狀態：心流專注模式已就緒")
st.markdown("---")

# 【上半部：即時情報看板】
@st.fragment
def render_info_station():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.subheader("🌡️ ☀️ 即時天氣情報")
            weather = get_weather()
            st.metric(
                label=f"目前位置：雲林古坑 ({weather['desc']})", 
                value=weather['temp'], 
                delta=weather['delta']
            )
            st.caption(f"💧 當前環境濕度：{weather['humidity']}")
            if st.button("🔄 刷新即時天氣", use_container_width=True):
                st.toast("天氣數據已同步至最新狀態！")

    with col2:
        with st.container(border=True):
            st.subheader("🌐 📰 今日焦點新聞 (Google News)")
            news_items = get_news()
            for item in news_items:
                st.markdown(f"• [{item['title']}]({item['link']})")
            if st.button("🔄 刷新焦點新聞", use_container_width=True):
                st.toast("已成功拉取最新即時新聞摘要！")

# 【下半部：個人筆記與核心工作區】
@st.fragment
def render_notes_system():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.subheader("📝 📌 隨身便利貼")
            st.caption("放臨時碎屑記憶的地方，辦完即刪，無負擔。")
            
            # 文字輸入框（同步連動 session_state）
            updated_sticky = st.text_area(
                "貼紙內容", 
                value=st.session_state.sticky_notes, 
                height=180,
                label_visibility="collapsed"
            )
            st.session_state.sticky_notes = updated_sticky
            
            # 點擊儲存，除了更新記憶體，也直接寫入硬碟文字檔！下次開機還在！
            if st.button("💾 儲存臨時便利貼", type="primary", use_container_width=True):
                with open(STICKY_FILE, "w", encoding="utf-8") as f:
                    f.write(updated_sticky)
                st.toast("便利貼已永久儲存至硬碟！", icon="💾")

    with col2:
        with st.container(border=True):
            st.subheader("✍️ 📓 知識深度筆記")
            st.caption("用於撰寫今日工作日誌、會議紀錄或靈感延伸。")
            
            note_title = st.text_input("筆記標題", value=f"{datetime.now().strftime('%Y-%m-%d')} 工作日誌")
            long_note = st.text_area(
                "內文 (支援完整 Markdown 語法)", 
                height=115, 
                placeholder="在這裡寫下今天學到了什麼，或是會議的詳細結論..."
            )
            
            if st.button("🚀 一鍵歸檔至本地知識庫 (.md)", use_container_width=True):
                if long_note.strip() == "":
                    st.warning("內文空空的，請寫點東西再歸檔喔！")
                else:
                    # 使用 append (a) 模式，每次歸檔都會像日記一樣自動往下疊加
                    with open("my_knowledge_base.md", "a", encoding="utf-8") as f:
                        f.write(f"\n\n## {note_title}\n* 📅 建立時間：{datetime.now().strftime('%H:%M:%S')}\n\n{long_note}")
                    st.success(f"成功！該篇筆記已累積歸檔至專案目錄下的 `my_knowledge_base.md`！")

# ==========================================
# 5. 執行渲染
# ==========================================
render_info_station()
st.markdown("<br>", unsafe_allow_html=True)
render_notes_system()
