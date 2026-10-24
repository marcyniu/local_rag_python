"""Search a collection by text and print the nearest records."""

import argparse

import ollama
import chromadb

from config import COLLECTION_NAME, DB_DIR, EMBED_MODEL, TOP_K


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Text to search for")
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--limit", type=int, default=TOP_K, help=f"Results to return (default: {TOP_K})")
    args = parser.parse_args()
    if args.limit <= 0:
        parser.error("--limit must be positive")

    collection = chromadb.PersistentClient(path=DB_DIR).get_collection(name=args.collection)
    vector = ollama.embed(model=EMBED_MODEL, input=args.query)["embeddings"][0]
    results = collection.query(
        query_embeddings=[vector],
        n_results=args.limit,
        include=["documents", "metadatas", "distances"],
    )
    for record_id, document, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        print(f"ID: {record_id} | Distance: {distance:.6g} | Metadata: {metadata}")
        print(document)
        print()


if __name__ == "__main__":
    main()
