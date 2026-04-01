"""Dependency injection for the ASIA API."""
from __future__ import annotations

from functools import lru_cache

from asia.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def create_rag_pipeline():
    """Create RAG pipeline with production adapters."""
    from asia.adapters.groq_provider import GroqProvider
    from asia.adapters.pg_paper_repository import PgPaperRepository
    from asia.adapters.sentence_transformer_embedder import SentenceTransformerEmbedder
    from asia.services.rag_pipeline import RAGPipeline

    settings = get_settings()

    llm = GroqProvider(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_NAME,
    )
    embedder = SentenceTransformerEmbedder(model_name=settings.EMBEDDING_MODEL_NAME)

    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    repo = PgPaperRepository(db_url)

    return RAGPipeline(
        llm_provider=llm,
        embedding_provider=embedder,
        paper_repository=repo,
        top_k=settings.RETRIEVAL_TOP_K,
    )
