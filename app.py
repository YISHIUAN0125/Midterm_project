import streamlit as st
import atexit
from database import Database
from auth import show_login, show_register
import pandas as pd

# 初始化資料庫
if 'db' not in st.session_state:
    st.session_state['db'] = Database()
db = st.session_state['db']

# 確保 Session State 追蹤登入狀態
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 初始化 data_editor_selected_rows
if "data_editor_selected_rows" not in st.session_state:
    st.session_state["data_editor_selected_rows"] = []

# 如果未登入，顯示登入 / 註冊介面
if not st.session_state["logged_in"]:
    st.sidebar.title("🔐 登入系統")
    page = st.sidebar.radio("選擇操作", ["登入", "註冊"])

    if page == "登入":
        show_login()
    else:
        show_register()
    st.stop()

# **已登入**
st.sidebar.write(f"👤 歡迎，{st.session_state['username']}！")
if st.sidebar.button("🚪 登出"):
    st.session_state["logged_in"] = False
    st.rerun()

st.session_state["user_id"] = db.get_user_id(st.session_state["username"])[0]

st.title("🙂 Personal Schedule Management")

tab1, tab2, tab3 = st.tabs(["💬 AI 問答", "📋 To-Do List", "📚 文獻管理"])


# **💬 AI 問答**

# **📋 To-Do List**
with tab2:
    st.subheader("📋 待辦事項")
    task = st.text_input("新增任務")
    if st.button("➕ 新增"):
        db.add_todo(st.session_state["user_id"], task)
        st.rerun()

    for todo_id, task, completed in db.get_todos(st.session_state["user_id"]):
        st.checkbox(task, value=bool(completed), key=str(todo_id))

# **📚 文獻管理**
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

        # 顯示資料表格
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

        # 處理刪除功能
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