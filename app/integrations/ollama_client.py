from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings

from app.core.config import settings


def get_llm() -> ChatOllama:
    return ChatOllama(base_url=settings.ollama_base_url, model=settings.ollama_llm_model, temperature=0.2)


def get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(base_url=settings.ollama_base_url, model=settings.ollama_embed_model)
