import chromadb
import ollama

DB_DIR = "./chroma_db"
COLLECTION_NAME = "rag_knowledge_base"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen3.8:27b-mlx"
TOP_K = 3

def retrieve_context(query: str, n_results: int = TOP_K):
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    # Embed user question using the exact same embedder
    query_vector = ollama.embed(model=EMBED_MODEL, input=query)["embeddings"][0]

    # Query Chroma
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )
    
    retrieved_texts = results["documents"][0]
    retrieved_sources = [meta["source"] for meta in results["metadatas"][0]]
    return retrieved_texts, retrieved_sources

def ask_rag(question: str):
    contexts, sources = retrieve_context(question)
    
    formatted_context = "\n---\n".join(
        [f"[Source: {sources[i]}]\n{c}" for i, c in enumerate(contexts)]
    )

    prompt = f"""You are a helpful assistant. Use ONLY the following context to answer the question.
If the answer is not present in the context, clearly state that you do not have enough information.

Context:
{formatted_context}

Question:
{question}
"""

    print(f"\n--- Asking {LLM_MODEL} ---\n")
    stream = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "What is the home-office stipend and how do I submit for it?"        
    
    ask_rag(query)
