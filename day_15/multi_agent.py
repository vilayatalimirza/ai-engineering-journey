import sys
from pathlib import Path

# Add project root to sys.path so we can import from common
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.llm import generate

RESEARCHER_PROMPT = """You are a critical research analyst. Given a topic, list 4-6 key factual 
points about it, being specific and avoiding fluff. Do not write prose paragraphs — just a 
clear bullet list of facts. If you're unsure of a fact, say so explicitly rather than guessing."""

WRITER_PROMPT = """You are a friendly content writer. Given a list of research bullet points, 
write a short, engaging paragraph (4-6 sentences) for a general audience. Do not invent any 
facts beyond what's given to you in the bullet points."""

CRITIC_PROMPT = """You are a strict fact-checker. Compare the summary against the original 
research notes. List any claims in the summary that are NOT supported by the research notes. 
If everything is supported, say "No unsupported claims found." Otherwise, list the unsupported claims clearly."""

def call_agent(system_prompt: str, user_message: str) -> str:
    return generate(contents=user_message, system_prompt=system_prompt)

def research_topic(topic: str) -> str:
    return call_agent(RESEARCHER_PROMPT, f"Research this topic: {topic}")

def write_summary(research_notes: str) -> str:
    return call_agent(WRITER_PROMPT, f"Write a summary based on these notes:\n\n{research_notes}")

def fact_check(summary: str, research_notes: str) -> str:
    return call_agent(CRITIC_PROMPT, f"Summary:\n{summary}\n\nResearch Notes:\n{research_notes}")

def run_pipeline(topic: str):
    print(f"[Researcher agent working on: {topic}]\n")
    research = research_topic(topic)
    print(f"--- Research notes ---\n{research}\n")

    print("[Writer agent turning notes into a summary]\n")
    summary = write_summary(research)
    print(f"--- Final summary ---\n{summary}\n")

    print("[Critic agent checking summary against research]\n")
    verification = fact_check(summary, research)
    print(f"--- Fact-checking results ---\n{verification}\n")

    # Item 2 addressed: return all three outputs
    return research, summary, verification

def main():
    topic = input("What topic should the agents cover? ").strip() or "Playwright"
    run_pipeline(topic)

if __name__ == "__main__":
    main()