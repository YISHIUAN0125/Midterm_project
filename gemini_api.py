from google import genai
from  dotenv import load_dotenv
import os
from auth import login_required
import streamlit as st
from database import db

class  google_genai:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model="gemini-2.0-flash"
    def generate_content(self, contents):
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )
        return response.text


@login_required
def show_google_genai():
    st.subheader("AI 問答")
    
    chat_history = st.container()
    input_area = st.container()
    if "genai" not in st.session_state:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        st.session_state["genai"] = google_genai(api_key)
    genai = st.session_state["genai"]

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Text input
    with input_area:
        user_input = st.text_input("請輸入您的問題...")
        if st.button("提問"):
            if user_input:
                response = genai.generate_content(user_input)
                if response:
                    st.session_state["chat_history"].append((user_input, response))
                    st.rerun()
    
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
        for i, (q, a) in enumerate(st.session_state["chat_history"]):
            st.markdown("---")
            st.write("**您的問題：**")
            st.write(q)
            st.write("**AI 回答：**")
            st.markdown(a)

            if st.button("加入備忘錄", key=f"save_note_{i}"):
                db.add_note(st.session_state.user_id, q, a)
                st.success("✅ 已加入備忘錄！")


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    agent = google_genai(api_key)

    print(agent.generate_content("請問你是誰？"))