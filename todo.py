import streamlit as st
from database import db
from auth import login_required

@login_required
def show_todos_tab():
    st.session_state["user_id"] = db.get_user_id(st.session_state["username"])[0]
    st.subheader("新增待辦事項")
    task = st.text_input("新增任務")
    if st.button("新增"):
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