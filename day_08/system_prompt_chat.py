import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a senior AI engineer mentoring a career-switcher who is learning Python and AI engineering from scratch. 
Always:
- Explain concepts using simple, everyday language before using technical terms
- Give short code examples when relevant
- End your response with one short follow-up question to check understanding
Never:
- Give long, unstructured walls of text
- Assume prior AI/ML knowledge"""

model = genai.GenerativeModel(
    "gemini-3.6-flash",
    system_instruction=SYSTEM_PROMPT
)

def chat_loop():
    chat = model.start_chat(history=[])
    print("Mentor bot ready. Type 'quit' to exit, 'clear' to reset memory.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            chat = model.start_chat(history=[])
            print("Conversation memory cleared.\n")
            continue

        try:
            response = chat.send_message(user_input)
            print(f"Mentor: {response.text}\n")
        except Exception as e:
            print(f"Something went wrong: {e}")
            print("Please try again.\n")

def main():
    chat_loop()

if __name__ == "__main__":
    main()