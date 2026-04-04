import os

import openai


def _secret_or_env(st_mod, secret_key: str, env_key: str) -> str:
    env_val = (os.environ.get(env_key) or "").strip()
    if env_val:
        return env_val
    try:
        v = st_mod.secrets[secret_key]
        if v:
            return str(v).strip()
    except (KeyError, FileNotFoundError, TypeError):
        pass
    return ""


def get_llm_key_and_provider():
    """Returns (provider, api_key) where provider is 'anthropic' or 'openai', or (None, '')."""
    import streamlit as st

    anthropic_key = _secret_or_env(st, "ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
    if anthropic_key:
        return "anthropic", anthropic_key

    openai_named = _secret_or_env(st, "OPENAI_API_KEY", "OPENAI_API_KEY")
    if openai_named.startswith("sk-ant-"):
        return "anthropic", openai_named
    if openai_named:
        return "openai", openai_named

    return None, ""


def ask_beauty_advisor(question: str, provider: str, api_key: str) -> str:
    system = (
        "You are a warm, professional beauty salon consultant. Give concise, safe, "
        "general advice about hair, skin, nails, and self-care. Remind users that "
        "in-person consultation is best for color, chemicals, or medical concerns."
    )
    if provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": question}],
        )
        block = msg.content[0]
        if block.type == "text":
            return block.text
        return str(block)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
