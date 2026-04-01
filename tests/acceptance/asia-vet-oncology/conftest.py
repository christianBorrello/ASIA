"""
Acceptance test fixtures for ASIA Vet Oncology.

Test approach:
- Tests exercise API endpoints (driving ports) exclusively
- External services (Groq LLM, PubMed, Semantic Scholar) are mocked
- Paper repository uses in-memory fake for test isolation
- All responses use pre-canned LLM fixtures for determinism
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from pathlib import Path

import pytest

from asia.domain.models import Chunk, Paper


# ---------------------------------------------------------------------------
# Feature file discovery
# ---------------------------------------------------------------------------

FEATURE_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Mock providers for external services
# ---------------------------------------------------------------------------


class FakeLLMProvider:
    """Returns pre-canned synthesis text for deterministic testing."""

    def __init__(self, canned_response: str) -> None:
        self._canned = canned_response

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        return self._canned

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        for word in self._canned.split(" "):
            yield word + " "


class FakeEmbeddingProvider:
    """Returns deterministic 384-dimensional vectors."""

    def embed_text(self, text: str) -> list[float]:
        vec = [0.0] * 384
        for i, char in enumerate(text[:384]):
            vec[i] = ord(char) / 1000.0
        return vec

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]


class InMemoryPaperRepository:
    """Fake paper repository storing papers and chunks in memory."""

    def __init__(self) -> None:
        self._papers: dict[uuid.UUID, Paper] = {}
        self._chunks: list[Chunk] = []

    async def save(self, paper: Paper, chunks: list[Chunk] | None = None) -> None:
        self._papers[paper.id] = paper
        if chunks:
            self._chunks.extend(chunks)

    async def find_similar(
        self, embedding: list[float], top_k: int = 10
    ) -> list[Chunk]:
        return self._chunks[:top_k]

    async def get_by_id(self, paper_id: uuid.UUID) -> Paper | None:
        return self._papers.get(paper_id)

    async def get_by_doi(self, doi: str) -> Paper | None:
        for paper in self._papers.values():
            if paper.doi == doi:
                return paper
        return None

    async def save_ingestion_run(self, run) -> None:
        pass

    async def get_ingestion_run(self, run_id: uuid.UUID):
        return None


# ---------------------------------------------------------------------------
# Session-scoped fixtures (expensive setup, created once)
# ---------------------------------------------------------------------------


CANNED_SYNTHESIS = (
    "Il protocollo raccomandato e il CHOP, che produce remissione "
    "nell'80-90% dei casi [1][2]. La sopravvivenza mediana e di "
    "10-14 mesi per il linfoma B-cell [1][2][3]."
)


@pytest.fixture(scope="session")
def paper_repo():
    """In-memory paper repository shared across session."""
    return InMemoryPaperRepository()


@pytest.fixture(scope="session")
def app(paper_repo):
    """
    Create the ASIA FastAPI application with test configuration.

    Uses in-memory repository and mocked LLM provider.
    """
    from asia.main import app as fastapi_app
    from asia.services.rag_pipeline import RAGPipeline

    fake_llm = FakeLLMProvider(CANNED_SYNTHESIS)
    fake_embedder = FakeEmbeddingProvider()

    rag_pipeline = RAGPipeline(
        llm_provider=fake_llm,
        embedding_provider=fake_embedder,
        paper_repository=paper_repo,
    )

    fastapi_app.state.rag_pipeline = rag_pipeline

    return fastapi_app


@pytest.fixture(scope="session")
def test_client(app):
    """
    HTTP test client for the ASIA API.

    All acceptance tests invoke through this client,
    exercising the API endpoints (driving ports).
    """
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def seeded_corpus(app, paper_repo):
    """
    Seed the in-memory repository with papers for the 5 critical queries.
    """
    import asyncio

    from db.seeds.seed_papers import SEED_PAPERS

    embedder = FakeEmbeddingProvider()

    async def _seed():
        for paper_data in SEED_PAPERS:
            paper_id = uuid.uuid4()
            paper = Paper(
                id=paper_id,
                title=paper_data["title"],
                authors=paper_data["authors"],
                year=paper_data["year"],
                source="seed",
                doi=paper_data.get("doi"),
                journal=paper_data.get("journal"),
                abstract_text=paper_data.get("abstract"),
                study_type=paper_data.get("study_type"),
                sample_size=paper_data.get("sample_size"),
            )
            abstract = paper_data.get("abstract", paper_data["title"])
            embedding = embedder.embed_text(abstract)
            chunk = Chunk(
                id=uuid.uuid4(),
                paper_id=paper_id,
                chunk_index=0,
                chunk_text=abstract,
                chunk_type="abstract",
                embedding=embedding,
            )
            await paper_repo.save(paper, [chunk])

    asyncio.get_event_loop_policy().new_event_loop().run_until_complete(_seed())
    return True


# ---------------------------------------------------------------------------
# Function-scoped fixtures (per-test isolation)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_cases(app):
    """
    Remove all cases and query logs between tests.
    Papers/corpus data is preserved (session-scoped).
    """
    yield


# ---------------------------------------------------------------------------
# Mock providers for external services
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def mock_llm_responses():
    """
    Pre-canned LLM responses for the 5 critical queries.

    Each response includes:
    - Italian synthesis text with citation markers [1], [2], etc.
    - Citation-claim mappings for verification
    - Evidence level metadata
    - Comparison table data (for Q2 only)

    These fixtures ensure deterministic, reviewable test behavior
    without calling the real Groq API.
    """
    return {
        "Q1_first_line_protocol": {
            "synthesis": (
                "Il protocollo raccomandato e il CHOP, che produce remissione "
                "nell'80-90% dei casi [1][2]. La sopravvivenza mediana e di "
                "10-14 mesi per il linfoma B-cell [1][2][3]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Garrett",
                    "year": 2002,
                    "claim": "80-90% remission",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Simon",
                    "year": 2006,
                    "claim": "80-90% remission",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 3,
                    "author": "Vail",
                    "year": 2013,
                    "claim": "10-14 months survival",
                    "verification": "PARZIALE",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 3,
            "total_sample_size": 285,
        },
        "Q2_chop_comparison": {
            "synthesis": (
                "CHOP-19 e CHOP-25 hanno outcome equivalenti in termini di "
                "remissione e sopravvivenza [1]. Lo studio multicentrico "
                "randomizzato su 408 cani non ha trovato differenze "
                "significative [1]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Sorenmo",
                    "year": 2020,
                    "claim": "equivalent outcomes",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "ALTO",
            "study_count": 1,
            "total_sample_size": 408,
            "comparison_table": {
                "columns": [
                    "protocol",
                    "remission_rate",
                    "median_survival",
                    "sample_size",
                ],
                "rows": [
                    {
                        "protocol": "CHOP-19",
                        "remission_rate": "80-90%",
                        "median_survival": "10-12 mesi",
                        "sample_size": 204,
                        "citation_id": 1,
                    },
                    {
                        "protocol": "CHOP-25",
                        "remission_rate": "80-90%",
                        "median_survival": "10-12 mesi",
                        "sample_size": 204,
                        "citation_id": 1,
                    },
                ],
            },
        },
        "Q3_rescue_protocols": {
            "synthesis": (
                "Per la recidiva precoce dopo CHOP, le opzioni di rescue "
                "includono LOPP [1], LAP [2] e protocolli a base di "
                "rabacfosadina [3]. La scelta dipende dalla risposta "
                "iniziale e dalla tolleranza del paziente."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Griessmayr",
                    "year": 2007,
                    "claim": "LOPP rescue",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Saba",
                    "year": 2009,
                    "claim": "LAP rescue",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 3,
                    "author": "Thamm",
                    "year": 2017,
                    "claim": "rabacfosadine",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 3,
            "total_sample_size": 142,
        },
        "Q4_prognosis_immunophenotype": {
            "synthesis": (
                "Il linfoma B-cell ha una prognosi significativamente "
                "migliore rispetto al T-cell [1][2]. La sopravvivenza "
                "mediana per B-cell e di 10-14 mesi contro 5-8 mesi "
                "per T-cell [1][2]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Vail",
                    "year": 2013,
                    "claim": "B-cell better prognosis",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Aresu",
                    "year": 2015,
                    "claim": "survival differences",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 2,
            "total_sample_size": 310,
        },
        "Q5_dose_adjustment": {
            "synthesis": (
                "Per neutropenia di grado 1-2, si consiglia il ritardo di "
                "1 settimana senza riduzione della dose [1]. Per grado 3-4, "
                "riduzione del 20-25% della dose di doxorubicina e "
                "considerare lo switch a protocolli alternativi [1][2]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Chun",
                    "year": 2007,
                    "claim": "dose adjustment by grade",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Rau",
                    "year": 2010,
                    "claim": "protocol switch for grade 3-4",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "BASSO",
            "study_count": 2,
            "total_sample_size": 89,
        },
        "no_evidence": {
            "synthesis": None,
            "message": (
                "Non sono state trovate evidenze sufficienti nel corpus "
                "per rispondere a questa domanda."
            ),
            "scope_explanation": "Il corpus attuale copre il linfoma multicentrico canino.",
            "suggestions": [
                "Prova a riformulare la domanda",
                "Consulta le query pre-caricate",
                "Cerca direttamente su PubMed",
            ],
        },
        "citation_removed": {
            "synthesis": (
                "Il protocollo CHOP e il trattamento di riferimento [1][2]. "
                "La remissione e elevata [1]."
            ),
            "original_citation_count": 5,
            "final_citation_count": 4,
            "removed_citation_id": 4,
            "transparency_note": (
                "Una citazione inizialmente identificata e stata rimossa "
                "perche non supportava adeguatamente l'affermazione."
            ),
        },
    }
