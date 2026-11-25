import streamlit as st
st.set_page_config(layout="wide", page_title="PR Agent Dashboard")


pages = [
    st.Page("pages/Runs.py", title="Runs"),
    st.Page("pages/pull_requests.py", title="Pull requests"),
    st.Page("pages/issues.py", title="Issues"),
    st.Page("pages/history.py", title="History"),
    st.Page("pages/service_log.py", title="Service log"),
    st.Page("pages/repository.py", title="Repositories"),
    st.Page("pages/agents_prompts.py", title="Agents & prompts"),
]
pg = st.navigation(pages, position="top")
pg.run()
