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
    page_title="Cyber Hacker Workstation v8.4",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTE_FILE = "sticky_notes.txt"
KB_FILE = "my_knowledge_base.md"
DOC_FILE = "cyber_document.md"

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
if "king_unlocked" not in st.session_state:
    st.session_state.king_unlocked = False

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
    st.title("🛜 控制中心")
    
    ui_mode = st.radio(
        "切換工作台模式 (或按 F1 鍵)",
        ["正常模式 (Normal)", "駭客模式 (Hacker)"],
        index=0,
        key="ui_mode_select"
    )
    is_hacker = "Hacker" in ui_mode

    # 如果非駭客模式，清空狀態
    if not is_hacker:
        st.session_state.hacker_console_active = False
        st.session_state.king_unlocked = False

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
# 3. 全域 CSS 強力黑化樣式
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
        }
        div[data-testid="stDownloadButton"] button p { color: #00ff66 !important; }
        div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { 
            background-color: #00ff66 !important; 
            color: #000000 !important; 
            box-shadow: 0 0 8px #00ff66 !important; 
        }
        div[data-testid="stDownloadButton"] button:hover p { color: #000000 !important; }
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

# F1 快捷鍵相容層
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


# ========================================================================
# 🚨 畫面分流：全螢幕控制台 (畫面 A)
# ========================================================================
if is_hacker and st.session_state.hacker_console_active:
    
    if st.session_state.king_unlocked:
        st.markdown("<h1 style='color: #ff0033 !important;'>👑 終極矩陣核心控制台 (OVERRIDE ACTIVE)</h1>", unsafe_allow_html=True)
    else:
        st.title("📟 終極矩陣核心控制台 (OVERRIDE ACTIVE)")
    
    c_top1, c_top2 = st.columns([3, 1])
    with c_top1:
        if st.button("↩️ 關閉控制台並返回工作台"):
            st.session_state.hacker_console_active = False
            st.session_state.king_unlocked = False
            st.rerun()
    with c_top2:
        if st.session_state.king_unlocked:
            st.error("🚨 SYSTEM STATUS: OVERCLOCKED")
            
    st.markdown("---")
    
    # 動態變色變數設定
    if st.session_state.king_unlocked:
        speed_ms = "12"
        color_theme = "#ff0033"
        radar_speed = "0.22"
        radar_color = "rgba(255, 0, 50, 0.25)"
        radar_line_color = "#ff0033"
    else:
        speed_ms = "35"
        color_theme = "#00ff66"
        radar_speed = "0.06"
        radar_color = "rgba(0, 235, 212, 0.15)"
        radar_line_color = "#004411"

    # 頂部矩陣代碼雨 (徹底修復：不透過 Python 變數傳遞字串，完全由 JS 本地定義，100% 絕不報錯白屏)
    matrix_rain_html = f"""
    <div style="background:#000; padding:10px; border:2px solid {color_theme}; border-radius:8px; margin-bottom:20px;">
        <canvas id="fullscreenRain" style="width:100%; height:180px; background:#000;"></canvas>
    </div>
    <script>
    (function(){{
        const canvas = document.getElementById('fullscreenRain');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = 180;
        const letters = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","X","Y","Z"]; 
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        function draw() {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.06)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '{color_theme}'; ctx.font = fontSize + 'px monospace';
            for(let i=0; i<drops.length; i++) {{
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) {{ drops[i] = 0; }}
                drops[i]++;
            }}
        }}
        setInterval(draw, {speed_ms});
    }})();
    </script>
    """
    st.components.v1.html(matrix_rain_html, height=205)
    
    # 控制台功能區
    h_col1, h_col2, h_col3 = st.columns([1, 1, 1])
    with h_col1:
        with st.container(border=True):
            st.subheader("📡 特工節點安全通訊")
            if st.session_state.king_unlocked:
                st.error("⚠️ STATUS: ROOT OVERCLOCK")
                st.metric("權限等級", "ROOT / KING", "MAX")
                st.metric("主機核心頻率", "8.4 GHz", "+500%")
            else:
                st.metric("核心跳轉節點", "Proxy-Node-9", "+413ms")
                st.metric("防禦壁壘狀態", "BYPASSED", "100%")
            st.progress(1.0, text="安全矩陣核心全域覆寫已完成")
            
    with h_col2:
        with st.container(border=True):
            st.subheader("🛰️ 雷達追蹤 (極速脈衝模式)")
            radar_html_fs = f"""
            <div style="text-align: center; background: #03120E; padding: 5px; border-radius: 8px;">
                <canvas id="radarFS" width="300" height="230"></canvas>
            </div>
            <script>
            (function() {{
                const canvas = document.getElementById('radarFS');
                const ctx = canvas.getContext('2d');
                let angle = 0;
                const cx = canvas.width / 2; const cy = canvas.height / 2;
                function draw() {{
                    ctx.fillStyle = '#03120E'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.strokeStyle = '{radar_line_color}';
                    for(let r = 20; r <= 100; r += 20) {{
                        ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
                    }}
                    ctx.fillStyle = '{radar_color}'; ctx.beginPath(); ctx.moveTo(cx, cy);
                    ctx.arc(cx, cy, 100, angle, angle + 0.5); ctx.closePath(); ctx.fill();
                    angle += {radar_speed}; 
                    requestAnimationFrame(draw);
                }}
                draw();
            })();
            </script>
            """
            st.components.v1.html(radar_html_fs, height=250)

    with h_col3:
        with st.container(border=True):
            st.subheader("💀 [GHOST-NETWORK]")
            st.markdown(f"""
            <div style='border: 1px solid {color_theme}; padding: 10px; border-radius: 5px; background-color: #051a10; margin-bottom:12px;'>
                <p style='color: {color_theme}; font-weight: bold; margin-bottom: 0px;'>[ 戰略後門操控模組 ]</p>
            </div>
            """, unsafe_allow_html=True)
            
            b1 = st.button("📁 數據導出 (Dump User Credentials)", use_container_width=True)
            b2 = st.button("📡 衛星劫持 (Hijack Orbital Satellite)", use_container_width=True)
            b3 = st.button("🎭 換臉偽裝 (Wipe Terminal Traces)", use_container_width=True)
            b4 = st.button("💣 自毀程序 (Nuke Mainframe Server)", use_container_width=True)
            b5 = st.button("☢️ 引爆核彈 (Launch Strategic Nuke)", use_container_width=True)
            
            if b5:
                st.toast("⚠️ CRITICAL: 戰略引爆指令已成功向全球中繼節點發送！", icon="☢️")
            elif b1 or b2 or b3 or b4:
                st.toast("黑帽指令調用成功，正在進行終端擦除...", icon="⚡")
                
            st.markdown(f"<p style='font-size:11px; color:{color_theme}; margin-top:6px; line-height:1.4;'>系統狀態: 在線 (ENCRYPTED)<br>中繼節點: SOCKS5://103.24.51.9</p>", unsafe_allow_html=True)

    # 🔑 密碼與指令輸入框（完美固定出現在控制台最下方）
    st.write("")
    with st.container(border=True):
        cmd_input = st.text_input(
            "⌨️ [SYS-OVERRIDE] 核心指令輸入端 :", 
            key="hacker_cmd_terminal",
            type="password",
            placeholder="請輸入核心交互密鑰（輸入 king1030622 可啟用終極皇權紅化超頻模式）...",
        )
        if cmd_input.strip() == "king1030622" and not st.session_state.king_unlocked:
            st.session_state.king_unlocked = True
            st.toast("👑 終極皇權模式已啟用！矩陣系統開始全域超頻！", icon="👑")
            st.rerun()
        elif cmd_input and cmd_input.strip() != "king1030622":
            st.toast(f"執行指令: {cmd_input}", icon="📟")

else:
    # ========================================================================
    # 💻 標準主工作台面 (畫面 B)
    # ========================================================================
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
    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.container(border=True):
            st.subheader("📝 賽博文書終端 (Word & PPT 整合模組)")
            doc_tab1, doc_tab2 = st.tabs(["📄 Word 編輯模式", "📺 PPT 簡報播放模式"])
            
            with open(DOC_FILE, "r", encoding="utf-8") as f:
                doc_content = f.read()
                
            with doc_tab1:
                st.caption("利用 Markdown 編寫文件，使用 `---` 作為 PPT 的換頁符號。")
                edited_doc = st.text_area("文件編輯器", value=doc_content, height=250, key="word_editor")
                
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
                    st.markdown('<div class="ppt-slide-box" style="text-align: center; line-height: 200px; color: #888;">📡 暫無簡報數據</div>', unsafe_allow_html=True)
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
        with st.container(border=True):
            st.subheader("🛰️ 軍用即時聲納雷達監控")
            is_hacker_js = "true" if is_hacker else "false"
            pomo_speed_js = "0.04" if st.session_state.pomodoro_active else "0.015"
            
            # 軍用雷達
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
                const colors = isHacker ? {{ bg: '#03120E', grid: '#004411', line: '#00ebd4', sweep: 'rgba(0, 235, 212, 0.15)', target: '#00ffcc' }} : {{ bg: '#f7f9fa', grid: '#d1dbe0', line: '#0070f3', sweep: 'rgba(0, 112, 243, 0.08)', target: '#0051a8' }};
                let angle = 0; const cx = canvas.width / 2; const cy = canvas.height / 2; const maxRadius = 130;
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
                    ctx.beginPath(); ctx.moveTo(cx - maxRadius, cy); ctx.lineTo(cx + maxRadius, cy); ctx.moveTo(cx, cy - maxRadius); ctx.lineTo(cx, cy + maxRadius); ctx.stroke();
                    ctx.beginPath(); 
                    targets.forEach((t, i) => {{ 
                        let r = (t.val / 100) * maxRadius; 
                        let x = cx + r * Math.cos(t.angle); 
                        let y = cy + r * Math.sin(t.angle); 
                        if(i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); 
                    }}); 
                    ctx.closePath();
                    ctx.strokeStyle = isHacker ? 'rgba(0,255,102,0.6)' : 'rgba(255,75,75,0.6)'; ctx.stroke();
                    ctx.fillStyle = colors.sweep; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, maxRadius, angle, angle + 0.4); ctx.closePath(); ctx.fill();
                    ctx.strokeStyle = colors.line; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + maxRadius * Math.cos(angle + 0.4), cy + maxRadius * Math.sin(angle + 0.4)); ctx.stroke();
                    angle += sweepSpeed; requestAnimationFrame(draw);
                }}
                draw();
            }})();
            </script>
            """
            st.components.v1.html(radar_html, height=340)

        # 系統日誌流通行閘門 (主畫面進入控制台按鈕與通道)
        if is_hacker:
            with st.container(border=True):
                st.subheader("📟 系統事件日誌流 (Execute)")
                
                cmd_box = st.text_input("🔑 輸入終極通行密碼解鎖全螢幕隱藏控制台：", key="main_hacker_gate", type="password", placeholder="請在此輸入通行密鑰...")
                
                if cmd_box.strip() == "king1030622" and not st.session_state.hacker_console_active:
                    st.session_state.king_unlocked = True
                    st.session_state.hacker_console_active = True
                    st.success("👑 驗證通過！全域矩陣核心強制覆寫跳轉中...")
                    st.rerun()
                
                st.markdown("---")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("🔓 解鎖特工模擬器" if not st.session_state.hacker_simulator_unlocked else "🔒 鎖定模擬器"):
                        st.session_state.hacker_simulator_unlocked = not st.session_state.hacker_simulator_unlocked
                        st.rerun()
                with btn_col2:
                    if st.button("⚡ 手動進入全螢幕控制台"):
                        st.session_state.hacker_console_active = True
                        st.rerun()
