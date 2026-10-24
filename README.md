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
