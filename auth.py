import streamlit as st
from database import Database

db = Database()

def show_login():
    st.subheader("🔑 使用者登入")

    username = st.text_input("使用者名稱")
    password = st.text_input("密碼", type="password")

    if st.button("登入"):
        user_id = db.authenticate_user(username, password)
        if user_id:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("❌ 登入失敗，請檢查帳號或密碼")

def show_register():
    st.subheader("🆕 註冊新帳號")

    username = st.text_input("使用者名稱", key="register_username")
    password = st.text_input("密碼", type="password", key="register_password")

    if st.button("註冊"):
        if db.create_user(username, password):
            st.success("✅ 註冊成功，請登入！")
        else:
            st.error("⚠️ 帳號已存在，請換個名稱！")
