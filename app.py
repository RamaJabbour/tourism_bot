import os

import streamlit as st

from bot import ask_tourism_bot


def _openai_api_key() -> str:
    env_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if env_key:
        return env_key
    try:
        secret = st.secrets["OPENAI_API_KEY"]
        if secret:
            return str(secret).strip()
    except (KeyError, FileNotFoundError, TypeError):
        pass
    return ""


st.set_page_config(page_title="Tourism Bot", page_icon="🌍")

st.title("🌍 Tourism Bot")
st.write(
    "Ask about destinations, travel tips, or anything related to tourism."
)

api_key = _openai_api_key()
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
