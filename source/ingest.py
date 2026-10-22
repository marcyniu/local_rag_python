import os
import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

DATA_DIR = "./data"
DB_DIR = "./chroma_db"
COLLECTION_NAME = "rag_knowledge_base"
EMBED_MODEL = "nomic-embed-text"

def load_documents(data_path: str):
    documents = []
    for file in os.listdir(data_path):
        full_path = os.path.join(data_path, file)
        if file.endswith(".pdf"):
            reader = PdfReader(full_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            documents.append({"text": text, "source": file})
        elif file.endswith((".txt", ".md")):
            with open(full_path, "r", encoding="utf-8") as f:
                documents.append({"text": f.read(), "source": file})
    return documents

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        # Create a sample document to test immediately
        with open(os.path.join(DATA_DIR, "company_policy.txt"), "w") as f:
            f.write(
                "Acme Corp Remote Work Policy: Employees are entitled to a $500 annual home-office stipend. "
                "All remote workers must log in via WireGuard VPN between 09:00 and 17:00 EST. "
                "Reimbursements must be submitted through the Expensify portal within 30 days of purchase."
            )
        print("Created sample document in ./data/company_policy.txt")

    print("Loading documents...")
    docs = load_documents(DATA_DIR)

    # 500 characters with 100-character overlap
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    
    chunks = []
    metadatas = []
    ids = []

    for doc_idx, doc in enumerate(docs):
        split_texts = splitter.split_text(doc["text"])
        for chunk_idx, chunk in enumerate(split_texts):
            chunks.append(chunk)
            metadatas.append({"source": doc["source"]})
            ids.append(f"doc_{doc_idx}_chunk_{chunk_idx}")

    print(f"Generated {len(chunks)} chunks. Generating embeddings with Ollama ({EMBED_MODEL})...")

    # Connect to persistent ChromaDB
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Batch embed and insert
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        batch_meta = metadatas[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]

        # Call Ollama embedding API
        embed_response = ollama.embed(model=EMBED_MODEL, input=batch_chunks)
        embeddings = embed_response["embeddings"]

        collection.upsert(
            documents=batch_chunks,
            embeddings=embeddings,
            metadatas=batch_meta,
            ids=batch_ids
        )

    print(f"Indexing complete! Database saved to '{DB_DIR}'.")

if __name__ == "__main__":
    main()
