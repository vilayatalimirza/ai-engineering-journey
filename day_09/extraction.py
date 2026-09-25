import os
import json
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_info(text):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"Extract the name, age, and occupation from this text:\n\n{text}",
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "occupation": {"type": "string"}
                },
                "required": ["name", "age", "occupation"]
            }
        }
    )
    return json.loads(response.text)

def main():
    text = input("Enter a sentence describing a person: ")
    try:
        data = extract_info(text)
        print("\nExtracted data:")
        print(json.dumps(data, indent=2))
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to parse structured response: {e}")

if __name__ == "__main__":
    main()