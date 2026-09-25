import os
import json
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

INTERVIEWER_PROMPT = """You are a friendly intake assistant collecting basic info from a candidate
interested in an AI Engineering bootcamp. Ask one question at a time about: their name,
current occupation, years of programming experience, and what they hope to achieve.
Keep questions short and conversational. Once you have all four pieces of information,
thank the candidate and let them know you have everything you need."""
MODEL_NAME = "gemini-3.1-flash-lite"


def create_chat():
    return client.chats.create(
        model=MODEL_NAME,
        config={"system_instruction": INTERVIEWER_PROMPT}
    )


def is_interview_complete(bot_message):
    """Ask the model directly whether the given bot message signals the
    interview is finished, and get back a reliable boolean instead of
    relying on fragile exact-text matching."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=(
            "Does this message indicate the interviewer has finished asking "
            "all four questions (name, occupation, years of experience, goal) "
            "and is concluding the interview? Answer based on the message's "
            "intent, not exact wording.\n\n"
            f"Message: {bot_message}"
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "complete": {"type": "boolean"}
                },
                "required": ["complete"]
            }
        }
    )
    return json.loads(response.text)["complete"]


def extract_profile(conversation_text):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"Extract the candidate's info from this interview transcript:\n\n{conversation_text}",
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "occupation": {"type": "string"},
                    "years_experience": {"type": "integer"},
                    "goal": {"type": "string"}
                },
                "required": ["name", "occupation", "years_experience", "goal"]
            }
        }
    )
    return json.loads(response.text)


def run_interview():
    chat = create_chat()
    transcript = []

    print("Interview bot starting...\n")

    try:
        response = chat.send_message("Start the interview.")
    except Exception as e:
        print(f"Something went wrong starting the interview: {e}")
        return ""

    print(f"Bot: {response.text}\n")
    transcript.append(f"Bot: {response.text}")

    # Safety net: never loop forever even if the completion check misfires
    max_turns = 10
    turn_count = 0

    while not is_interview_complete(response.text) and turn_count < max_turns:
        user_input = input("You: ")
        transcript.append(f"You: {user_input}")

        try:
            response = chat.send_message(user_input)
            print(f"Bot: {response.text}\n")
            transcript.append(f"Bot: {response.text}")
        except Exception as e:
            print(f"Something went wrong: {e}")
            break

        turn_count += 1

    return "\n".join(transcript)


def main():
    full_transcript = run_interview()

    if not full_transcript:
        print("No interview data collected.")
        return

    print("\nExtracting structured profile...\n")

    try:
        profile = extract_profile(full_transcript)
        print(json.dumps(profile, indent=2))

        output_path = Path(__file__).resolve().parent / "candidate_profile.json"
        with open(output_path, "w") as f:
            json.dump(profile, f, indent=2)
        print(f"\nSaved to {output_path}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to extract structured profile: {e}")


if __name__ == "__main__":
    main()