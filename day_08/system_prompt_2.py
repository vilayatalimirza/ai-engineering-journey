import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """A blunt, no-fluff senior engineer who gives terse, direct answers
Always:
- Give example of application of the concept in real world scenarios
- Explain concepts using simple, everyday language before using technical terms
- Give short code examples when relevant
- End your response with two short follow-up question to check understanding
Never:
- Give long, unstructured walls of text
- Assume prior AI/ML knowledge"""

model = genai.GenerativeModel(
    "gemini-3.8-flash",
    system_instruction=SYSTEM_PROMPT
)

def chat_loop():
    chat = model.start_chat(history=[])
    print("Engineer bot ready. Type 'quit' to exit, 'clear' to reset memory.\n")

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
            print(f"Engineer: {response.text}\n")
        except Exception as e:
            print(f"Something went wrong: {e}")
            print("Please try again.\n")

def main():
    chat_loop()

if __name__ == "__main__":
    main()