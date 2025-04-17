import streamlit as st
from database import Database
from auth import login_required
import pandas as pd

@login_required
def show_literature():
    db = Database()
    st.subheader("我的研究文獻")
    title = st.text_input("標題", key="title")
    author = st.text_input("作者", key="author")
    date = st.date_input("日期", key="date")
    abstract = st.text_area("摘要", key="abstract")

    if st.button("儲存"):
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
            if st.button("刪除所選文獻"):
                for idx, row in selected_rows.iterrows():
                    delete_literature(row['id'])
                st.rerun()
    else:
        st.write("目前沒有文獻。")
