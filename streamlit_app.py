import streamlit as st


st.set_page_config(
    page_title="ExpenseFlow",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DEFAULT_FRONTEND_URL = "https://expense-flow-thhg.vercel.app"
frontend_url = DEFAULT_FRONTEND_URL

st.markdown(
    """
    <style>
    [data-testid="stMainBlockContainer"] {
        max-width: 100%;
        padding: 0.5rem 0.75rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ExpenseFlow")
st.caption("Your complete ExpenseFlow app, including login, dashboard, and finance tools.")
st.link_button("Open ExpenseFlow in a new tab", frontend_url)

st.iframe(
    frontend_url,
    height=900,
)
