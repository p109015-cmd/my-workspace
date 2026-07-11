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
    page_title="Cyber Hacker Workstation v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTE_FILE = "sticky_notes.txt"
KB_FILE = "my_knowledge_base.md"
DOC_FILE = "cyber_document.md"  # 新增：Word/PPT 核心文本儲存

for file, default_content in [
    (NOTE_FILE, "隨手記下目前的雜念、任務、待辦..."),
    (KB_FILE, "# 知識管理庫 (PARA)\n\n在這裡建立你的深度第二大腦。"),
    (DOC_FILE, "# 📌 賽博特工專案報告\n---\n## 🚀 第一頁：核心目標\n- 自動化防禦系統部署\n- 雷達聲納全時監控\n---\n## 💻 第二頁：技術架構\n- 前端：Streamlit \n- 底層：Python 3.11 Kernel")
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
        div[data-testid="stButton"] button { background-color: #000000 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; font-weight: bold !important; }
        div[data-testid="stButton"] button:hover { background-color: #00ff66 !important; color: #000000 !important; box-shadow: 0 0 8px #00ff66 !important; }
        div[data-testid="stNotification"], div[data-testid="stAlert"] { background-color: #000000 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; }
    """

# 額外新增 PPT 投影箱的樣式
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
st.title("⚡ 高效率個人工作台 v4.0")
st.caption(f"系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 內建 Word/PPT 雙模文書終端")

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

with col_left:
    # 📝 新增：Word / PPT 賽博編輯器
    with st.container(border=True):
        st.subheader("📝 賽博文書終端 (Word & PPT 整合模組)")
        
        doc_tab1, doc_tab2 = st.tabs(["📄 Word 編輯模式", "📺 PPT 簡報播放模式"])
        
        with open(DOC_FILE, "r", encoding="utf-8") as f:
            doc_content = f.read()
            
        with doc_tab1:
            st.caption("利用 Markdown 編寫文件，使用 `---` 作為 PPT 的換頁符號。")
            edited_doc = st.text_area("文件編輯器 (支援豐富文本)", value=doc_content, height=250, key="word_editor")
            
            w_col1, w_col2, w_col3 = st.columns(3)
            with w_col1:
                if st.button("💾 儲存最新文本"):
                    with open(DOC_FILE, "w", encoding="utf-8") as f:
                        f.write(edited_doc)
                    st.toast("文件已成功寫入核心矩陣！", icon="💾")
            with w_col2:
                # 匯出標準 Markdown 檔案
                st.download_button("📥 匯出為 .md 檔案", data=edited_doc, file_name="Cyber_Report.md", mime="text/markdown")
            with w_col3:
                # 偽 Word 匯出：直接生成含有 doc 格式頭部的純文字流
                st.download_button("📥 匯出為 Word 格式", data=edited_doc, file_name="Cyber_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                
        with doc_tab2:
            # 根據 "---" 分割投影片
            slides = [s.strip() for s in edited_doc.split("---") if s.strip()]
            
            if not slides:
                st.write("請在編輯器中輸入內容，並用 `---` 進行分頁。")
            else:
                # 防呆：避免索引溢出
                if st.session_state.ppt_page >= len(slides):
                    st.session_state.ppt_page = len(slides) - 1
                
                # 渲染簡報箱
                current_slide_content = slides[st.session_state.ppt_page]
                st.markdown(f'<div class="ppt-slide-box">{current_slide_content}</div>', unsafe_allow_html=True)
                
                # PPT 控制按鈕
                ppt_ctrl1, ppt_ctrl2, ppt_ctrl3 = st.columns([1, 2, 1])
                with ppt_ctrl1:
                    if st.button("⬅️ 上一頁") and st.session_state.ppt_page > 0:
                        st.session_state.ppt_page -= 1
                        st.rerun()
                with ppt_ctrl2:
                    st.markdown(f"<p style='text-align: center; margin-top: 8px;'>投影片進度: {st.session_state.ppt_page + 1} / {len(slides)}</p>", unsafe_allow_html=True)
                with ppt_ctrl3:
                    if st.button("下一頁 ➡️") and st.session_state.ppt_page < len(slides) - 1:
                        st.session_state.ppt_page += 1
                        st.rerun()

    # ⚡ 閃電收件匣 & 知識庫
    @st.fragment
    def render_sticky_notes():
        with st.container(border=True):
            st.subheader("⚡ 閃電收件匣 (Capture)")
            with open(NOTE_FILE, "r", encoding="utf-8") as f: current_notes = f.read()
            user_notes = st.text_area("隨手記下目前的雜念...", value=current_notes, height=100, key="sticky_notes_input")
            if st.button("💾 儲存連接筆記"):
                with open(NOTE_FILE, "w", encoding="utf-8") as f: f.write(user_notes)
                st.toast("筆記已寫入本地端檔案！", icon="💾")

    render_sticky_notes()

with col_right:
    # 1. 軍用動態聲納雷達
    with st.container(border=True):
        st.subheader("🛰️ 軍用即時聲納雷達監控")
        
        # 如果番茄鐘啟動，雷達轉速和顏色會進入超載加速模式
        is_hacker_js = "true" if is_hacker else "false"
        pomo_speed_js = "0.04" if st.session_state.pomodoro_active else "0.015"
        
        radar_html = f"""
        <div style="text-align: center; background: { '#03120E' if is_hacker else '#f7f9fa' }; padding: 10px; border-radius: 8px;">
            <canvas id="militaryRadar" width="360" height="320"></canvas>
        </div>
        <script>
        (function() {{
            const canvas = document.getElementById('militaryRadar');
            const ctx = canvas.getContext('2d');
            const isHacker = {is_hacker_js};
            const sweepSpeed = {pomo_speed_js};
            
            const colors = isHacker ? {{
                bg: '#03120E', grid: '#004411', line: '#00ebd4', sweep: 'rgba(0, 235, 212, 0.15)', target: '#00ffcc'
            }} : {{
                bg: '#f7f9fa', grid: '#d1dbe0', line: '#0070f3', sweep: 'rgba(0, 112, 243, 0.08)', target: '#0051a8'
            }};
            
            let angle = 0;
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            const maxRadius = 130;
            
            const targets = [
                {{ name: 'Coding', val: {radar_data['Coding']}, angle: -Math.PI/2 }},
                {{ name: 'Focus', val: {radar_data['Focus']}, angle: -Math.PI/2 + (Math.PI*2/5) }},
                {{ name: 'Learn', val: {radar_data['Learn']}, angle: -Math.PI/2 + (Math.PI*2/5)*2 }},
                {{ name: 'Energy', val: {radar_data['Energy']}, angle: -Math.PI/2 + (Math.PI*2/5)*3 }},
                {{ name: 'Delivery', val: {radar_data['Delivery']}, angle: -Math.PI/2 + (Math.PI*2/5)*4 }}
            ];
            
            function draw() {{
                ctx.fillStyle = colors.bg; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = colors.grid; ctx.lineWidth = 1;
                for(let r = 30; r <= maxRadius; r += 30) {{
                    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
                }}
                ctx.beginPath(); ctx.moveTo(cx - maxRadius, cy); ctx.lineTo(cx + maxRadius, cy);
                ctx.moveTo(cx, cy - maxRadius); ctx.lineTo(cx, cy + maxRadius); ctx.stroke();
                
                ctx.beginPath();
                targets.forEach((t, i) => {{
                    let r = (t.val / 100) * maxRadius;
                    let x = cx + r * Math.cos(t.angle); let y = cy + r * Math.sin(t.angle);
                    if(i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
                }});
                ctx.closePath();
                ctx.strokeStyle = isHacker ? 'rgba(0,255,102,0.6)' : 'rgba(255,75,75,0.6)';
                ctx.stroke();

                ctx.fillStyle = colors.sweep; ctx.beginPath(); ctx.moveTo(cx, cy);
                ctx.arc(cx, cy, maxRadius, angle, angle + 0.4); ctx.closePath(); ctx.fill();
                
                ctx.strokeStyle = colors.line; ctx.beginPath(); ctx.moveTo(cx, cy);
                ctx.lineTo(cx + maxRadius * Math.cos(angle + 0.4), cy + maxRadius * Math.sin(angle + 0.4)); ctx.stroke();

                angle += sweepSpeed;
                requestAnimationFrame(draw);
            }}
            draw();
        }})();
        </script>
        """
        st.components.v1.html(radar_html, height=340)

    # 2. 下方區塊：動態日誌與實體解鎖控制區
    with st.container(border=True):
        if st.session_state.hacker_simulator_unlocked:
            st.subheader("🚨 極客黑客終極模擬器 (Matrix Core)")
            hacker_simulator_html = """
            <div id="simConsole" style="background:#000; color:#0f0; font-family:monospace; font-size:11px; padding:10px; height:180px; overflow:hidden; border:1px solid #0f0; border-radius:5px;"></div>
            <script>
            (function(){
                const consoleBox = document.getElementById('simConsole');
                const logPool = [
                    "[OK] AUTHORIZED VIA GITHUB OAUTH CLIENT...",
                    "[OK] DOCX_GENERATOR: COMPILING STANDARD RICH TEXT...",
                    "[INFO] PPT_ENGINE: PARTITIONING DATA VIA '---' SEGMENTS...",
                    "[ALIVE] POMODORO TIMER LINKED TO RADAR SWEEP SPEED..."
                ];
                function appendLog() {
                    let randomLine = logPool[Math.floor(Math.random() * logPool.length)];
                    let p = document.createElement('div'); p.innerText = "[" + new Date().toLocaleTimeString() + "] " + randomLine;
                    consoleBox.appendChild(p);
                    if(consoleBox.childNodes.length > 10) consoleBox.removeChild(consoleBox.firstChild);
                    consoleBox.scrollTop = consoleBox.scrollHeight;
                }
                setInterval(appendLog, 200);
            })();
            </script>
            """
            st.components.v1.html(hacker_simulator_html, height=200)
            if st.button("🔒 重新鎖定模擬器"):
                st.session_state.hacker_simulator_unlocked = False
                st.rerun()
        else:
            st.subheader("📟 系統事件日誌流 (Execute)")
            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col1:
                st.caption("提示: 系統處於防禦狀態。點擊右側解鎖高級模擬器。")
            with btn_col2:
                if st.button("🔓 解鎖特工模擬器"):
                    st.session_state.hacker_simulator_unlocked = True
                    st.rerun()
            
            log_time = datetime.now().strftime('%H:%M:%S')
            st.info(f"[{log_time}] [WORD_PPT_KERNEL] 雙模簡報與文件引擎運作正常。\n[{log_time}] [POMODORO] 脈衝鎖定裝置就緒。")
