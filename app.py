import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime

# ==========================================
# 0. 基礎設定與持久化檔案初始化
# ==========================================
st.set_page_config(
    page_title="Cyber Hacker Workstation v9.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTE_FILE = "sticky_notes.txt"
KB_FILE = "my_knowledge_base.md"
DOC_FILE = "cyber_document.md"

if "doc_initialized" not in st.session_state:
    try:
        with open(DOC_FILE, "w", encoding="utf-8") as f: f.write("")
    except Exception: pass
    st.session_state.doc_initialized = True

for file, default_content in [
    (NOTE_FILE, "隨手記下目前的雜念、任務、待辦..."),
    (KB_FILE, "# 知識管理庫 (PARA)\n\n在這裡建立你的深度第二大腦。")
]:
    if not os.path.exists(file):
        try:
            with open(file, "w", encoding="utf-8") as f: f.write(default_content)
        except Exception: pass

# 初始化 Session 狀態
if "hacker_simulator_unlocked" not in st.session_state: st.session_state.hacker_simulator_unlocked = False
if "ppt_page" not in st.session_state: st.session_state.ppt_page = 0
if "pomodoro_active" not in st.session_state: st.session_state.pomodoro_active = False
if "hacker_console_active" not in st.session_state: st.session_state.hacker_console_active = False
if "king_unlocked" not in st.session_state: st.session_state.king_unlocked = False
if "active_panel" not in st.session_state: st.session_state.active_panel = None
if "nuke_detonated" not in st.session_state: st.session_state.nuke_detonated = False

# ==========================================
# 1. 拔除外部網路 API，改為純本地高速模擬
# ==========================================
def get_formatted_weather():
    current_hour = datetime.now().hour
    temp = 28 if 6 <= current_hour <= 18 else 24
    return f"⛅ 雲林古坑本地安全終端 / {temp}°C / 濕度 78% [衛星連線正常]"

def get_google_news():
    return [
        {"title": "🔊 [系統安全] 核心網路防火牆協議已全面升級至第 9 代", "link": "#"},
        {"title": "📡 [衛星通訊] 戰略軍用軌道劫持模組已完成全自動沙盒測試", "link": "#"},
        {"title": "⚡ [能源管理] 賽博脈衝番茄鐘核心矩陣超頻效率提升 22%", "link": "#"},
        {"title": "👑 [權限宣告] 檢測到特有代碼 '22' 指令閘門，高階覆寫系統準備就緒", "link": "#"}
    ]

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

    if not is_hacker:
        st.session_state.hacker_console_active = False
        st.session_state.king_unlocked = False
        st.session_state.active_panel = None

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
# 3. 全域 CSS 強力黑化與爆紅自毀樣式 (大括號已修正)
# ==========================================
hacker_css = ""
if is_hacker:
    if st.session_state.active_panel == "nuke_self":
        theme_main = "#ff0033"
        bg_main = "#1a0003"
        border_main = "#ff0033"
    elif st.session_state.king_unlocked:
        theme_main = "#ff0033"
        bg_main = "#0d0d0d"
        border_main = "#ff0033"
    else:
        theme_main = "#00ff66"
        bg_main = "#0d0d0d"
        border_main = "#004411"

    hacker_css = f"""
        header[data-testid="stHeader"], [data-testid="stHeader"] {{ background-color: {bg_main} !important; border-bottom: 1px solid {border_main} !important; }}
        header[data-testid="stHeader"] * {{ color: {theme_main} !important; fill: {theme_main} !important; }}
        .stApp {{ background-color: {bg_main} !important; color: {theme_main} !important; font-family: 'Courier New', monospace !important; }}
        [data-testid="stSidebar"] {{ background-color: #111111 !important; color: {theme_main} !important; border-right: 1px solid {theme_main}; }}
        [data-testid="stMetric"] {{ background-color: #000000 !important; border: 1px solid {theme_main} !important; border-radius: 8px; padding: 10px; }}
        div[data-testid="stContainer"] {{ border: 1px solid {border_main} !important; background-color: #000000 !important; color: {theme_main} !important; }}
        textarea, input {{ background-color: #151515 !important; color: {theme_main} !important; border: 1px solid {theme_main} !important; }}
        p, li, h1, h2, h3, h4, h5, h6, span, label {{ color: {theme_main} !important; }}
        a {{ color: #88ccff !important; }}
        
        div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button, div[data-testid="stDownloadButton"] a {{
            background-color: #000000 !important; 
            color: {theme_main} !important; 
            border: 1px solid {theme_main} !important; 
            font-weight: bold !important; 
        }}
        div[data-testid="stDownloadButton"] button p {{ color: {theme_main} !important; }}
        div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {{
            background-color: {theme_main} !important; 
            color: #000000 !important; 
            box-shadow: 0 0 8px {theme_main} !important; 
        }}
        div[data-testid="stDownloadButton"] button:hover p {{ color: #000000 !important; }}
        div[data-testid="stNotification"], div[data-testid="stAlert"] {{ background-color: #000000 !important; color: {theme_main} !important; border: 1px solid {theme_main} !important; }}
    """

ppt_box_bg = "#051a10" if is_hacker else "#f0f4f8"
ppt_box_border = "#00ff66" if is_hacker else "#0070f3"
ppt_text_color = "#00ff66" if is_hacker else "#333333"

st.markdown(f"<style>{hacker_css} .ppt-slide-box {{ background-color: {ppt_box_bg}; border: 2px dashed {ppt_box_border}; border-radius: 12px; padding: 40px; min-height: 280px; color: {ppt_text_color}; box-shadow: inset 0 0 15px rgba(0,0,0,0.5); margin-bottom: 15px; }} </style>", unsafe_allow_html=True)

# F1 快捷鍵
st.components.v1.html("<script>const handleF1 = (e) => { if (e.key === 'F1') { e.preventDefault(); const radios = window.parent.document.querySelectorAll('[data-testid=\"stSidebar\"] input[type=\"radio\"]'); if (radios.length >= 2) { if (radios[0].checked) radios[1].click(); else radios[0].click(); } } }; window.addEventListener('keydown', handleF1); window.parent.document.addEventListener('keydown', handleF1);</script>", height=0)

# ========================================================================
# 🚨 畫面分流：全螢幕終極控制台 (畫面 A)
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
            st.session_state.active_panel = None
            st.rerun()
    with c_top2:
        if st.session_state.king_unlocked or st.session_state.active_panel == "nuke_self":
            st.error("🚨 SYSTEM STATUS: CRITICAL")
            
    st.markdown("---")
    
    # 動態變色主題
    if st.session_state.king_unlocked or st.session_state.active_panel == "nuke_self":
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

    matrix_rain_template = """
    <div style="background:#000; padding:10px; border:2px solid __COLOR__; border-radius:8px; margin-bottom:20px;">
        <canvas id="fullscreenRain" style="width:100%; height:140px; background:#000;"></canvas>
    </div>
    <script>
    (function(){
        const canvas = document.getElementById('fullscreenRain'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = 140;
        const isKing = __IS_KING__;
        const charStr = isKing ? "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ☣☠⚡⚙KING👑" : "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ☣☠⚡";
        const letters = charStr.split(''); const fontSize = 14; const columns = canvas.width / fontSize; const drops = Array(Math.floor(columns)).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.06)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '__COLOR__'; ctx.font = fontSize + 'px monospace';
            for(let i=0; i<drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)]; ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
                drops[i]++;
            }
        }
        setInterval(draw, __SPEED__);
    })();
    </script>
    """
    st.components.v1.html(matrix_rain_template.replace("__COLOR__", color_theme).replace("__SPEED__", speed_ms).replace("__IS_KING__", "true" if st.session_state.king_unlocked else "false"), height=160)
    
    h_col1, h_col2, h_col3 = st.columns([1, 1, 1])
    with h_col1:
        with st.container(border=True):
            st.subheader("📡 特工節點安全通訊")
            if st.session_state.king_unlocked:
                st.error("⚠️ STATUS: ROOT OVERCLOCK")
                st.metric("權限等級", "ROOT / KING", "MAX")
                st.metric("主機核心頻率", "8.4 GHz", "+500%")
            else:
                st.metric("核心跳轉節點", "Proxy-Node-22", "+22ms")
                st.metric("防禦壁壘狀態", "BYPASSED", "100%")
            st.progress(1.0, text="安全矩陣核心全域覆寫已完成")
            
    with h_col2:
        with st.container(border=True):
            st.subheader("🛰️ 雷達追蹤 (極速脈衝模式)")
            radar_template_fs = """
            <div style="text-align: center; background: #03120E; padding: 5px; border-radius: 8px;">
                <canvas id="radarFS" width="300" height="210"></canvas>
            </div>
            <script>
            (function() {
                const canvas = document.getElementById('radarFS'); const ctx = canvas.getContext('2d'); let angle = 0;
                const cx = canvas.width / 2; const cy = canvas.height / 2;
                function draw() {
                    ctx.fillStyle = '#03120E'; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = '__LINE_COLOR__';
                    for(let r = 20; r <= 90; r += 20) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke(); }
                    ctx.fillStyle = '__RADAR_COLOR__'; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, 90, angle, angle + 0.5); ctx.closePath(); ctx.fill();
                    angle += __SPEED__; requestAnimationFrame(draw);
                }
                draw();
            })();
            </script>
            """
            st.components.v1.html(radar_template_fs.replace("__LINE_COLOR__", radar_line_color).replace("__RADAR_COLOR__", radar_color).replace("__SPEED__", radar_speed), height=225)

    with h_col3:
        with st.container(border=True):
            st.subheader("💀 [GHOST-NETWORK]")
            st.markdown(f"<div style='border: 1px solid {color_theme}; padding: 6px; border-radius: 5px; background-color: #051a10; margin-bottom:10px;'><p style='color: {color_theme}; font-weight: bold; margin-bottom: 0px;'>[ 戰略後門操控模組 ]</p></div>", unsafe_allow_html=True)
            
            if st.button("📁 數據導出 (Dump User Credentials)", use_container_width=True): st.session_state.active_panel = "dump"
            if st.button("📡 衛星劫持 (Hijack Orbital Satellite)", use_container_width=True): st.session_state.active_panel = "satellite"
            if st.button("🎭 換臉偽裝 (Wipe Terminal Traces)", use_container_width=True): st.session_state.active_panel = "wipe"
            if st.button("💣 自毀程序 (Nuke Mainframe Server)", use_container_width=True): st.session_state.active_panel = "nuke_self"
            if st.button("☢️ 引爆核彈 (Launch Strategic Nuke)", use_container_width=True): st.session_state.active_panel = "nuke_launch"

    # ========================================================================
    # 🕹️ 核心動態聯動交互面板 (5 大按鈕對應畫面)
    # ========================================================================
    if st.session_state.active_panel:
        st.write("")
        
        # --- 1. 數據導出 ---
        if st.session_state.active_panel == "dump":
            with st.container(border=True):
                st.subheader("📁 [DUMPING] 憑證數據全域爆破流")
                dump_html = """
                <div style="background:#000; border:1px solid #00ff66; padding:15px; border-radius:5px; font-family:monospace; height:200px; overflow-y:scroll;" id="dump_box"></div>
                <script>
                const box = document.getElementById('dump_box');
                function addLog() {
                    const ips = ["103.24.51.9", "192.168.1.22", "45.112.33.88", "12.84.22.103"];
                    const randomIp = ips[Math.floor(Math.random()*ips.length)];
                    const hash = Math.random().toString(36).substring(2, 15).toUpperCase();
                    box.innerHTML += `<p style="color:#00ff66; margin:3px 0;">[FETCHING] IP: ${randomIp} | HASH_KEY: SHA256-${hash} ... <span style="color:#fff;">[SUCCESS]</span></p>`;
                    box.scrollTop = box.scrollHeight;
                }
                setInterval(addLog, 150);
                </script>
                """
                st.components.v1.html(dump_html, height=220)
                fake_data = "IP_Address,Access_Token,Status\n103.24.51.9,X78S922K,ROOT\n192.168.1.22,KING0622,OVERCLOCK"
                st.download_button("📥 下載已打包憑證機密明單 (.csv)", fake_data, file_name="compromised_credentials.csv", mime="text/csv")

        # --- 2. 衛星劫持 (修正大括號與 getContext) ---
        elif st.session_state.active_panel == "satellite":
            with st.container(border=True):
                st.subheader("📡 [ORBITAL-LINK] 戰略衛星特種劫持控制台")
                sat_target = st.text_input("⌨️ 請輸入欲鎖定的目標國家/城市名稱：", value="台灣", key="sat_target_input")
                
                sat_html = f"""
                <div style="background:#000; padding:10px; border:1px solid #00ff66; border-radius:5px; text-align:center;">
                    <canvas id="satCanvas" width="600" height="220" style="background:#020b08;"></canvas>
                </div>
                <script>
                (function(){{
                    const canvas = document.getElementById('satCanvas'); const ctx = canvas.getContext('2d');
                    let target = "{sat_target}"; let angle = 0; let scale = 1.5; let lockTimer = 0;
                    function draw() {{
                        ctx.fillStyle = '#020b08'; ctx.fillRect(0,0,canvas.width,canvas.height);
                        let cx = canvas.width/2; let cy = canvas.height/2;
                        
                        ctx.strokeStyle = 'rgba(0,68,17,0.4)'; ctx.lineWidth = 1;
                        for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
                        for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width,j); ctx.stroke(); }}
                        
                        lockTimer += 2;
                        if(lockTimer < 100) {{
                            ctx.strokeStyle = '#00ff66'; ctx.beginPath(); ctx.arc(cx, cy, 80 * scale, 0, Math.PI*2); ctx.stroke();
                            ctx.fillStyle = 'rgba(0,255,102,0.1)'; ctx.beginPath(); ctx.moveTo(cx,cy); ctx.arc(cx,cy, 120, angle, angle+0.8); ctx.closePath(); ctx.fill();
                            ctx.fillStyle = '#00ff66'; ctx.font = '14px monospace'; ctx.fillText("[SCANNING & LOCKING]: " + target + "...", 20, 30);
                            scale = 1.0 + Math.sin(lockTimer/10)*0.3; angle += 0.1;
                        }} else {{
                            ctx.strokeStyle = '#ff0033'; ctx.lineWidth = 2;
                            ctx.beginPath(); ctx.arc(cx, cy, 50, 0, Math.PI*2); ctx.stroke();
                            ctx.beginPath(); ctx.moveTo(cx-70, cy); ctx.lineTo(cx+70, cy); ctx.moveTo(cx, cy-70); ctx.lineTo(cx, cy+70); ctx.stroke();
                            ctx.fillStyle = '#ff0033'; ctx.font = '14px monospace';
                            ctx.fillText("[🔒 TARGET LOCKED SUCCESS]", 20, 30);
                            ctx.fillText("TARGET: " + target.toUpperCase(), 20, 50);
                            ctx.fillText("LAT: " + (22.0622 + Math.random()*2).toFixed(4) + "° N", 20, 70);
                            ctx.fillText("LNG: " + (120.5190 + Math.random()*2).toFixed(4) + "° E", 20, 90);
                        }}
                        requestAnimationFrame(draw);
                    }}
                    draw();
                }})();
                </script>
                """
                st.components.v1.html(sat_html, height=260)

        # --- 3. 換臉偽裝 ---
        elif st.session_state.active_panel == "wipe":
            with st.container(border=True):
                st.subheader("🎭 [IDENTITY-SHIELD] 虛擬數位迷彩跳轉")
                wipe_html = """
                <div style="background:#000; font-family:monospace; padding:15px; border:1px solid #00ff66; border-radius:5px; color:#00ff66;">
                    <p id="p1">> 正在初始化全域 Proxy 跳轉鏈...</p>
                    <p id="p2" style="display:none; color:#00ebd4;">> 節點 1: TAIWAN_GUKENG_GATEWAY (ESTABLISHED)</p>
                    <p id="p3" style="display:none; color:#00ebd4;">> 節點 2: TOKYO_DARKNET_NODE_22 (TUNNELING)</p>
                    <p id="p4" style="display:none; color:#ff0033;">> [INFO] 本地真實 MAC & IP 位址已全面抹除隱蔽！</p>
                    <h4 id="p5" style="display:none; color:#00ff66; text-shadow:0 0 5px #00ff66;">🟢 虛擬數位迷彩防護盾：100% 全域覆蓋中</h4>
                </div>
                <script>
                setTimeout(()=>{ document.getElementById('p2').style.display='block'; }, 500);
                setTimeout(()=>{ document.getElementById('p3').style.display='block'; }, 1200);
                setTimeout(()=>{ document.getElementById('p4').style.display='block'; }, 2000);
                setTimeout(()=>{ document.getElementById('p5').style.display='block'; }, 2600);
                </script>
                """
                st.components.v1.html(wipe_html, height=180)

        # --- 4. 自毀程序 ---
        elif st.session_state.active_panel == "nuke_self":
            with st.container(border=True):
                st.markdown("<h3 style='color:#ff0033;'>💣 [⚠️ CRITICAL] 主機自毀矩陣已全面啟動</h3>", unsafe_allow_html=True)
                st.error("警告：全域伺服器沙盒即將在 10 秒內完全核平熔毀。")
                
                nuke_self_html = """
                <div style="text-align:center; font-family:monospace; background:#000; padding:15px; border:2px solid #ff0033; border-radius:5px;">
                    <h1 style="color:#ff0033; font-size:48px; margin:5px 0;" id="self_countdown">10.00</h1>
                    <p style="color:#ff0033;" id="self_status">SYS_MELTDOWN_IN_PROGRESS</p>
                </div>
                <script>
                let sec = 10.00;
                let timer = setInterval(()=>{
                    sec -= 0.01;
                    if(sec <= 0) {
                        clearInterval(timer);
                        document.getElementById('self_countdown').innerHTML = "00.00";
                        document.getElementById('self_status').innerHTML = "[SYSTEM DESTROYED]";
                    } else {
                        document.getElementById('self_countdown').innerHTML = sec.toFixed(2);
                    }
                }, 10);
                </script>
                """
                st.components.v1.html(nuke_self_html, height=140)
                
                abort_key = st.text_input("🔑 請輸入核心解碼密鑰終止自毀程序：", type="password", key="abort_nuke_input")
                if abort_key.strip() in ["22", "king1030622"]:
                    st.session_state.active_panel = None
                    st.toast("🛡️ 自毀程序已成功終止，核心防禦矩陣安全回復！", icon="🛡️")
                    st.rerun()

        # --- 5. 引爆核彈 (附帶打字框 + 發射按鈕) ---
        elif st.session_state.active_panel == "nuke_launch":
            with st.container(border=True):
                st.subheader("☢️ [STRATEGIC-NUKE] 洲際彈道導彈打擊終端")
                nuke_target = st.text_input("⌨️ 請輸入洲際彈道飛彈打擊目標國家/城市：", value="莫斯科", key="nuke_target_input")
                
                nl_col1, nl_col2 = st.columns([1, 4])
                with nl_col1:
                    if st.button("🚨 授權發射 (LAUNCH)", use_container_width=True):
                        st.session_state.nuke_detonated = True
                        st.rerun()
                with nl_col2:
                    if st.session_state.nuke_detonated:
                        st.error(f"🚀 戰略導彈已出井！預計打擊座標：{nuke_target.upper()}")
                    else:
                        st.warning("等待最高指揮官按下紅色發射按鈕...")
                        
                nuke_canvas_html = f"""
                <div style="background:#000; padding:10px; border:1px solid #ff0033; border-radius:5px; text-align:center;">
                    <canvas id="nukeCanvas" width="600" height="220" style="background:#0a0102;"></canvas>
                </div>
                <script>
                (function(){{
                    const canvas = document.getElementById('nukeCanvas'); const ctx = canvas.getContext('2d');
                    let isLaunched = { "true" if st.session_state.nuke_detonated else "false" };
                    let px = 50, py = 180; let t = 0;
                    function draw() {{
                        ctx.fillStyle = '#0a0102'; ctx.fillRect(0,0,canvas.width,canvas.height);
                        
                        ctx.strokeStyle = '#331111'; ctx.lineWidth = 2;
                        ctx.beginPath(); ctx.moveTo(0, 180); ctx.lineTo(canvas.width, 180); ctx.stroke();
                        
                        ctx.fillStyle = '#00ff66'; ctx.font = '12px monospace'; ctx.fillText("[LAUNCH_SILO_22]", 20, 200);
                        ctx.fillStyle = '#ff0033'; ctx.fillText("[TARGET: " + "{nuke_target}".toUpperCase() + "]", 480, 200);
                        
                        if(isLaunched) {{
                            t += 0.01;
                            if(t <= 1.0) {{
                                px = 50 + t * 450;
                                py = 180 - Math.sin(t * Math.PI) * 120;
                                ctx.strokeStyle = 'rgba(255, 0, 51, 0.4)'; ctx.setLineDash([4, 4]);
                                ctx.beginPath(); ctx.moveTo(50, 180); ctx.quadraticCurveTo(275, -20, 500, 180); ctx.stroke();
                                ctx.setLineDash([]);
                                
                                ctx.fillStyle = '#ff0033'; ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI*2); ctx.fill();
                            }} else {{
                                ctx.fillStyle = 'rgba(255,0,51,' + (Math.sin(Date.now()/50)+1)/2 + ')';
                                ctx.beginPath(); ctx.arc(500, 180, 40, 0, Math.PI*2); ctx.fill();
                                ctx.fillStyle = '#fff'; ctx.font = 'bold 16px monospace'; ctx.fillText("💥 IMPACT & DETONATED", 220, 100);
                            }}
                        }}
                        requestAnimationFrame(draw);
                    }}
                    draw();
                }})();
                </script>
                """
                st.components.v1.html(nuke_canvas_html, height=250)
                
                if st.button("🔄 重置導彈發射控制台"):
                    st.session_state.nuke_detonated = False
                    st.rerun()

    # 🔑 密碼與指令輸入框
    st.write("")
    with st.container(border=True):
        cmd_input = st.text_input("⌨️ [SYS-OVERRIDE] 核心指令輸入端 :", key="hacker_cmd_terminal", type="password", placeholder="請輸入核心交互密鑰（輸入 king1030622 可啟用終極皇權紅化超頻模式）...")
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
            st.subheader("📰 今日焦點新聞 (模擬日誌)")
            news_list = get_google_news()
            for i, news in enumerate(news_list, 1):
                st.markdown(f"{i}. {news['title']}")

    st.write("") 
    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.container(border=True):
            st.subheader("📝 賽博文書終端 (Word & PPT 整合模組)")
            doc_tab1, doc_tab2 = st.tabs(["📄 Word 編輯模式", "📺 PPT 簡報播放模式"])
            
            doc_content = ""
            if os.path.exists(DOC_FILE):
                try:
                    with open(DOC_FILE, "r", encoding="utf-8") as f: doc_content = f.read()
                except Exception: pass
                
            with doc_tab1:
                st.caption("利用 Markdown 編寫文件，使用 `---` 作為 PPT 的換頁符號。")
                edited_doc = st.text_area("文件編輯器", value=doc_content, height=220, key="word_editor")
                
                w_col1, w_col2, w_col3 = st.columns(3)
                with w_col1:
                    if st.button("💾 儲存最新文本"):
                        try:
                            with open(DOC_FILE, "w", encoding="utf-8") as f: f.write(edited_doc)
                            st.toast("文件已成功寫入核心矩陣！", icon="💾")
                            st.rerun()
                        except Exception as e: st.error(f"寫入失敗: {e}")
                with w_col2: st.download_button("📥 匯出為 .md 檔案", data=edited_doc, file_name="Cyber_Report.md", mime="text/markdown")
                with w_col3: st.download_button("📥 匯出為 Word 格式", data=edited_doc, file_name="Cyber_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    
            with doc_tab2:
                slides = [s.strip() for s in doc_content.split("---") if s.strip()]
                if not slides or doc_content.strip() == "":
                    st.markdown('<div class="ppt-slide-box" style="text-align: center; line-height: 200px; color: #888;">📡 暫與簡報數據</div>', unsafe_allow_html=True)
                else:
                    if st.session_state.ppt_page >= len(slides): st.session_state.ppt_page = len(slides) - 1
                    st.markdown(f'<div class="ppt-slide-box">{slides[st.session_state.ppt_page]}</div>', unsafe_allow_html=True)
                    
                    ppt_ctrl1, ppt_ctrl2, ppt_ctrl3 = st.columns([1, 2, 1])
                    with ppt_ctrl1:
                        if st.button("⬅️ 上一頁") and st.session_state.ppt_page > 0:
                            st.session_state.ppt_page -= 1; st.rerun()
                    with ppt_ctrl2: st.markdown(f"<p style='text-align: center; margin-top: 8px;'>投影片進度: {st.session_state.ppt_page + 1} / {len(slides)}</p>", unsafe_allow_html=True)
                    with ppt_ctrl3:
                        if st.button("下一頁 ➡️") and st.session_state.ppt_page < len(slides) - 1:
                            st.session_state.ppt_page += 1; st.rerun()

        @st.fragment
        def render_sticky_notes():
            with st.container(border=True):
                st.subheader("⚡ 閃電收件匣 (Capture)")
                current_notes = ""
                if os.path.exists(NOTE_FILE):
                    try:
                        with open(NOTE_FILE, "r", encoding="utf-8") as f: current_notes = f.read()
                    except Exception: pass
                user_notes = st.text_area("隨手記下目前的雜念...", value=current_notes, height=100, key="sticky_notes_input")
                if st.button("💾 儲存連接筆記"):
                    try:
                        with open(NOTE_FILE, "w", encoding="utf-8") as f: f.write(user_notes)
                        st.toast("筆記已寫入本地端檔案！", icon="💾")
                    except Exception: pass
        render_sticky_notes()

    with col_right:
        with st.container(border=True):
            st.subheader("🛰️ 軍用即時聲納雷達監控")
            radar_template = """
            <div style="text-align: center; background: __BG__; padding: 10px; border-radius: 8px;">
                <canvas id="militaryRadar" width="360" height="300"></canvas>
            </div>
            <script>
            (function() {
                const canvas = document.getElementById('militaryRadar'); const ctx = canvas.getContext('2d');
                const isHacker = __IS_HACKER__; const sweepSpeed = __SWEEP_SPEED__;
                let bg_color = isHacker ? '#03120E' : '#f7f9fa'; let grid_color = isHacker ? '#004411' : '#d1dbe0';
                let line_color = isHacker ? '#00ebd4' : '#0070f3'; let sweep_color = isHacker ? 'rgba(0, 235, 212, 0.15)' : 'rgba(0, 112, 243, 0.08)';
                let angle = 0; const cx = canvas.width / 2; const cy = canvas.height / 2; const maxRadius = 120;
                const targets = [
                    { name: 'Coding', val: __VAL_CODING__, angle: -Math.PI/2 },
                    { name: 'Focus', val: __VAL_FOCUS__, angle: -Math.PI/2 + (Math.PI*2/5) },
                    { name: 'Learn', val: __VAL_LEARN__, angle: -Math.PI/2 + (Math.PI*2/5)*2 },
                    { name: 'Energy', val: __VAL_ENERGY__, angle: -Math.PI/2 + (Math.PI*2/5)*3 },
                    { name: 'Delivery', val: __VAL_DELIVERY__, angle: -Math.PI/2 + (Math.PI*2/5)*4 }
                ];
                function draw() {
                    ctx.fillStyle = bg_color; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = grid_color; ctx.lineWidth = 1;
                    for(let r = 30; r <= maxRadius; r += 30) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke(); }
                    ctx.beginPath(); ctx.moveTo(cx - maxRadius, cy); ctx.lineTo(cx + maxRadius, cy); ctx.moveTo(cx, cy - maxRadius); ctx.lineTo(cx, cy + maxRadius); ctx.stroke();
                    ctx.beginPath(); targets.forEach((t, i) => { let r = (t.val / 100) * maxRadius; let x = cx + r * Math.cos(t.angle); let y = cy + r * Math.sin(t.angle); if(i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }); ctx.closePath();
                    ctx.strokeStyle = isHacker ? 'rgba(0,255,102,0.6)' : 'rgba(255,75,75,0.6)'; ctx.stroke();
                    ctx.fillStyle = sweep_color; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, maxRadius, angle, angle + 0.4); ctx.closePath(); ctx.fill();
                    ctx.strokeStyle = line_color; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + maxRadius * Math.cos(angle + 0.4), cy + maxRadius * Math.sin(angle + 0.4)); ctx.stroke();
                    angle += sweepSpeed; requestAnimationFrame(draw);
                }
                draw();
            })();
            </script>
            """
            st.components.v1.html(radar_template.replace("__BG__", '#03120E' if is_hacker else '#f7f9fa').replace("__IS_HACKER__", "true" if is_hacker else "false").replace("__SWEEP_SPEED__", "0.04" if st.session_state.pomodoro_active else "0.015").replace("__VAL_CODING__", str(radar_data['Coding'])).replace("__VAL_FOCUS__", str(radar_data['Focus'])).replace("__VAL_LEARN__", str(radar_data['Learn'])).replace("__VAL_ENERGY__", str(radar_data['Energy'])).replace("__VAL_DELIVERY__", str(radar_data['Delivery'])), height=320)

        # 通行閘門
        if is_hacker:
            with st.container(border=True):
                st.subheader("📟 系統事件日誌流 (Execute)")
                cmd_box = st.text_input("🔑 輸入終極通行密碼解鎖全螢幕隱藏控制台：", key="main_hacker_gate", type="password", placeholder="請在此輸入通行密鑰...")
                if cmd_box.strip() in ["22", "king1030622"] and not st.session_state.hacker_console_active:
                    st.session_state.king_unlocked = True; st.session_state.hacker_console_active = True
                    st.success("👑 驗證通過！全域矩陣核心強制覆寫跳轉中..."); st.rerun()
                st.markdown("---")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("🔓 解鎖特工模擬器" if not st.session_state.hacker_simulator_unlocked else "🔒 鎖定模擬器"):
                        st.session_state.hacker_simulator_unlocked = not st.session_state.hacker_simulator_unlocked; st.rerun()
                with btn_col2:
                    if st.button("⚡ 手動進入全螢幕控制台"): st.session_state.hacker_console_active = True; st.rerun()
