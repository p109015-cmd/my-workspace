import streamlit as st
import pandas as pd
import numpy as np
import requests
import feedparser
import os
from datetime import datetime

# ==========================================
# 0. 基礎設定與持久化檔案初始化
# ==========================================
st.set_page_config(
    page_title="Military Hacker Station v3.0",
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

# 初始化密碼解鎖狀態
if "hacker_simulator_unlocked" not in st.session_state:
    st.session_state.hacker_simulator_unlocked = False

# ==========================================
# 1. 外部 API 快取與擷取
# ==========================================
@st.cache_data(ttl=600)
def get_weather():
    try:
        response = requests.get("https://wttr.in/Gukeng?format=%c+%t+%h+%w", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception:
        pass
    return "⛅ 無法取得即時天氣資訊"

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
    st.subheader("📊 個人能力指標設定")
    val_coding = st.slider("Coding 輸出率", 0, 100, 85)
    val_focus = st.slider("心流專注度", 0, 100, 90)
    val_learn = st.slider("知識內化率", 0, 100, 75)
    val_energy = st.slider("精力續航力", 0, 100, 80)
    val_delivery = st.slider("專案交付率", 0, 100, 95)

# 用於傳遞給前端 Canvas 雷達的數據字典
radar_data = {
    "Coding": val_coding,
    "Focus": val_focus,
    "Learn": val_learn,
    "Energy": val_energy,
    "Delivery": val_delivery
}

# ==========================================
# 3. 處理 F2 密碼解鎖後台接收
# ==========================================
# 建立一個隱藏的輸入框，由前端 JavaScript 填入並觸發表單
secret_trigger = st.text_input("Secret Trigger", key="secret_trigger", label_visibility="collapsed")
if secret_trigger == "1030622":
    st.session_state.hacker_simulator_unlocked = True
    st.toast("🚨 [ACCESS GRANTED] 終極駭客模擬器已解鎖！", icon="🚨")

# ==========================================
# 4. 全域 CSS 與 鍵盤事件 JS 注入 (F1 & F2 監聽)
# ==========================================
# 基礎樣式與【全黑按鈕】優化
hacker_css = ""
if is_hacker:
    hacker_css = """
        .stApp { background-color: #0d0d0d !important; color: #00ff66 !important; font-family: 'Courier New', monospace !important; }
        [data-testid="stSidebar"] { background-color: #1a1a1a !important; color: #00ff66 !important; border-right: 1px solid #00ff66; }
        [data-testid="stMetric"] { background-color: #111111 !important; border: 1px solid #00ff66 !important; border-radius: 8px; padding: 10px; }
        div[data-testid="stContainer"] { border: 1px solid #00ff66 !important; background-color: #111111 !important; color: #00ff66 !important; }
        textarea, input { background-color: #151515 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; font-family: 'Courier New', monospace !important; }
        p, li, h1, h2, h3, h4, h5, h6, span, label { color: #00ff66 !important; }
        
        /* 🛠️ 駭客模式下的全黑按鈕 */
        button[data-testid="baseButton-secondary"] {
            background-color: #000000 !important;
            color: #00ff66 !important;
            border: 1px solid #00ff66 !important;
            font-weight: bold !important;
            font-family: 'Courier New', monospace !important;
            transition: all 0.3s ease;
        }
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #00ff66 !important;
            color: #000000 !important;
            box-shadow: 0 0 10px #00ff66;
        }
    """

st.markdown(f"<style>{hacker_css}</style>", unsafe_allow_html=True)

# 注入 F1 切換、F2 密碼彈窗的 JavaScript
st.components.v1.html(f"""
    <script>
    const doc = window.parent.document;
    
    // 監聽 F1 與 F2
    doc.removeEventListener('keydown', window.hackerKeyListener);
    window.hackerKeyListener = function(e) {{
        if (e.key === 'F1') {{
            e.preventDefault(); 
            const radios = doc.querySelectorAll('input[name="ui_mode_select"]');
            if (radios.length >= 2) {{
                if (radios[0].checked) radios[1].click();
                else radios[0].click();
            }}
        }}
        if (e.key === 'F2') {{
            e.preventDefault();
            let password = prompt("🔑 [SECURITY AUTHENTICATION] 請輸入特工解鎖密碼:");
            if (password !== null) {{
                // 找到 Streamlit 的隱藏輸入框並填值
                const inputs = doc.querySelectorAll('input[aria-label="Secret Trigger"]');
                if (inputs.length > 0) {{
                    inputs[0].value = password;
                    inputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        }}
    }};
    doc.addEventListener('keydown', window.hackerKeyListener);
    </script>
""", height=0)

# ==========================================
# 5. 主畫面排版 (Main UI Layout)
# ==========================================
st.title("⚡ 高效個人工作台")
st.caption(f"系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 軍用雷達＆極客解鎖完全體")

# 第一層：即時情報 Bento Grid (天氣與焦點新聞)
col_info1, col_info2 = st.columns([1, 2])
with col_info1:
    with st.container(border=True):
        st.subheader("📍 即時環境 (雲林古坑)")
        st.metric(label="wttr.in 觀測數據", value=get_weather())

with col_info2:
    with st.container(border=True):
        st.subheader("📰 今日焦點新聞 (Google News)")
        news_list = get_google_news()
        if news_list:
            for i, news in enumerate(news_list, 1):
                st.markdown(f"{i}. [{news['title']}]({news['link']})")
        else:
            st.write("暫時無法載入新聞。")

st.write("") 

# 第二層：核心工作區 (雙欄排版)
col_left, col_right = st.columns([3, 2])

# --- 左側欄：輸入與處理端 (採用 Fragment 確保重新整理時不干擾 Canvas) ---
with col_left:
    @st.fragment
    def render_sticky_notes():
        with st.container(border=True):
            st.subheader("⚡ 閃電收件匣 (Capture)")
            with open(NOTE_FILE, "r", encoding="utf-8") as f:
                current_notes = f.read()
            user_notes = st.text_area("隨手記下目前的雜念、任務、待辦...", value=current_notes, height=150, key="sticky_notes_input")
            if st.button("💾 儲存隨身筆記", key="save_notes_btn"):
                with open(NOTE_FILE, "w", encoding="utf-8") as f: f.write(user_notes)
                st.toast("隨身便利貼已安全寫入本地端檔案！", icon="💾")

    @st.fragment
    def render_knowledge_base():
        with st.container(border=True):
            st.subheader("🧠 深度第二大腦 (Knowledge Base)")
            with open(KB_FILE, "r", encoding="utf-8") as f:
                current_kb = f.read()
            user_kb = st.text_area("編輯你的 Markdown 知識庫內容：", value=current_kb, height=220, key="kb_input")
            if st.button("💾 更新知識庫", key="save_kb_btn"):
                with open(KB_FILE, "w", encoding="utf-8") as f: f.write(user_kb)
                st.toast("知識庫 Markdown 檔案已成功更新！", icon="🧠")
            st.markdown("---")
            st.markdown("**📄 當前知識庫預覽：**")
            st.markdown(user_kb)

    render_sticky_notes()
    st.write("")
    render_knowledge_base()

# --- 右側欄：軍用雷達與日誌打碼模擬器 (純 HTML5 Canvas 60FPS 極致流暢) ---
with col_right:
    # 1. 雙模軍用動態聲納雷達 (HTML5 Canvas)
    with st.container(border=True):
        st.subheader("🛰️ 軍用即時聲納雷達監控")
        
        # 將變數代入 JS Canvas 中
        is_hacker_js = "true" if is_hacker else "false"
        
        radar_html = f"""
        <div style="text-align: center; background: { '#03120E' if is_hacker else '#f7f9fa' }; padding: 10px; border-radius: 8px;">
            <canvas id="militaryRadar" width="360" height="360"></canvas>
        </div>
        <script>
        (function() {{
            const canvas = document.getElementById('militaryRadar');
            const ctx = canvas.getContext('2d');
            const isHacker = {is_hacker_js};
            
            // 主題配色設定
            const colors = isHacker ? {{
                bg: '#03120E', grid: '#004411', line: '#00ebd4', sweep: 'rgba(0, 235, 212, 0.15)', target: '#00ffcc'
            }} : {{
                bg: '#f7f9fa', grid: '#d1dbe0', line: '#0070f3', sweep: 'rgba(0, 112, 243, 0.08)', target: '#0051a8'
            }};
            
            let angle = 0;
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            const maxRadius = 150;
            
            // 讀取後端能力指標作為目標點
            const targets = [
                {{ name: 'Coding', val: {radar_data['Coding']}, angle: -Math.PI/2 }},
                {{ name: 'Focus', val: {radar_data['Focus']}, angle: -Math.PI/2 + (Math.PI*2/5) }},
                {{ name: 'Learn', val: {radar_data['Learn']}, angle: -Math.PI/2 + (Math.PI*2/5)*2 }},
                {{ name: 'Energy', val: {radar_data['Energy']}, angle: -Math.PI/2 + (Math.PI*2/5)*3 }},
                {{ name: 'Delivery', val: {radar_data['Delivery']}, angle: -Math.PI/2 + (Math.PI*2/5)*4 }}
            ];
            
            // 紀錄每個目標的發光強度
            targets.forEach(t => t.intensity = 0);

            function draw() {{
                ctx.fillStyle = colors.bg;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // 1. 繪製圓形雷達網格與十字架
                ctx.strokeStyle = colors.grid;
                ctx.lineWidth = 1;
                for(let r = 30; r <= maxRadius; r += 30) {{
                    ctx.beginPath();
                    ctx.arc(cx, cy, r, 0, Math.PI * 2);
                    ctx.stroke();
                }}
                ctx.beginPath();
                ctx.moveTo(cx - maxRadius, cy); ctx.lineTo(cx + maxRadius, cy);
                ctx.moveTo(cx, cy - maxRadius); ctx.lineTo(cx, cy + maxRadius);
                ctx.stroke();
                
                // 外圈刻度線
                ctx.strokeStyle = colors.grid;
                for(let a=0; a<360; a+=10) {{
                    let rad = a * Math.PI / 180;
                    let x1 = cx + maxRadius * Math.cos(rad);
                    let y1 = cy + maxRadius * Math.sin(rad);
                    let x2 = cx + (maxRadius - (a % 30 === 0 ? 8 : 4)) * Math.cos(rad);
                    let y2 = cy + (maxRadius - (a % 30 === 0 ? 8 : 4)) * Math.sin(rad);
                    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
                }}
                
                // 2. 繪製連動的多邊形狀態面 (雷達核心數據)
                ctx.beginPath();
                targets.forEach((t, i) => {{
                    let r = (t.val / 100) * maxRadius;
                    let x = cx + r * Math.cos(t.angle);
                    let y = cy + r * Math.sin(t.angle);
                    if(i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
                }});
                ctx.closePath();
                ctx.strokeStyle = isHacker ? 'rgba(0,255,102,0.6)' : 'rgba(255,75,75,0.6)';
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.fillStyle = isHacker ? 'rgba(0,255,102,0.1)' : 'rgba(255,75,75,0.08)';
                ctx.fill();

                // 3. 繪製動態雷達掃描扇面
                ctx.fillStyle = ctx.createRadialGradient(cx, cy, 10, cx, cy, maxRadius);
                ctx.fillStyle = colors.sweep;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.arc(cx, cy, maxRadius, angle, angle + 0.4);
                ctx.closePath();
                ctx.fill();
                
                // 掃描主導線
                ctx.strokeStyle = colors.line;
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(cx + maxRadius * Math.cos(angle + 0.4), cy + maxRadius * Math.sin(angle + 0.4));
                ctx.stroke();

                // 4. 繪製追蹤目標點並計算掃描高亮
                targets.forEach(t => {{
                    let r = (t.val / 100) * maxRadius;
                    let tx = cx + r * Math.cos(t.angle);
                    let ty = cy + r * Math.sin(t.angle);
                    
                    // 計算掃描線與目標點的角度差，若被掃到則激發高亮
                    let diff = (angle + 0.4) - t.angle;
                    while (diff < 0) diff += Math.PI * 2;
                    diff = diff % (Math.PI * 2);
                    if (diff < 0.15) {{
                        t.intensity = 1.0;
                    }} else {{
                        t.intensity *= 0.98; // 逐漸淡出 (Fade out)
                    }}
                    
                    if (t.intensity > 0.05) {{
                        ctx.shadowBlur = 15;
                        ctx.shadowColor = colors.target;
                        ctx.fillStyle = colors.target;
                        ctx.beginPath();
                        ctx.arc(tx, ty, 5 * t.intensity + 2, 0, Math.PI*2);
                        ctx.fill();
                        ctx.shadowBlur = 0; // 還原
                        
                        // 戰術文字
                        ctx.fillStyle = colors.line;
                        ctx.font = "9px monospace";
                        ctx.fillText(`[TRGT:${t.name} ${t.val}%]`, tx + 8, ty - 2);
                    }}
                }});

                angle += 0.015; // 控制雷達旋轉速度
                requestAnimationFrame(draw);
            }}
            draw();
        }})();
        </script>
        """
        st.components.v1.html(radar_html, height=390)

    # 2. 下方區塊：一般事件日誌 vs 解鎖後的【極客黑客終極模擬器】
    with st.container(border=True):
        if st.session_state.hacker_simulator_unlocked:
            st.subheader("🚨 極客黑客終極模擬器 (Matrix Core)")
            
            # 60FPS 快速向下噴碼的駭客模擬器代碼
            hacker_simulator_html = """
            <div id="simConsole" style="background:#000; color:#0f0; font-family:monospace; font-size:11px; padding:10px; height:220px; overflow-hidden:hidden; border:1px solid #0f0; border-radius:5px; line-height:1.4;"></div>
            <script>
            (function(){
                const consoleBox = document.getElementById('simConsole');
                const logPool = [
                    "[OK] CONNECTED TO CORE MAIN_FRAME SERVER...",
                    "[INFO] DECRYPTING BLOCKCHAIN SYNC INDEX...",
                    "[WARN] FIREWALL DETECTED: BYPASSING PROTOCOL SEC-9",
                    "[SUCCESS] ACCESS GRANTED TO DATABASE TRIDENT_V2",
                    "[ALIVE] RUNNING INFILTRATION SCRIPT: ./shadow_walk.sh",
                    "[CRITICAL] EXPLOITING BUFFER OVERFLOW AT ADDRESS 0x7FFF58",
                    "[PACKET] INBOUND TRAFFIC FROM IP 103.6.22.109 LOCKED",
                    "--------------------------------------------------",
                    ">> LOADING MATRIX QUANTUM ALGORITHM...",
                    ">> DOWNLOADING ENCRYPTED DATA STREAM... [78% completed]",
                    ">> INJECTING PAYLOAD INTO KERNEL LAND (ROOT_ACCESS)"
                ];
                
                function appendLog() {
                    let randomLine = logPool[Math.floor(Math.random() * logPool.length)];
                    let timestamp = new Date().toLocaleTimeString();
                    
                    let p = document.createElement('div');
                    p.innerText = `[${timestamp}] ${randomLine}`;
                    consoleBox.appendChild(p);
                    
                    // 超出高度時滾動並刪除舊資料，維持流暢
                    if(consoleBox.childNodes.length > 15) {
                        consoleBox.removeChild(consoleBox.firstChild);
                    }
                    consoleBox.scrollTop = consoleBox.scrollHeight;
                }
                setInterval(appendLog, 120); // 瘋狂打碼刷新速率
            })();
            </script>
            """
            st.components.v1.html(hacker_simulator_html, height=240)
            
            if st.button("🔒 重新鎖定模擬器"):
                st.session_state.hacker_simulator_unlocked = False
                st.rerun()
        else:
            st.subheader("📟 系統事件日誌流 (Execute)")
            st.caption("提示: 系統處於安全狀態下。按下 F2 可以輸入特工密鑰。")
            
            log_time = datetime.now().strftime('%H:%M:%S')
            mode_tag = "[CRITICAL_HACKER_MODE]" if is_hacker else "[NORMAL_WORK_MODE]"
            logs = [
                f"[{log_time}] {mode_tag} 心流狀態儀表板已成功掛載。",
                f"[{log_time}] [IO_SERVER] 讀取儲存檔案完畢。",
                f"[{log_time}] [NETWORK] 天氣與新聞快取同步中。",
                f"[{log_time}] [JS_KERNEL] F1(切換)/F2(解鎖) 核心監聽器已安全就緒。"
            ]
            if is_hacker:
                st.code("\n".join(logs), language="bash")
            else:
                for log in logs: st.info(log)
