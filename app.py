import streamlit as st
from auth import User
from todo import show_todos_tab
from gemini_api import show_google_genai
from literature import show_literature

user = User()
st.set_page_config(page_title="AI Research Companion", layout="wide")

# Login check
if st.session_state["logged_in"] == False:
    page = st.sidebar.radio("選擇頁面", ["🔐 登入", "📝 註冊"])
    if page == "🔐 登入":
        user.show_login()
    else:
        user.show_register()
    st.stop()

with st.container():
    col1, col2 = st.columns([8, 3])  # Adjust column widths as needed
    with col2:
        with st.expander(f"👤 歡迎，{st.session_state['username']}！", expanded=False):
            if st.button("🚪 登出"):
                st.session_state["logged_in"] = False
                st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["📜 備忘錄", "✅ 待辦事項", "📖 文獻管理"])

with tab1:
    show_google_genai()

with tab2:
    show_todos_tab()

with tab3:
    show_literature()
