import streamlit as st
import openai

st.title("Tourism Bot")
st.write("Ask me anything about tourism!")

def ask_tourism_bot(question):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful tourism assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

user_input = st.text_input("You:", "")
if user_input:
    with st.spinner("Thinking..."):
        answer = ask_tourism_bot(user_input)
    st.markdown(f"**Bot:** {answer}")
