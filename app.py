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
        .backdoor-input {
