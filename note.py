import streamlit as st
import copy
from database import db
from auth import login_required
from gemini_api import google_genai, load_dotenv, os

@login_required
def show_notes_tab():
    st.subheader("我的備忘錄")

    user_input = st.text_area("輸入問題或筆記")

    if st.button("儲存筆記"):
        db.add_note(st.session_state.user_id, user_input, " ")
        st.success("筆記已儲存！")
        st.rerun()

    st.markdown("---")
    st.markdown("### 歷史筆記")
    notes = db.get_notes(st.session_state.user_id)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "genai" not in st.session_state:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        st.session_state["genai"] = google_genai(api_key)
    genai = st.session_state["genai"]

    for note_id, user_input, llm_response in notes:
        with st.expander(user_input[:30] + "..."):
            st.markdown(f"**輸入內容：**\n{user_input}")
            st.markdown(f"**回應內容：**\n{llm_response}")

            col1, col2, col3 = st.columns([0.3, 0.3, 0.4])
            with col1:
                if st.button("刪除", key=f"del_{note_id}"):
                    db.delete_note(note_id)
                    st.rerun()
            with col2:
                if st.button("複製為新筆記", key=f"copy_{note_id}"):
                    original = list(db.get_origin_note(note_id)[0]) 
                    if original:
                        _, input_copy, response_copy = copy.deepcopy(original)
                        db.add_note(st.session_state.user_id, input_copy, response_copy)
                        st.success("✅ 筆記已複製！")
                        st.rerun()
            with col3:
                if st.button("交由 LLM 重新回答", key=f"load_{note_id}"):
                    response = genai.generate_content(user_input)
                    st.session_state["chat_history"].append((user_input, response))
                    db.add_note(st.session_state.user_id, user_input, response)
                    st.success("✅ 已交由 LLM 回覆並儲存！")
                    st.rerun()

    if "user_input" in st.session_state:
        st.text_area("輸入問題或筆記", value=st.session_state["user_input"], key="user_input")
    if "llm_response" in st.session_state:
        st.text_area("LLM 回應", value=st.session_state["llm_response"], key="llm_response")

