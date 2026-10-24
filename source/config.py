"""Shared configuration for document ingestion and querying."""

import os


DATA_DIR = os.getenv("RAG_DATA_DIR", "./data")
DB_DIR = os.getenv("RAG_DB_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("RAG_COLLECTION_NAME", "rag_knowledge_base")
EMBED_MODEL = os.getenv("RAG_EMBED_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("RAG_LLM_MODEL", "qwen3.8:27b-mlx")
TOP_K = int(os.getenv("RAG_TOP_K", "3"))
