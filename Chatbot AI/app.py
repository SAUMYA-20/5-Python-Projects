import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

# Set up OpenAI client
client = openai.OpenAI(api_key=api_key)

print("Chatbot: Hello! I'm powered by ChatGPT. Ask me anything. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot: Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        print(f"Chatbot: {reply}\n")
    except Exception as e:
        print(f"Chatbot: Error occurred: {e}\n")