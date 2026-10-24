"""Show a collection's settings, record count, and a sample of its records."""

import argparse

import chromadb

from config import COLLECTION_NAME, DB_DIR


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--limit", type=int, default=5, help="Number of records to show")
    args = parser.parse_args()

    collection = chromadb.PersistentClient(path=DB_DIR).get_collection(name=args.collection)
    print(f"Collection: {collection.name}")
    print(f"Count: {collection.count()}")
    print(f"Metadata: {collection.metadata}")
    if args.limit <= 0:
        return

    records = collection.get(limit=args.limit, include=["documents", "metadatas"])
    for index, record_id in enumerate(records["ids"]):
        print(f"\n[{index + 1}] ID: {record_id}")
        print(f"Metadata: {records['metadatas'][index]}")
        print(f"Document: {records['documents'][index]}")


if __name__ == "__main__":
    main()
