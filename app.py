import streamlit as st
import pandas as pd
import time
from datetime import datetime
import streamlit.components.v1 as components

# 1. 初始化全域設定
st.set_page_config(page_title="Dual Workspace v2.0", page_icon="💼", layout="wide")

# 初始化資料狀態，避免切換模式時資料不見
if "todos" not in st.session_state:
    st.session_state.todos = [{"task": "📄 閱讀專案報告", "done": False}]
if "notes" not in st.session_state:
    st.session_state.notes = ""

# 2. 側邊欄：切換網頁風格風格
st.sidebar.title("🎛️ 控制面板")
web_mode = st.sidebar.radio("切換網頁模式", ["白晝高效模式 💼", "極客夜間模式 💀"])

# ==========================================================
# 模式一：白晝高效模式（你剛剛成功做出來的超讚介面！）
# ==========================================================
if web_mode == "白晝高效模式 💼":
    st.markdown("# 💼 高效個人工作台")
    st.caption(f"今天是 {datetime.now().strftime('%Y-%m-%d')} │ 專注當下。")
    st.markdown("---")

    col_left, col_right = st.columns([7, 3], gap="large")

    with col_left:
        st.markdown("### 📝 今日待辦事項")
        with st.form("todo_form", clear_on_submit=True):
            col_input, col_btn = st.columns([5, 1])
            with col_input:
                new_todo = st.text_input("", placeholder="準備下午的簡報...", label_visibility="collapsed")
            with col_btn:
                submit_todo = st.form_submit_button("新增", use_container_width=True)
            if submit_todo and new_todo.strip():
                st.session_state.todos.append({"task": new_todo.strip(), "done": False})
                st.rerun()

        if st.session_state.todos:
            updated_todos = []
            for i, todo in enumerate(st.session_state.todos):
                col_check, col_text = st.columns([1, 25])
                with col_check:
                    is_done = st.checkbox("", value=todo["done"], key=f"todo_{i}")
                with col_text:
                    if is_done:
                        st.markdown(f"~~{todo['task']}~~")
                    else:
                        st.markdown(f"**{todo['task']}**")
                updated_todos.append({"task": todo["task"], "done": is_done})
            st.session_state.todos = updated_todos

        if st.button("🧹 清除已完成事項"):
            st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]
            st.rerun()

    with col_right:
        st.markdown("### ⏱️ 專注計時器")
        if st.button("⏱️ 開始 25 分鐘專注", use_container_width=True, type="primary"):
            bar = st.progress(0, text="專注中...")
            for p in range(100):
                time.sleep(0.05)  # 快速展示模擬
                bar.progress(p + 1, text="專注中...")
            st.balloons()
            st.success("🎉 結束！休息一下吧！")
            
        st.markdown("---")
        st.markdown("### 📓 隨手便利貼")
        memo = st.text_area("寫點什麼...", value=st.session_state.notes, height=200, label_visibility="collapsed")
        st.session_state.notes = memo

