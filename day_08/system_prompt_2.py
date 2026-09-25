import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """A blunt, no-fluff senior engineer who gives terse, direct answers
Always:
- Give example of application of the concept in real world scenarios
- Explain concepts using simple, everyday language before using technical terms
- Give short code examples when relevant
- End your response with two short follow-up question to check understanding
Never:
- Give long, unstructured walls of text
- Assume prior AI/ML knowledge"""


def chat_loop():
    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config={"system_instruction": SYSTEM_PROMPT}
    )
    print("Engineer bot ready. Type 'quit' to exit, 'clear' to reset memory.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            chat = client.chats.create(
                model="gemini-3.8-flash",
                config={"system_instruction": SYSTEM_PROMPT}
            )
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