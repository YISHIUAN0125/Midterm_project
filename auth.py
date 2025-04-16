import streamlit as st
from database import Database, AuthUtils

def login_required(func):
    def wrapper(*args, **kwargs):
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            st.warning("請先登入！")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

class User:
    st.session_state["logged_in"] = False
    def __init__(self):
        self.db = Database()
    def show_login(self):
        st.subheader("🔑 使用者登入")

        username = st.text_input("使用者名稱")
        password = st.text_input("密碼", type="password")

        if st.button("登入"):
            user_id = self.db.authenticate_user(username, password)
            if user_id:
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("❌ 登入失敗，請檢查帳號或密碼")

    def show_register(self):
        st.subheader("🆕 註冊新帳號")

        username = st.text_input("使用者名稱", key="register_username")
        password = st.text_input("密碼", type="password", key="register_password")

        if st.button("註冊"):
            try:
                assert AuthUtils.is_valid_username(username), "使用者名稱不可為空"
                assert AuthUtils.is_valid_password(password), "密碼至少4字元且由英文及數字組成"
                user_id = self.db.create_user(username, password)
                if user_id:
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                    st.success("註冊成功！")
                    st.balloons()
            except AssertionError as e:
                st.error(f"❌ {e}")
