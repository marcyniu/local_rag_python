"""List collections in the configured Chroma database."""

import chromadb

from config import DB_DIR


def main():
    collections = chromadb.PersistentClient(path=DB_DIR).list_collections()
    if not collections:
        print("No collections found.")
        return

    for collection in collections:
        # Chroma versions differ on whether list_collections returns names or objects.
        name = collection if isinstance(collection, str) else collection.name
        print(name)


if __name__ == "__main__":
    main()
