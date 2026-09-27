import os
import chromadb
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path=str(Path(__file__).resolve().parent / "chroma_db"))
collection = chroma_client.get_or_create_collection(name="documents")

def read_document(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed_text(text):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    return response.embeddings[0].values

def store_document(filepath):
    text = read_document(filepath)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk]
        )
    print(f"Stored {len(chunks)} chunks in the vector database.\n")

def search(query, n_results=2):
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0]

def main():
    filepath = Path(__file__).resolve().parent.parent / "day_11" / "documents" / "Messi.txt"
    store_document(filepath)

    query = input("What do you want to know about the document? ")
    top_chunks = search(query)

    print("\nMost relevant chunks found:\n")
    for i, chunk in enumerate(top_chunks):
        print(f"--- Match {i+1} ---")
        print(chunk)
        print()

if __name__ == "__main__":
    main()