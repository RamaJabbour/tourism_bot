import openai


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
