import streamlit as st
from auth import User
from todo import show_todos_tab
from gemini_api import show_google_genai
from literature import show_literature
from note import show_notes_tab

user = User()
st.set_page_config(page_title="AI Research Companion", layout="wide")

# Login check
st.session_state["logged_in"] == False
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
tab1, tab2, tab3, tab4 = st.tabs(["AI問答", "待辦事項", "備忘錄", "文獻管理"])

with tab1:
    show_google_genai()

with tab2:
    show_todos_tab()

with tab3:
    show_notes_tab()

with tab4:
    show_literature()