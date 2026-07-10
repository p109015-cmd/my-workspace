import streamlit as st
import plotly.graph_objects as go

# --- 1. 網頁基本設定 (必須是第一個 Streamlit 指令) ---
st.set_page_config(
    page_title="高效個人工作台",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 側邊欄導覽 ---
with st.sidebar:
    st.title("⚡ 導覽選單")
    st.markdown("---")
    page = st.radio(
        "切換功能模組",
        ["📊 狀態儀表板", "📝 任務管理", "🎯 目標追蹤", "⚙️ 系統設定"]
    )
    st.markdown("---")
    st.caption("高效個人工作台 v2.0 • 2026")

# --- 3. 主畫面內容 ---
if page == "📊 狀態儀表板":
    st.title("📊 個人狀態儀表板")
    st.subheader("今日核心能力雷達指標")
    
    # 填入你的能力數值（可自行調整 0 ~ 100）
    # 順序：專案執行力, 程式開發, 資訊吸收, 身心健康, 時間管理
    # 註：最後一個數字必須與第一個相同 (80)，圖形才會閉合
    categories = ['專案執行力', '程式開發', '資訊吸收', '身心健康', '時間管理']
    values = [80, 85, 70, 75, 65, 80] 
    categories_closed = categories + [categories[0]]

    # 建立 Plotly 雷達圖
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.25)',  # 半透明螢光藍紫
        line=dict(color='rgba(129, 140, 248, 1)', width=2.5), # 亮螢光藍線條
        marker=dict(color='rgba(129, 140, 248, 1)', size=7),
        name='目前狀態'
    ))

    # 極致暗黑風格設定
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(16, 22, 35, 1)',  # 深色背景
            angularaxis=dict(
                tickfont=dict(size=14, color='#F3F4F6', family="Microsoft JhengHei"), # 文字標籤改白
                linewidth=1,
                linecolor='rgba(255, 255, 255, 0.15)'
            ),
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='rgba(255, 255, 255, 0.4)'), # 數字刻度半透明
                gridcolor='rgba(255, 255, 255, 0.08)',          # 網格線
                linecolor='rgba(255, 255, 255, 0.15)',
            )
        ),
        paper_bgcolor='rgba(16, 22, 35, 1)',  # 畫布外圍背景
        showlegend=False,
        width=550,
        height=550,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # 在網頁上置中呈現雷達圖
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig, use_container_width=True)

elif page == "📝 任務管理":
    st.title("📝 任務管理系統")
    st.info("這裡可以串接你的待辦事項清單或 Notion 數據庫。")

elif page == "🎯 目標追蹤":
    st.title("🎯 核心目標追蹤")
    st.info("追蹤季目標（OKR）或長期專案進度。")

elif page == "⚙️ 系統設定":
    st.title("⚙️ 工作台設定")
    st.success("工作台正常運行中，已成功套用 Plotly 暗黑雷達圖組件。")
