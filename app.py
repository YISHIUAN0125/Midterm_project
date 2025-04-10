import streamlit as st
import atexit
from database import Database
from auth import show_login, show_register
import pandas as pd
from gemini_api import google_genai
from  dotenv import load_dotenv
import os

# Initialize the database connection
if 'db' not in st.session_state:
    st.session_state['db'] = Database()
db = st.session_state['db']

# Session state for user login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "genai" not in st.session_state:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    st.session_state["genai"] = google_genai(api_key)
genai = st.session_state["genai"]

# Initialize data_editor_selected_rows
if "data_editor_selected_rows" not in st.session_state:
    st.session_state["data_editor_selected_rows"] = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# If not logged in, show login/register page
if not st.session_state["logged_in"]:
    st.sidebar.title("🔐 登入系統")
    page = st.sidebar.radio("選擇操作", ["登入", "註冊"])

    if page == "登入":
        show_login()
    else:
        show_register()
    st.stop()

# Login successful, set session state
with st.container():
    col1, col2 = st.columns([8, 3])  # Adjust column widths as needed
    with col2:
        with st.expander(f"👤 歡迎，{st.session_state['username']}！", expanded=False):
            if st.button("🚪 登出"):
                st.session_state["logged_in"] = False
                st.rerun()

st.session_state["user_id"] = db.get_user_id(st.session_state["username"])[0]

st.title("🙂 Personal Schedule Management")

tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 問答", "📋 To-Do List", "📚 文獻管理", "📝備忘錄"])


# AI chatbot
with tab1:
    st.subheader("💬 AI 問答")
    
    chat_history = st.container()
    input_area = st.container()
    
    # Text input
    with input_area:
        user_input = st.text_input("請輸入您的問題...")
        if st.button("🤖 提問"):
            if user_input:
                response = genai.generate_content(user_input)
                if response:
                    st.session_state["chat_history"].append((user_input, response))
                    st.rerun()
                else:
                    st.markdown("**AI 回答：** 我無法回答這個問題，請稍後再試。")
            else:
                st.warning("請輸入問題！")
    
    # Chat history
    with chat_history:
        # Set the height of the chat history container
        st.markdown("""
            <style>
                [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
                    max-height: 400px;
                    overflow-y: auto;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 2rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Display chat history
        for q, a in st.session_state["chat_history"]:
            st.markdown("---")
            st.write("❓ **您的問題：**")
            st.write(q)
            st.write("🤖 **AI 回答：**")
            st.markdown(a)


# To-Do List
with tab2:
    st.subheader("📋 新增待辦事項")
    task = st.text_input("新增任務")
    if st.button("➕ 新增"):
        db.add_todo(st.session_state["user_id"], task)
        st.rerun()
    st.sidebar.write("✏️以下是最新代辦事項：")
    for todo_id, task, completed in db.get_todos(st.session_state["user_id"]):
        col1, col2 = st.sidebar.columns([1, 3])
        with col1:
            if st.button("✔️", key=f"done_{todo_id}", disabled=completed):
                db.delete_todo(todo_id, task)
                st.rerun()
        with col2:
            st.markdown(f"<span style='font-size:20px;'>{task}</span>", unsafe_allow_html=True)

# Literature Management
with tab3:
    st.subheader("📚 我的研究文獻")
    title = st.text_input("標題", key="title")
    author = st.text_input("作者", key="author")
    date = st.date_input("日期", key="date")
    abstract = st.text_area("摘要", key="abstract")

    if st.button("📥 儲存"):
        db.add_literature(st.session_state["user_id"], str(date), title, author, abstract)
        st.rerun()

    # Fetch literature data
    literature = db.get_literature(st.session_state["user_id"])
    if literature:
        df = pd.DataFrame(literature, columns=["id", "Date", "Title", "Author", "Abstract"])
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        def delete_literature(literature_id):
            db.delete_literature(literature_id)
            st.rerun()

        df['selected'] = False

        # Display the data editor with the literature data
        edited_df = st.data_editor(
            df,
            column_config={
                "id": None,
                "Date": st.column_config.DateColumn("日期"),
                "Title": st.column_config.TextColumn("標題"),
                "Author": st.column_config.TextColumn("作者"),
                "Abstract": st.column_config.TextColumn("摘要"),
                "selected": st.column_config.CheckboxColumn("選取", default=False),
            },
            disabled=["id"],
            hide_index=True,
            key="data_editor",
        )

        # Delete selected literature
        selected_rows = edited_df[edited_df['selected'] == True]
        if not selected_rows.empty:
            if st.button("🗑️ 刪除所選文獻"):
                for idx, row in selected_rows.iterrows():
                    delete_literature(row['id'])
                st.rerun()
    else:
        st.write("目前沒有文獻。")


# Close database connection when the app is closed
@atexit.register
def cleanup():
    if 'db' in st.session_state:
        db.close()
    print("✅ Database connection closed")