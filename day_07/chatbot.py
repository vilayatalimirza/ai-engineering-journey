import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

def chat_loop():
    chat = model.start_chat(history=[])
    print("Chatbot ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() =="quit":
            print("Goodbye!")
            break
        try:    
            response = chat.send_message(user_input)
            print(f"Gemini: {response.text}")
        except Exception as e:
            print(f"Something went wrong: {e}")
            print("Please try again.\n")

    print(chat.history)

def main():
    chat_loop()

if __name__ == "__main__":
    main()