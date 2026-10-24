"""Delete a collection after an explicit confirmation flag."""

import argparse

import chromadb

from config import COLLECTION_NAME, DB_DIR


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--yes", action="store_true", help="Confirm permanent collection deletion")
    args = parser.parse_args()
    if not args.yes:
        parser.error("deletion is permanent; pass --yes to confirm")

    chromadb.PersistentClient(path=DB_DIR).delete_collection(name=args.collection)
    print(f"Deleted collection '{args.collection}'.")


if __name__ == "__main__":
    main()