# ==========================================================
# 模式二：極客夜間模式（完美修復影片錯誤與語法錯誤的雷達！）
# ==========================================================
else:
    # 透過 HTML/CSS 蓋掉 Streamlit 原本的白底，注入純黑客環境
    st.markdown(
        """
        <style>
        [data-testid="stHeader"], footer, #MainMenu {visibility: hidden !important;}
        .stApp {background-color: #000000 !important;}
        .block-container {padding: 0px !important; max-width: 100% !important; margin: 0px !important;}
        iframe { width: 100% !important; height: 85vh !important; display: block !important; border: none !important; }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # 這裡面完全使用純 Canvas 畫出科技感雷達與數字雨，彻底避免 YouTube 阻擋嵌入的問題！
    hacker_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body, html { margin: 0; padding: 0; background-color: #000; overflow: hidden; width: 100%; height: 100vh; font-family: monospace; }
            canvas.bg-matrix { display: block; position: absolute; top: 0; left: 0; z-index: 1; opacity: 0.15; }
            #control-panel { position: absolute; top: 0; left: 0; width: 100%; height: 100vh; z-index: 2; text-align: center; padding-top: 2vh; color: #00ff00; }
            .radar-box { position: relative; width: 550px; height: 320px; margin: 20px auto; border: 2px solid #00ff00; box-shadow: 0 0 25px rgba(0,255,0,0.5); background: #000; }
            #radarCanvas { width: 100%; height: 100%; display: block; }
            .p-bar { width: 60%; margin: 15px auto; border: 1px solid #00ff00; padding: 2px; }
            .p-fill { height: 18px; background: #00ff00; width: 0%; }
        </style>
    </head>
    <body>
        <canvas id="matrixCanvas" class="bg-matrix"></canvas>
        
        <div id="control-panel">
            <div style="font-size: 22px; font-weight: bold; letter-spacing: 2px;">🛰️ [ORBITAL SATELLITE HIJACK PROTOCOL]</div>
            <div style="font-size: 13px; color: #00aa00; margin-top: 5px;">正在強制劫持下行微波，聲頻與光學雷達影像實時解碼中...</div>
            
            <div class="radar-box">
                <canvas id="radarCanvas"></canvas>
            </div>
            
            <div class="p-bar"><div id="fill" class="p-fill"></div></div>
            <div id="text" style="font-size: 18px; font-weight: bold;">0%</div>
            
            <div id="log-box" style="font-size: 13px; color: #33ff33; text-align: left; width: 60%; margin: 10px auto; height: 60px; overflow-y: auto; line-height: 1.4;">
                &gt;&gt; 正在初始化全網段監聽機制...<br>
            </div>
        </div>

        <script>
            // 1. 數字雨動畫
            var mCanvas = document.getElementById("matrixCanvas"); var mCtx = mCanvas.getContext("2d");
            mCanvas.width = window.innerWidth; mCanvas.height = window.innerHeight;
            var alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ💀🛰️🔥⚡".split("");
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

            // 2. 完美的動態科技雷達
            var rCanvas = document.getElementById("radarCanvas"); var rCtx = rCanvas.getContext("2d");
            rCanvas.width = 550; rCanvas.height = 320;
            var angle = 0;
            function drawRadar() {
                rCtx.fillStyle = "rgba(0, 8, 0, 0.15)"; rCtx.fillRect(0, 0, 550, 320);
                var cx = 275, cy = 160;
                rCtx.strokeStyle = "rgba(0, 255, 0, 0.25)";
                for(var r=40; r<=120; r+=40) { rCtx.beginPath(); rCtx.arc(cx, cy, r, 0, Math.PI*2); rCtx.stroke(); }
                rCtx.beginPath(); rCtx.moveTo(cx-160, cy); rCtx.lineTo(cx+160, cy); rCtx.moveTo(cx, cy-130); rCtx.lineTo(cx, cy+130); rCtx.stroke();
                
                var bx = cx + Math.cos(angle)*150; var by = cy + Math.sin(angle)*150;
                var grad = rCtx.createLinearGradient(cx, cy, bx, by);
                grad.addColorStop(0, "rgba(0,255,0,0.6)"); grad.addColorStop(1, "rgba(0,255,0,0)");
                rCtx.strokeStyle = grad; rCtx.lineWidth = 3; rCtx.beginPath(); rCtx.moveTo(cx, cy); rCtx.lineTo(bx, by); rCtx.stroke();
                angle += 0.04;
            }
            setInterval(drawRadar, 33);

            // 3. 進度與模擬日誌
            var pct = 0; var fill = document.getElementById("fill"); var txt = document.getElementById("text"); var log = document.getElementById("log-box");
            var timer = setInterval(function() {
                pct += 1; if(pct > 100) { pct = 100; clearInterval(timer); log.innerHTML += "<br><span style='color:#fff;'>[SUCCESS] 戰略控制鏈架設完畢，即時數據包穩定封裝。</span>"; }
                fill.style.width = pct + "%"; txt.textContent = pct + "%";
                if(pct == 30) log.innerHTML += "&gt;&gt; 正在解鎖光學訊號通道... [OK]<br>";
                if(pct == 65) log.innerHTML += "&gt;&gt; 目標衛星精準鎖定：LAT 23.58°N / LNG 120.58°E<br>";
                log.scrollTop = log.scrollHeight;
            }, 60);
        </script>
    </body>
    </html>
    """
    components.html(hacker_html, height=750)
