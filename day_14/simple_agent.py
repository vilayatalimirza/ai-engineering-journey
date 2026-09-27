import os
import json
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- The actual tools your code can run ---
def get_word_count(text):
    return {"word_count": len(text.split())}

def get_current_year():
    from datetime import datetime
    return {"year": datetime.now().year}

# --- Describing those tools to the model, so it knows they exist ---
tools = [
    {
        "function_declarations": [
            {
                "name": "get_word_count",
                "description": "Counts the number of words in a given piece of text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The text to count words in."}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "get_current_year",
                "description": "Returns the current calendar year.",
                "parameters": {"type": "object", "properties": {}}
            }
        ]
    }
]

# --- Mapping tool names to actual Python functions ---
available_functions = {
    "get_word_count": get_word_count,
    "get_current_year": get_current_year
}

import time

def run_agent(user_input, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=user_input,
                config={"tools": tools}
            )
            break
        except Exception as e:
            print(f"[API error: {e}]")
            if attempt < max_retries - 1:
                print(f"[Retrying in 2 seconds... (attempt {attempt + 2}/{max_retries})]")
                time.sleep(2)
            else:
                return "Sorry, the service is currently unavailable. Please try again in a moment."

    candidate = response.candidates[0]
    part = candidate.content.parts[0]

    if part.function_call:
        function_name = part.function_call.name
        function_args = dict(part.function_call.args)

        print(f"[Agent decided to call: {function_name}({function_args})]")

        function_to_call = available_functions[function_name]
        result = function_to_call(**function_args)

        print(f"[Function returned: {result}]")

        try:
            follow_up = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    user_input,
                    part,
                    types.Part.from_function_response(name=function_name, response=result)
                ],
                config={"tools": tools}
            )
            return follow_up.text
        except Exception as e:
            return f"Got the tool result ({result}), but couldn't generate a final response: {e}"
    else:
        return part.text
    
def main():
    print("Simple tool-using agent ready.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit", "q"):
            break
        answer = run_agent(user_input)
        print(f"Agent: {answer}\n")

if __name__ == "__main__":
    main()