from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://asia:asia@localhost:5432/asia"
    GROQ_API_KEY: str = ""
    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL_NAME: str = "llama-3.1-8b-instant"
    GROQ_MAX_RETRIES: int = 2
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    RETRIEVAL_TOP_K: int = 10
    CONFIDENCE_THRESHOLD: float = 0.35

    model_config = {"env_prefix": "", "case_sensitive": True}
