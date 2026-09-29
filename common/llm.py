import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRIMARY_MODEL = "gemini-3.1-flash-lite"
FALLBACK_MODEL = "gemini-3.5-flash"


def _get_backoff_seconds(error_code: int | None, attempt: int) -> int:
    """Return appropriate wait time for rate limits vs server errors."""
    if error_code == 429:
        return 12
    return 2 ** attempt


def _execute_model_attempts(model: str, contents: str, config: dict | None, max_retries: int) -> str | None:
    """Attempt generation with retries on temporary failures. Return text or None."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
            return response.text or ""
        except errors.APIError as e:
            is_transient = (e.code == 429) or (e.code is not None and e.code >= 500)
            if not is_transient:
                print(f"[{model} non-retryable error {e.code}: {e.message}]")
                return None

            wait_time = _get_backoff_seconds(e.code, attempt)
            print(f"[{model} code {e.code} (attempt {attempt}/{max_retries}). Backing off for {wait_time}s...]")
            time.sleep(wait_time)

    print(f"[{model} exhausted retries.]")
    return None


def generate(contents: str, system_prompt: str = None, max_retries: int = 3) -> str:
    config = {"system_instruction": system_prompt} if system_prompt else None
    candidate_models = [m for m in dict.fromkeys([PRIMARY_MODEL, FALLBACK_MODEL]) if m]

    for model in candidate_models:
        result = _execute_model_attempts(model, contents, config, max_retries)
        if result is not None:
            return result

    raise RuntimeError("All models and retries failed.")