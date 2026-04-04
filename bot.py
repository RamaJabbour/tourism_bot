import os

import openai


def get_openai_api_key() -> str:
    import streamlit as st

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


def ask_tourism_bot(question: str, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful tourism assistant."},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
