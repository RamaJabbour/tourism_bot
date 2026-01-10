import openai
import os

def ask_tourism_bot(question):
    client = openai.OpenAI(api_key="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")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful tourism assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Welcome to the Tourism Bot! Ask me anything about tourism.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        answer = ask_tourism_bot(user_input)
        print("Bot:", answer)
