import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    prompt = input("Ask Gemini something: ")
    answer = ask_gemini(prompt)
    print(f"\nGemini says:\n{answer}")

if __name__ == "__main__":
    main()