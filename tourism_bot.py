"""Alternate Streamlit entry (e.g. older Cloud apps); prefer `streamlit run app.py`."""

import streamlit as st

from bot import ask_tourism_bot, get_openai_api_key

st.set_page_config(page_title="Tourism Bot", page_icon="🌍")

st.title("🌍 Tourism Bot")
st.write(
    "Ask about destinations, travel tips, or anything related to tourism."
)

api_key = get_openai_api_key()
if not api_key:
    st.error(
        "Missing **OPENAI_API_KEY**. Set it locally in `.streamlit/secrets.toml`, "
        "as an environment variable, or in **Streamlit Cloud → Settings → Secrets**."
    )
    st.stop()

user_input = st.text_input("How can I help you today?", "")

if user_input:
    with st.spinner("Thinking..."):
        answer = ask_tourism_bot(user_input, api_key)
    st.markdown(f"**Bot:** {answer}")
