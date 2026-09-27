import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def read_document(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_chunk(chunk):
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=chunk
    )
    return response.embeddings[0].values

def main():
    filepath = Path(__file__).resolve().parent / "documents" / "Messi.txt"
    text = read_document(filepath)

    chunks = chunk_text(text)
    print(f"Document split into {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks):
        embedding = embed_chunk(chunk)
        print(f"Chunk {i}: {len(embedding)}-dimensional vector")
        print(f"Preview: {chunk[:80]}...\n")

if __name__ == "__main__":
    main()