import streamlit as st

st.set_page_config(page_title="Tourism Bot", page_icon="🌍")

st.title("🌍 Tourism Bot")
st.write("Welcome to the Tourism Bot! Ask me about destinations, travel tips, or anything related to tourism.")

user_input = st.text_input("How can I help you today?")

if user_input:
    # Placeholder for bot logic
    st.write(f"You asked: {user_input}")
    st.write("(Tourism Bot will answer your question here.)")
