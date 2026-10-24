"""Display stored embeddings, optionally including full vectors."""

import argparse

import chromadb

from config import COLLECTION_NAME, DB_DIR


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--limit", type=int, default=5, help="Number of vectors to show")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many records")
    parser.add_argument(
        "--dimensions",
        type=int,
        default=8,
        help="Show the first N dimensions (default: 8); use --full for all dimensions",
    )
    parser.add_argument("--full", action="store_true", help="Print complete vectors")
    args = parser.parse_args()
    if args.limit < 0 or args.offset < 0 or args.dimensions < 1:
        parser.error("--limit and --offset must be non-negative; --dimensions must be positive")

    collection = chromadb.PersistentClient(path=DB_DIR).get_collection(name=args.collection)
    records = collection.get(
        limit=args.limit,
        offset=args.offset,
        include=["embeddings", "metadatas"],
    )
    if not records["ids"]:
        print("No records found for the requested range.")
        return

    for record_id, embedding, metadata in zip(
        records["ids"], records["embeddings"], records["metadatas"]
    ):
        vector = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
        shown = vector if args.full else vector[: args.dimensions]
        suffix = "" if args.full or len(shown) == len(vector) else ", …"
        print(f"ID: {record_id}")
        print(f"Metadata: {metadata}")
        print(f"Dimensions: {len(vector)}")
        print(f"Embedding: [{', '.join(f'{value:.6g}' for value in shown)}{suffix}]\n")


if __name__ == "__main__":
    main()
