import streamlit as st

from pr_agent.dashboard.utils.read_reviews import get_review_json

st.title("Pull Requests")


prs = get_review_json()
data = []
for pr in prs:
    repos = pr.repository
    pr_number = pr.pr_number
    title = pr.title
    number_of_finding = len(pr.agent_output.review.findings)
    risk_level = pr.agent_output.review.risk_level
    recommendation = pr.agent_output.review.recommendation
    tokens_used = pr.agent_output.usage["total_tokens"] if pr.agent_output.usage else None
    data.append({
        "Repository": repos,
        "PR #": pr_number,
        "Title": title,
        "Findings #": number_of_finding,
        "Risk Level": risk_level,
        "Recommendation": recommendation,
        "Tokens": tokens_used
    })
st.dataframe(data)