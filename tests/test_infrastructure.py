"""Infrastructure acceptance test for step 01-01.

Validates:
- Domain models are importable (Paper, Chunk, Case, EvidenceLevel)
- Port interfaces are importable (LLMProvider, EmbeddingProvider, PaperRepository, CaseRepository)
- FastAPI app can be created and /api/health responds 200
- Pydantic Settings configuration loads
"""
import pytest


def test_domain_models_importable():
    from asia.domain.models import Paper, Chunk, Case, CaseQuery, EvidenceLevel, IngestionRun

    assert EvidenceLevel.ALTO is not None
    assert EvidenceLevel.MODERATO is not None
    assert EvidenceLevel.BASSO is not None


def test_port_interfaces_importable():
    from asia.ports.llm_provider import LLMProvider
    from asia.ports.embedding_provider import EmbeddingProvider
    from asia.ports.paper_repository import PaperRepository
    from asia.ports.case_repository import CaseRepository


def test_settings_loadable():
    from asia.config.settings import Settings

    settings = Settings(
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        GROQ_API_KEY="test-key",
    )
    assert settings.GROQ_MODEL_NAME == "llama-3.3-70b-versatile"
    assert settings.EMBEDDING_DIMENSION == 384
    assert settings.RETRIEVAL_TOP_K == 10
    assert settings.CONFIDENCE_THRESHOLD == 0.35


@pytest.mark.anyio
async def test_health_endpoint_returns_200():
    from httpx import ASGITransport, AsyncClient
    from asia.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
