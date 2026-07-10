import streamlit as st
import streamlit.components.v1 as components

# 1. 初始化頁面設定
st.set_page_config(page_title="Central Command Center v20.0", page_icon="⚡", layout="wide")

# 強制消除 Streamlit 原生白邊與頁首，改由內部 HTML 控制完整視覺
st.markdown(
    """
    <style>
    [data-testid="stHeader"], footer, #MainMenu {visibility: hidden !important;}
    .stApp {background-color: #000000 !important;}
    .block-container {padding: 0px !important; max-width: 100% !important; margin: 0px !important;}
    iframe { width: 100% !important; height: 100vh !important; display: block !important; border: none !important; }
    body { overflow: hidden !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

# 2. 注入包含「密碼特權、自動噴代碼、C2自訂指令、實用備忘、動態雷達」的究極網頁原始碼
raw_html_code = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Hybrid Command Console</title>
    <style>
        * { box-sizing: border-box; }
        body, html { margin: 0; padding: 0; overflow: hidden; width: 100%; height: 100vh; font-family: "Courier New", monospace; }
        
        /* 預設：賽博白晝風格 (Light Cyberpunk) */
        body.light-theme { background-color: #f1f5f9; color: #0f172a; }
        body.light-theme::before {
            content: " "; display: block; position: fixed; top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(255,255,255,0) 50%, rgba(200,220,240,0.15) 50%);
            z-index: 99999; background-size: 100% 4px; pointer-events: none;
        }
        
        /* 切換：深層夜間黑客風格 (Dark Matrix) */
        body.dark-theme { background-color: #000000; color: #00ff00; }
        body.dark-theme::before {
            content: " "; display: block; position: fixed; top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%);
            z-index: 99999; background-size: 100% 4px; pointer-events: none;
        }

        canvas.bg-matrix { display: none; position: absolute; top: 0; left: 0; z-index: 1; opacity: 0.15; }
        body.dark-theme canvas.bg-matrix { display: block; }

        /* 介面框架佈局 */
        .ui-wrapper { position: absolute; top: 0; left: 0; width: 100%; height: 100vh; z-index: 2; display: flex; flex-direction: column; padding: 25px; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold; }
        body.light-theme .top-bar { border-color: #cbd5e1; }
        body.dark-theme .top-bar { border-color: #00ff00; text-shadow: 0 0 5px #00ff00; }

        .main-content { display: grid; grid-template-columns: 7fr 3fr; gap: 25px; flex: 1; overflow: hidden; }
        .panel { display: flex; flex-direction: column; border: 1px solid; padding: 20px; background: rgba(255,255,255,0.6); backdrop-filter: blur(5px); }
        body.light-theme .panel { border-color: #cbd5e1; background: rgba(255,255,255,0.85); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        body.dark-theme .panel { border-color: #00ff00; background: rgba(0,12,0,0.8); box-shadow: 0 0 15px rgba(0,255,0,0.2); }

        /* 階段一：自動噴代碼主終端 */
        .terminal-screen { flex: 1; overflow-y: auto; white-space: pre-wrap; font-size: 14px; line-height: 1.5; margin-bottom: 10px; padding: 10px; background: rgba(0,0,0,0.03); }
        body.dark-theme .terminal-screen { background: rgba(0,0,0,0.4); color: #33ff33; }
        .cursor { display: inline-block; width: 8px; height: 15px; animation: blink 0.8s infinite; vertical-align: middle; }
        body.light-theme .cursor { background-color: #0f172a; }
        body.dark-theme .cursor { background-color: #00ff00; }
        @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }

        .status-box { font-weight: bold; padding: 8px; border-left: 4px solid; margin: 10px 0; }
        body.light-theme .status-box { background: #e2e8f0; border-color: #3b82f6; }
        body.dark-theme .status-box { background: rgba(0,30,0,0.6); border-color: #00ff00; }
        
        /* 🔒 密碼面板特權優化 (F1 呼叫) */
        #backdoor-modal {
            display: none; position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            padding: 25px; z-index: 10000; text-align: center; border-radius: 4px; border: 2px solid; width: 360px;
        }
        body.light-theme #backdoor-modal { background: #ffffff; border-color: #0f172a; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
        body.dark-theme #backdoor-modal { background: rgba(0,15,0,0.95); border-color: #00ff00; box-shadow: 0 0 30px rgba(0,255,0,0.5); }
        .backdoor-input { width: 100%; padding: 10px; font-size: 20px; text-align: center; margin-top: 15px; font-family: inherit; outline: none; border: 1px solid; }
        body.light-theme .backdoor-input { background: #f8fafc; border-color: #cbd5e1; color: #0f172a; }
        body.dark-theme .backdoor-input { background: #000; border-color: #00ff00; color: #00ff00; }
        
        /* 震動與錯誤動畫 */
        .error-shake { animation: shake 0.1s 4; border-color: #ef4444 !important; }
        @keyframes shake { 0%, 100% { transform: translate(-50%, -50%) scale(1); } 50% { transform: translate(-48%, -49%) scale(1.02); } }
        .screen-shake { animation: t-shake 0.3s; }
        @keyframes t-shake { 0%, 100% { transform: translate(0,0); } 20% { transform: translate(-8px, 5px); } 60% { transform: translate(8px, -5px); } }

        /* 階段二：解鎖後 C2 主控面板 */
        #c2-dashboard { display: none; flex-direction: column; height: 100%; }
        .c2-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 15px; flex: 1; overflow: hidden; }
        .c2-btn { padding: 10px; text-align: left; font-family: inherit; font-weight: bold; cursor: pointer; border: 1px solid; background: transparent; margin-bottom: 8px; }
        body.light-theme .c2-btn { border-color: #0f172a; color: #0f172a; }
        body.light-theme .c2-btn:hover { background: #0f172a; color: #fff; }
        body.dark-theme .c2-btn { border-color: #00ff00; color: #00ff00; }
        body.dark-theme .c2-btn:hover { background: #00ff00; color: #000; box-shadow: 0 0 10px #00ff00; }

        .c2-terminal { display: flex; flex-direction: column; border: 1px solid; padding: 10px; background: #000; color: #00ff00; font-size: 13px; }
        body.light-theme .c2-terminal { border-color: #0f172a; background: #1e293b; color: #38bdf8; }
        .c2-output { flex: 1; overflow-y: auto; margin-bottom: 5px; }
        .c2-input-line { display: flex; gap: 5px; align-items: center; }
        .c2-field { flex: 1; background: transparent; border: none; color: inherit; font-family: inherit; outline: none; border-bottom: 1px solid; }

        /* 右側面板：計時器與雷達 */
        .radar-box { width: 100%; height: 180px; border: 1px solid; margin: 10px 0; background: #000; }
        body.light-theme .radar-box { border-color: #0f172a; }
        body.dark-theme .radar-box { border-color: #00ff00; }
        #radarCanvas { width: 100%; height: 100%; display: block; }

        .theme-toggle-btn { padding: 5px 12px; cursor: pointer; font-family: inherit; font-weight: bold; border: 1px solid; background: transparent; }
        body.light-theme .theme-toggle-btn { border-color: #0f172a; color: #0f172a; }
        body.dark-theme .theme-toggle-btn { border-color: #00ff00; color: #00ff00; }
        
        #hidden-trigger { position: absolute; left: -9999px; }
        .memo-area { width: 100%; height: 120px; font-family: inherit; padding: 8px; border: 1px solid; background: transparent; color: inherit; resize: none; }
    </style>
</head>
<body class="light-theme">
    <canvas id="matrixCanvas" class="bg-matrix"></canvas>
    <input type="text" id="hidden-trigger" autofocus>

    <div id="backdoor-modal">
        <div style="font-weight:bold; font-size:14px;">⚠️ [OVERRIDE BYPASS SYSTEM]</div>
        <div style="font-size:11px; opacity:0.7; margin-top:4px;">請輸入特權金鑰以直接強制解鎖終端</div>
        <input type="password" id="backdoor-field" class="backdoor-input" placeholder="••••" maxlength="7" onkeydown="handleBackdoor(event)">
        <div style="font-size:11px; margin-top:12px; color:#ef4444; font-weight:bold;">[ ESC 取消 ]</div>
    </div>

    <div class="ui-wrapper" id="main-wrapper">
        <div class="top-bar">
            <span id="title-text">⚡ CENTRAL MULTI-MODE CONSOLE v20.0</span>
            <button class="theme-toggle-btn" onclick="toggleTheme()">切換模式 🔄</button>
        </div>

        <div class="main-content">
            <div class="panel" id="left-panel">
                <div id="phase1-terminal" style="display:flex; flex-direction:column; height:100%;">
                    <div style="font-weight:bold; margin-bottom:5px;">💻 終端協議核心注入口 (鍵盤敲擊任意鍵開始自動刻碼)</div>
                    <div class="terminal-screen" id="term-screen">💡 系統就緒。請在畫面上任意打字，或按下 [ F1 ] 開啟特權密碼解鎖通道...<br><br></div>
                    <div class="status-box" id="status-bar">目前進度: [ 🧭 PHASE 1: 初始化核心解密流... ] [0%]</div>
                    <div style="font-size:12px; opacity:0.7;">提示：當進度達到 100% 時，系統將自動授權對接 C2 控制台。</div>
                </div>

                <div id="c2-dashboard">
                    <div style="font-weight:bold; font-size:18px; margin-bottom:15px; color:#ef4444;">💀 [GHOST-NETWORK CENTRAL C2 ACCESS GRANTED]</div>
                    <div class="c2-grid">
                        <div style="display:flex; flex-direction:column;">
                            <div style="font-size:12px; font-weight:bold; margin-bottom:5px;">[ 戰略特權指令快捷 ]</div>
                            <button class="c2-btn" onclick="runC2Action('dump')">📂 數據導出 (Dump)</button>
                            <button class="c2-btn" onclick="runC2Action('scan')">🔍 漏洞掃描 (Scan)</button>
                            <button class="c2-btn" onclick="runC2Action('clear')">🧹 清除緩衝 (Clear)</button>
                            <div style="margin-top:auto; font-size:11px; opacity:0.8;">狀態: SECURE CONNECTION<br>NODE: LOCALHOST//STREAMLIT</div>
                        </div>
                        <div class="c2-terminal">
                            <div class="c2-output" id="c2-out-box">
                                [SYSTEM] 成功接通主鏈。可在下方鍵入自訂控制台指令。<br>
                                💡 輸入 <span style="font-weight:bold; text-decoration:underline;">help</span> 檢視全新自訂指令集。
                            </div>
                            <div class="c2-input-line">
                                <span>c2-admin#</span>
                                <input type="text" class="c2-field" id="c2-field-input" onkeydown="handleC2Cmd(event)">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div style="font-weight:bold; margin-bottom:5px;">⏱️ 任務進度與追蹤</div>
                <button class="c2-btn" style="width:100%; text-align:center;" onclick="startFocusTimer()">⏱️ 開始 25 分鐘專注</button>
                <div id="timer-status" style="font-size:12px; text-align:center; margin-top:5px; font-weight:bold;"></div>
                
                <div style="font-weight:bold; margin-top:20px; margin-bottom:5px;">🛰️ 軌道衛星下行解碼雷達</div>
                <div class="radar-box">
                    <canvas id="radarCanvas"></canvas>
                </div>
                
                <div style="font-weight:bold; margin-top:15px; margin-bottom:5px;">📓 隨手工作便利貼</div>
                <textarea class="memo-area" placeholder="在此記錄臨時的靈感、待辦事項、或者拖庫回傳的金鑰密碼..." id="memo-field"></textarea>
            </div>
        </div>
    </div>

    <script>
        // 1. 主題切換邏輯
        function toggleTheme() {
            var body = document.body;
            if(body.classList.contains("light-theme")) {
                body.classList.remove("light-theme"); body.classList.add("dark-theme");
            } else {
                body.classList.remove("dark-theme"); body.classList.add("light-theme");
            }
        }

        // 2. 數字雨動畫引擎
        var mCanvas = document.getElementById("matrixCanvas"); var mCtx = mCanvas.getContext("2d");
        mCanvas.width = window.innerWidth; mCanvas.height = window.innerHeight;
        var alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ💀🛰️🔥".split("");
        var columns = mCanvas.width / 16; var rainDrops = Array(Math.floor(columns)).fill(1);
        function drawMatrix() {
            mCtx.fillStyle = "rgba(0, 0, 0, 0.05)"; mCtx.fillRect(0, 0, mCanvas.width, mCanvas.height);
            mCtx.fillStyle = "#0F0"; mCtx.font = "16px monospace";
            for (var i = 0; i < rainDrops.length; i++) {
                var text = alphabet[Math.floor(Math.random() * alphabet.length)];
                mCtx.fillText(text, i * 16, rainDrops[i] * 16);
                if (rainDrops[i] * 16 > mCanvas.height && Math.random() > 0.975) rainDrops[i] = 0;
                rainDrops[i]++;
            }
        }
        setInterval(drawMatrix, 33);

        // 3. 科技動態雷達掃描引擎 (100% 純 Canvas 修正，絕不跳錯)
        var rCanvas = document.getElementById("radarCanvas"); var rCtx = rCanvas.getContext("2d");
        rCanvas.width = 300; rCanvas.height = 180;
        var angle = 0;
        function drawRadar() {
            rCtx.fillStyle = "rgba(0, 8, 0, 0.15)"; rCtx.fillRect(0, 0, 300, 180);
            var cx = 150, cy = 90;
            rCtx.strokeStyle = "rgba(0, 255, 0, 0.3)";
            for(var r=25; r<=75; r+=25) { rCtx.beginPath(); rCtx.arc(cx, cy, r, 0, Math.PI*2); rCtx.stroke(); }
            rCtx.beginPath(); rCtx.moveTo(cx-90, cy); rCtx.lineTo(cx+90, cy); rCtx.moveTo(cx, cy-75); rCtx.lineTo(cx, cy+75); rCtx.stroke();
            
            var bx = cx + Math.cos(angle)*85; var by = cy + Math.sin(angle)*85;
            var grad = rCtx.createLinearGradient(cx, cy, bx, by);
            grad.addColorStop(0, "rgba(0,255,0,0.6)"); grad.addColorStop(1, "rgba(0,255,0,0)");
            rCtx.strokeStyle = grad; rCtx.lineWidth = 2.5; rCtx.beginPath(); rCtx.moveTo(cx, cy); rCtx.lineTo(bx, by); rCtx.stroke();
            angle += 0.04;
        }
        setInterval(drawRadar, 33);

        // 4. 音效產生器
        var audioCtx = null;
        function playSound(freq, duration) {
            try {
                if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                var osc = audioCtx.createOscillator(); var gain = audioCtx.createGain();
                osc.type = "sine"; osc.frequency.value = freq;
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        // 5. 瘋狂自動打字噴代碼邏輯
        var termScreen = document.getElementById("term-screen");
        var statusBar = document.getElementById("status-bar");
        var lines = 0; var maxLines = 120; var isUnlocked = false;

        function appendFakeCode() {
            if(isUnlocked) return;
            lines++;
            if(Math.random() < 0.03) {
                playSound(150, 0.2);
                document.getElementById("main-wrapper").classList.add("screen-shake");
                setTimeout(function(){ document.getElementById("main-wrapper").classList.remove("screen-shake"); }, 300);
                termScreen.innerHTML += "<span style='color:#ef4444; font-weight:bold;'>[ALERT] 防禦性防火牆攔截阻斷，正在切換異步跳板節點...</span><br>";
            } else {
                termScreen.innerHTML += "[SYSTEM_CORE] 進程流導向記憶體區塊 0x" + Math.random().toString(16).substring(2,10).toUpperCase() + " | 對接狀態: SUCCESS<br>";
            }
            termScreen.scrollTop = termScreen.scrollHeight;
            
            var pct = Math.floor((lines/maxLines)*100);
            if(pct >= 100) { pct = 100; unlockC2(); }
            statusBar.textContent = "目前進度: [ ⚡ PHASE " + (Math.floor(pct/25)+1) + " : 協議核心爆破中... ] [" + pct + "%]";
        }

        function unlockC2() {
            isUnlocked = true; playSound(880, 0.4);
            document.getElementById("phase1-terminal").style.display = "none";
            document.getElementById("backdoor-modal").style.display = "none";
            document.getElementById("c2-dashboard").style.display = "flex";
            document.getElementById("c2-field-input").focus();
        }

        // 監聽鍵盤（任意鍵噴代碼，F1 開密碼面板）
        document.addEventListener("keydown", function(e) {
            if(e.key === "F1") {
                e.preventDefault(); if(!isUnlocked) { document.getElementById("backdoor-modal").style.display = "block"; document.getElementById("backdoor-field").focus(); }
                return;
            }
            if(document.activeElement === document.getElementById("backdoor-field") || document.activeElement === document.getElementById("c2-field-input") || document.activeElement === document.getElementById("memo-field")) return;
            if(!isUnlocked && e.key !== "Shift" && e.key !== "Control" && e.key !== "Alt") {
                for(var i=0; i<4; i++) appendFakeCode();
            }
        });

        // 6. 🔒 密碼面板特權密碼驗證
        function handleBackdoor(e) {
            if(e.key === "Enter") {
                var field = document.getElementById("backdoor-field");
                if(field.value === "1030622") {
                    unlockC2();
                } else {
                    playSound(100, 0.4);
                    document.getElementById("backdoor-modal").classList.add("error-shake");
                    field.value = "";
                    setTimeout(function(){ document.getElementById("backdoor-modal").classList.remove("error-shake"); }, 500);
                }
            } else if(e.key === "Escape") {
                document.getElementById("backdoor-field").value = "";
                document.getElementById("backdoor-modal").style.display = "none";
                document.getElementById("hidden-trigger").focus();
            }
        }

        // 7. C2 自訂內部黑客指令集
        var c2Out = document.getElementById("c2-out-box");
        function logC2(text) {
            var p = document.createElement("div"); p.style.margin = "3px 0"; p.innerHTML = text;
            c2Out.appendChild(p); c2Out.scrollTop = c2Out.scrollHeight;
        }

        function handleC2Cmd(e) {
            if(e.key === "Enter") {
                var input = document.getElementById("c2-field-input");
                var raw = input.value.trim(); var cmd = raw.toLowerCase();
                if(!cmd) return;
                logC2("<span style='color:#fff;'>c2-admin# " + raw + "</span>");
                input.value = "";
                
                if(cmd === "help") {
                    logC2("<span style='color:#eab308;'>==== 內部特權自訂指令集 ====</span>");
                    logC2("<b>scan</b>    - 啟動全網段深度漏洞掃描");
                    logC2("<b>dump</b>    - 導出本地快取密鑰數據庫");
                    logC2("<b>sysinfo</b> - 讀取伺服器底層核心架構");
                    logC2("<b>clear</b>   - 清除終端緩衝螢幕");
                } else if(cmd === "scan") { runC2Action("scan"); }
                else if(cmd === "dump") { runC2Action("dump"); }
                else if(cmd === "clear") { runC2Action("clear"); }
                else if(cmd === "sysinfo") {
                    playSound(500, 0.05); logC2("OS: Streamlit Distributed Linux 5.15"); logC2("ARCH: x86_64 Core-Matrix v20");
                } else {
                    logC2("<span style='color:#ef4444;'>[!] 未知指令。輸入 'help' 獲取支援。</span>");
                }
            }
        }

        function runC2Action(action) {
            if(action === "clear") { c2Out.innerHTML = ""; return; }
            if(action === "scan") {
                playSound(700, 0.1); logC2("[+] 正在初始化漏洞探測模組...");
                setTimeout(function(){ logC2("[-] 發現緩衝區溢位弱點於 port 80 [CVE-2026-9999]"); }, 500);
            }
            if(action === "dump") {
                playSound(900, 0.15); logC2("[+] 導出密鑰緩衝區...");
                setTimeout(function(){ logC2("[DUMP] ADMIN_HASH: 8C6976E5B5410415BDE908BD4DEE15DF"); }, 400);
            }
        }

        // 8. 右側實用專注進度條模擬
        function startFocusTimer() {
            var btnStatus = document.getElementById("timer-status");
            btnStatus.textContent = "⏳ 專注時間推進中 (模擬倒數)...";
            setTimeout(function(){ btnStatus.textContent = "🎉 專注時段結束！幹得好！"; playSound(600, 0.5); }, 3000);
        }

        document.addEventListener("click", function(e) {
            if(document.getElementById("backdoor-modal").contains(e.target) || document.getElementById("memo-field").contains(e.target) || document.getElementById("c2-field-input").contains(e.target)) return;
            if(!isUnlocked) document.getElementById("hidden-trigger").focus();
        });
        setTimeout(function(){ document.getElementById("hidden-trigger").focus(); }, 300);
    </script>
</body>
</html>
"""

# 將完全體網頁注入 Streamlit 容器
components.html(raw_html_code, height=850)
