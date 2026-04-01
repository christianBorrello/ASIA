"""Unit tests for LLM fallback flag propagation through RAG pipeline to query endpoint.

Step 01-02: RAG pipeline + query endpoint propagate fallback flag.

Tests enter through RAGPipeline driving port and assert observable outcomes
at the result dict boundary. LLM and repository are mocked at port boundaries.

Test Budget: 3 behaviors x 2 = 6 max
  1. When fallback used, result includes used_fallback=True + model names
  2. When primary model used, result includes used_fallback=False
  3. Query endpoint passes fallback fields through to JSON response
Actual: 3 tests (1 parametrized for behaviors 1+2, 1 acceptance through endpoint)
"""
from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import pytest

from asia.domain.models import Chunk, Paper


# ---------------------------------------------------------------------------
# Fakes at port boundaries
# ---------------------------------------------------------------------------

class FallbackAwareLLMStub:
    """Stub LLM that simulates fallback behavior via last_used_fallback property."""

    def __init__(self, response: str, simulate_fallback: bool = False) -> None:
        self._response = response
        self._simulate_fallback = simulate_fallback
        self._last_used_fallback = False
        self._model = "llama-3.3-70b-versatile"
        self._fallback_model = "llama-3.1-8b-instant"

    @property
    def last_used_fallback(self) -> bool:
        return self._last_used_fallback

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        self._last_used_fallback = self._simulate_fallback
        return self._response

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        for word in self._response.split(" "):
            yield word + " "


class StubEmbeddingProvider:
    """Stub embedder returning zero vectors."""

    def embed_text(self, text: str) -> list[float]:
        return [0.0] * 384

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]


class InMemoryPaperRepository:
    """Fake repository returning pre-seeded chunks."""

    def __init__(self, papers: list[Paper], chunks: list[Chunk]) -> None:
        self._papers = {p.id: p for p in papers}
        self._chunks = chunks

    async def find_similar(
        self, embedding: list[float], top_k: int = 10
    ) -> list[Chunk]:
        return self._chunks[:top_k]

    async def get_by_id(self, paper_id: uuid.UUID) -> Paper | None:
        return self._papers.get(paper_id)

    async def get_by_doi(self, doi: str) -> Paper | None:
        for p in self._papers.values():
            if p.doi == doi:
                return p
        return None

    async def save(self, paper: Paper, chunks: list[Chunk] | None = None) -> None:
        pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SYNTHESIS_WITH_CITATIONS = (
    "Il protocollo CHOP produce remissione nell'80-90% dei casi [1][2]. "
    "La sopravvivenza mediana e di 10-14 mesi [1]."
)


def _make_paper(
    study_type: str = "retrospective",
    sample_size: int = 100,
    year: int = 2020,
    title: str = "Test paper",
) -> Paper:
    paper_id = uuid.uuid4()
    return Paper(
        id=paper_id,
        title=title,
        authors=[{"name": "Author A"}],
        year=year,
        source="seed",
        doi=f"10.1234/{paper_id}",
        journal="Test Journal",
        abstract_text="Abstract text about CHOP protocol for canine lymphoma.",
        study_type=study_type,
        sample_size=sample_size,
    )


def _make_chunk(paper: Paper) -> Chunk:
    return Chunk(
        id=uuid.uuid4(),
        paper_id=paper.id,
        chunk_index=0,
        chunk_text=paper.abstract_text or paper.title,
        chunk_type="abstract",
        embedding=[0.0] * 384,
    )


# ---------------------------------------------------------------------------
# Test: RAG pipeline propagates fallback info (behaviors 1 + 2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "simulate_fallback,expected_used_fallback",
    [
        (True, True),
        (False, False),
    ],
    ids=["fallback-used", "primary-used"],
)
@pytest.mark.anyio
async def test_rag_pipeline_propagates_fallback_flag(
    simulate_fallback, expected_used_fallback
):
    """RAGPipeline result includes used_fallback reflecting LLM provider state."""
    from asia.services.rag_pipeline import RAGPipeline

    paper1 = _make_paper(study_type="meta_analysis", sample_size=400)
    paper2 = _make_paper(study_type="randomized_controlled_trial", sample_size=200)
    chunk1 = _make_chunk(paper1)
    chunk2 = _make_chunk(paper2)

    llm = FallbackAwareLLMStub(
        response=SYNTHESIS_WITH_CITATIONS,
        simulate_fallback=simulate_fallback,
    )

    pipeline = RAGPipeline(
        llm_provider=llm,
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper1, paper2],
            chunks=[chunk1, chunk2],
        ),
    )

    result = await pipeline.execute_query("Qual e il protocollo CHOP?")

    assert result["used_fallback"] is expected_used_fallback
    if expected_used_fallback:
        assert result["fallback_model"] == "llama-3.1-8b-instant"
        assert result["primary_model"] == "llama-3.3-70b-versatile"
    else:
        assert "fallback_model" not in result
        assert "primary_model" not in result


# ---------------------------------------------------------------------------
# Acceptance test: query endpoint passes fallback fields to JSON response
# ---------------------------------------------------------------------------

def test_query_endpoint_includes_fallback_fields_in_response():
    """POST /api/query response JSON includes used_fallback field from RAG pipeline."""
    import uuid as _uuid

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from asia.api.routes import query as query_module
    from asia.services.rag_pipeline import RAGPipeline

    paper_id = _uuid.uuid4()
    paper = Paper(
        id=paper_id,
        title="Test paper",
        authors=[{"name": "Author A"}],
        year=2020,
        source="seed",
        doi=f"10.1234/{paper_id}",
        journal="Test Journal",
        abstract_text="Abstract text about CHOP protocol for canine lymphoma.",
        study_type="retrospective",
        sample_size=100,
    )
    chunk = Chunk(
        id=_uuid.uuid4(),
        paper_id=paper_id,
        chunk_index=0,
        chunk_text=paper.abstract_text,
        chunk_type="abstract",
        embedding=[0.0] * 384,
    )

    llm = FallbackAwareLLMStub(
        response=SYNTHESIS_WITH_CITATIONS,
        simulate_fallback=True,
    )

    pipeline = RAGPipeline(
        llm_provider=llm,
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper],
            chunks=[chunk],
        ),
    )

    # Build a minimal FastAPI app with just the query router to avoid lifespan DB issues
    test_app = FastAPI()
    test_app.include_router(query_module.router)
    test_app.state.rag_pipeline = pipeline

    with TestClient(test_app) as client:
        response = client.post(
            "/api/query",
            json={"text": "Qual e il protocollo CHOP?"},
        )

    assert response.status_code == 200
    data = response.json()
    assert "used_fallback" in data, f"used_fallback missing from response: {data.keys()}"
    assert data["used_fallback"] is True
    assert data["fallback_model"] == "llama-3.1-8b-instant"
    assert data["primary_model"] == "llama-3.3-70b-versatile"
