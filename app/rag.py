import os
from dotenv import load_dotenv
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found in environment variables.")

# Load dataset
df = pd.read_csv("data/cleaned_bookings.csv")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="C:/Users/Admin/llm_booking_analytics/data/chromadb")
collection = chroma_client.get_collection("bookings")

# Ensure collection exists
try:
    collection = chroma_client.get_collection("bookings")
    print("✅ Collection 'bookings' found.")
except chromadb.errors.InvalidCollectionException:
    print("⚠️ Collection 'bookings' not found. Creating a new one...")
    collection = chroma_client.create_collection("bookings")
    print("✅ Collection 'bookings' created successfully.")

def create_embeddings(df):
    texts = df[['hotel', 'country', 'lead_time', 'adr', 'is_canceled', 'arrival_date_month']].astype(str).agg(' '.join, axis=1).tolist()
    embeddings = model.encode(texts, batch_size=32)

    for i, emb in enumerate(embeddings):
        if not collection.get(ids=[str(i)])["documents"]:
            collection.add(documents=[texts[i]], embeddings=[emb.tolist()], ids=[str(i)])
            print(f"Added new embedding ID: {i}")
        else:
            print(f"Skipped existing embedding ID: {i}")

create_embeddings(df)

client = OpenAI(api_key=openai_api_key)

def query_rag(question):
    print("🔍 Encoding query...")
    query_embedding = model.encode([question])
    print("🔎 Querying ChromaDB...")
    collection = chroma_client.get_collection("bookings")
    results = collection.query(query_embeddings=query_embedding.tolist(), n_results=5)["documents"]

    print("📄 Raw Results from ChromaDB:", results)

    if not results or not results[0]:
        print("⚠️ No relevant results found in ChromaDB.")
        return "I couldn't find relevant booking data."

    context = " ".join(results[0])
    print("📜 Context for LLM:", context)

    prompt = f"""
    You are an AI assistant analyzing hotel booking data.

    **Available Data:**
    {context}

    Answer the following question based on the given data:
    **Question:** {question}

    Provide a clear, concise, and correct response.
    """
    print("🤖 Sending request to OpenAI...")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant analyzing booking data."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        user_question = input("\nAsk a question (or type 'exit' to quit): ")
        if user_question.lower() == "exit":
            break
        answer = query_rag(user_question)
        print("📝 Answer:", answer)
