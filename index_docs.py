from doc_loader import load_documents
from vector_store import build_vector_store

chunks = load_documents()
build_vector_store(chunks)