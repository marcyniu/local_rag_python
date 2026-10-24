# local_rag_python


### Set local environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Configure the RAG environment
Shared settings are defined in `source/config.py`. Override them with environment
variables when needed:

| Variable | Default |
| --- | --- |
| `RAG_DATA_DIR` | `./data` |
| `RAG_DB_DIR` | `./chroma_db` |
| `RAG_COLLECTION_NAME` | `rag_knowledge_base` |
| `RAG_EMBED_MODEL` | `nomic-embed-text` |
| `RAG_LLM_MODEL` | `qwen3.8:27b-mlx` |
| `RAG_TOP_K` | `3` |

### Vector database tools
Run these commands from the repository root. Each uses `RAG_DB_DIR` and the
configured collection by default; use `--collection NAME` to select another one.

```bash
python3 source/list_collections.py
python3 source/inspect_collection.py --limit 10
python3 source/show_embeddings.py --limit 5
python3 source/show_embeddings.py --limit 1 --full
python3 source/query_collection.py "home-office stipend" --limit 5
```

`show_embeddings.py` prints the first eight vector dimensions by default; `--full`
prints the entire vector. Collection removal is available separately and requires
an explicit confirmation flag:

```bash
python3 source/delete_collection.py --collection rag_knowledge_base --yes
```
