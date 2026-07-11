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
    page_title="Cyber Hacker Workstation v4.6",
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
if "hacker_console_active" not in st.session_state:
    st.session_state.hacker_console_active = False

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
        
        /* 強制壓制普通按鈕與下載按鈕外殼，消滅亮白區塊 */
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
st.title("⚡ 高效率個人工作台 v4.6")
st.caption(f"系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 終端狀態: 線上")

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
    # 📝 Word / PPT 賽博編輯器
    with st.container(border=True):
        st.subheader("📝 賽博文書終端 (Word & PPT 整合模組)")
        
        doc_tab1, doc_tab2 = st.tabs(["📄 Word 編輯模式", "📺 PPT 簡報播放模式"])
        
        with open(DOC_FILE, "r", encoding="utf-8") as f:
            doc_content = f.read()
            
        with doc_tab1:
            st.caption("利用 Markdown 編寫文件，使用 `---` 作為 PPT 的換頁符號。")
            edited_doc = st.text_area("文件編輯器 (支援豐富文本)", value=doc_content, height=250, key="word_editor", placeholder="# 在這裡輸入標題...\n---\n## 新增分頁...")
            
            w_col1, w_col2, w_col3 = st.columns(3)
            with w_col1:
                if st.button("💾 儲存最新文本"):
                    with open(DOC_FILE, "w", encoding="utf-8") as f:
                        f.write(edited_doc)
                    st.toast("文件已成功寫入核心矩陣！", icon="💾")
                    st.rerun()
            with w_col2:
                st.download_button("📥 匯出為 .md 檔案", data=edited_doc, file_name="Cyber_Report.md", mime="text/markdown")
            with w_col3:
                st.download_button("📥 匯出為 Word 格式", data=edited_doc, file_name="Cyber_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                
        with doc_tab2:
            slides = [s.strip() for s in doc_content.split("---") if s.strip()]
            
            if not slides or doc_content.strip() == "":
                st.markdown('<div class="ppt-slide-box" style="text-align: center; line-height: 200px; color: #888;">📡 [WAITING FOR MATRIX DATA] 暫無簡報數據，請先在 Word 模式編寫並儲存。</div>', unsafe_allow_html=True)
            else:
                if st.session_state.ppt_page >= len(slides):
                    st.session_state.ppt_page = len(slides) - 1
                
                current_slide_content = slides[st.session_state.ppt_page]
                st.markdown(f'<div class="ppt-slide-box">{current_slide_content}</div>', unsafe_allow_html=True)
                
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

    # ⚡ 閃電收件匣
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

    # ==========================================
    # 🟢 駭客模式限制門：日誌與控制台切換區
    # ==========================================
    if is_hacker:
        with st.container(border=True):
            # 判斷是否按下了「駭客控制台」切換鈕
            if st.session_state.hacker_console_active:
                st.subheader("🖥️ 核心矩陣終端控制台 (Hacker OS)")
                
                # 經典駭客控制台畫面：Canvas 密碼雨 + 動態狀態面板
                hacker_dashboard_html = """
                <div style="background:#000; color:#0f0; padding:15px; border:2px solid #0f0; border-radius:5px; font-family:monospace; position:relative; overflow:hidden;">
                    <canvas id="matrixRain" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0.2; pointer-events:none;"></canvas>
                    <div style="position:relative; z-index:2;">
                        <h4 style="color:#00ff66; margin:0 0 10px 0;">🔴 OVERRIDE STATUS: ACTIVE</h4>
                        <table style="width:100%; border-collapse:collapse; font-size:12px; color:#00ff66;">
                            <tr><td>[MATRIX_CORE]</td><td>RUNNING (PORT 8080)</td></tr>
                            <tr><td>[PROXY_NODE]</td><td>ENCRYPTED TUNNEL TUN0</td></tr>
                            <tr><td>[DECRYPT_LOG]</td><td id="liveText">WAITING FOR PACKETS...</td></tr>
                        </table>
                        <hr style="border-color:#004411; margin:10px 0;">
                        <div id="scrollingConsole" style="height:80px; font-size:11px; overflow:hidden;"></div>
                    </div>
                </div>
                
                <script>
                (function(){
                    // 1. 密碼雨代碼
                    const canvas = document.getElementById('matrixRain');
                    const ctx = canvas.getContext('2d');
                    canvas.width = 400; canvas.height = 180;
                    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&'.split('');
                    const fontSize = 10;
                    const columns = canvas.width / fontSize;
                    const drops = Array(Math.floor(columns)).fill(1);
                    
                    function drawRain() {
                        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = '#0f0'; ctx.font = fontSize + 'px monospace';
                        for(let i=0; i<drops.length; i++) {
                            const text = letters[Math.floor(Math.random() * letters.length)];
                            ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                            if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                            drops[i]++;
                        }
                    }
                    setInterval(drawRain, 33);
                    
                    // 2. 動態事件輪播
                    const consoleBox = document.getElementById('scrollingConsole');
                    const liveText = document.getElementById('liveText');
                    const events = [
                        "Dumping memory block 0x7FFF...", "Bypassing mainstream firewall...", 
                        "Packet intercepted from mainframe.", "Injecting payload into proxy layer..."
                    ];
                    setInterval(() => {
                        let line = events[Math.floor(Math.random()*events.length)];
                        liveText.innerText = line;
                        let div = document.createElement('div'); div.innerText = ">> " + line;
                        consoleBox.appendChild(div);
                        if(consoleBox.childNodes.length > 5) consoleBox.removeChild(consoleBox.firstChild);
                    }, 800);
                })();
                </script>
                """
                st.components.v1.html(hacker_dashboard_html, height=210)
                
                # 控制台下方的回退/操作按鈕
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if st.button("↩️ 返回標準日誌"):
                        st.session_state.hacker_console_active = False
                        st.rerun()
                with btn_c2:
                    st.button("⚙️ 執行矩陣同步")

            # 預設：顯示原有的日誌系統與解鎖面板
            elif st.session_state.hacker_simulator_unlocked:
                st.subheader("🚨 極客黑客終極模擬器 (Matrix Core)")
                hacker_simulator_html = """
                <div id="simConsole" style="background:#000; color:#0f0; font-family:monospace; font-size:11px; padding:10px; height:140px; overflow:hidden; border:1px solid #0f0; border-radius:5px;"></div>
                <script>
                (function(){
                    const consoleBox = document.getElementById('simConsole');
                    const logPool = [
                        "[OK] AUTHORIZED VIA GITHUB OAUTH CLIENT...",
                        "[OK] RICH_TEXT_ENGINE: SECURITY LAYER ACTIVE...",
                        "[INFO] HACKER_CONSOLE_GATE: READIED...",
                        "[ALIVE] POMODORO TIMER LINKED TO RADAR SWEEP SPEED..."
                    ];
                    function appendLog() {
                        let randomLine = logPool[Math.floor(Math.random() * logPool.length)];
                        let p = document.createElement('div'); p.innerText = "[" + new Date().toLocaleTimeString() + "] " + randomLine;
                        consoleBox.appendChild(p);
                        if(consoleBox.childNodes.length > 8) consoleBox.removeChild(consoleBox.firstChild);
                        consoleBox.scrollTop = consoleBox.scrollHeight;
                    }
                    setInterval(appendLog, 250);
                })();
                </script>
                """
                st.components.v1.html(hacker_simulator_html, height=160)
                
                # 新增的「駭客」按鈕 (解鎖後顯示，用來切換至控制台畫面)
                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    if st.button("🔒 重新鎖定模擬器"):
                        st.session_state.hacker_simulator_unlocked = False
                        st.rerun()
                with h_col2:
                    if st.button("⚡ 啟動駭客控制台"):
                        st.session_state.hacker_console_active = True
                        st.rerun()
            else:
                st.subheader("📟 系統事件日誌流 (Execute)")
                btn_col1, btn_col2 = st.columns([2, 1])
                with btn_col1:
                    st.caption("提示: 系統處於安全防禦狀態。")
                with btn_col2:
                    if st.button("🔓 解鎖特工模擬器"):
                        st.session_state.hacker_simulator_unlocked = True
                        st.rerun()
                
                log_time = datetime.now().strftime('%H:%M:%S')
                st.info(f"[{log_time}] [KERNEL] 密鑰鎖定中。駭客專屬控制台按鈕已就緒。\n[{log_time}] [SECURITY] 隔離區未偵測到威脅。")
