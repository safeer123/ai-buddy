from langchain.vectorstores import Chroma
from langchain.embeddings import FakeEmbeddings  # Gemini doesn't support embeddings (yet)
import os

class DummyEmbeddings:
    def embed_documents(self, texts):
        return [[0.0] * 1536 for _ in texts]

    def embed_query(self, text):
        return [0.0] * 1536

def build_vector_store(chunks):
    return Chroma.from_documents(chunks, embedding=DummyEmbeddings(), persist_directory="chroma_db")

def load_vector_store():
    return Chroma(persist_directory="chroma_db", embedding_function=DummyEmbeddings())
