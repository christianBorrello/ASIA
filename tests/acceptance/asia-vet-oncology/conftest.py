"""
Acceptance test fixtures for ASIA Vet Oncology.

Test approach:
- Tests exercise API endpoints (driving ports) exclusively
- External services (Groq LLM, PubMed, Semantic Scholar) are mocked
- Paper repository uses in-memory fake for test isolation
- All responses use pre-canned LLM fixtures for determinism
"""

from __future__ import annotations

import math
import uuid
from collections.abc import AsyncIterator
from dataclasses import replace
from pathlib import Path

import pytest

from pytest_bdd import given

from asia.domain.models import Case, CaseQuery, Chunk, Paper


# ---------------------------------------------------------------------------
# Feature file discovery
# ---------------------------------------------------------------------------

FEATURE_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Mock providers for external services
# ---------------------------------------------------------------------------


CANNED_VERIFICATION_SYNTHESIS = (
    "Il protocollo CHOP e il trattamento di riferimento [1]. "
    "La remissione e elevata [2]. "
    "Studi recenti confermano l'efficacia [3]. "
    "Il dosaggio standard prevede cicli trisettimanali [4]. "
    "La tossicita e gestibile con supporto adeguato [5]."
)

CANNED_VERIFICATION_RESPONSE = (
    "[1]: SUPPORTA - il paper conferma il CHOP come riferimento\n"
    "[2]: SUPPORTA - dati di remissione confermati\n"
    "[3]: PARZIALE - supporto parziale sull'efficacia\n"
    "[4]: NON_SUPPORTA - il paper non menziona dosaggi specifici\n"
    "[5]: SUPPORTA - tossicita ben documentata"
)


class FakeLLMProvider:
    """Returns pre-canned synthesis text for deterministic testing.

    Routes responses based on query content keywords so each
    pre-loaded query receives a clinically appropriate canned response.
    When prompt contains verification keywords (SUPPORTA, verifica +
    classifica), returns canned verification response.
    """

    def __init__(self, default_response: str, query_responses: dict[str, str] | None = None) -> None:
        self._default = default_response
        self._query_responses = query_responses or {}

    def _select_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        # Verification prompt detection: contains classification keywords
        if "supporta" in prompt_lower and "non_supporta" in prompt_lower:
            return CANNED_VERIFICATION_RESPONSE
        for keyword, response in self._query_responses.items():
            if keyword in prompt_lower:
                return response
        return self._default

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        return self._select_response(prompt)

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        response = self._select_response(prompt)
        for word in response.split(" "):
            yield word + " "


class FakeEmbeddingProvider:
    """Returns deterministic 384-dimensional vectors.

    Off-topic terms (non-canine-lymphoma species/diseases) produce
    orthogonal vectors to ensure the confidence threshold rejects them.
    """

    _OFF_TOPIC_MARKERS = {"gatto", "felino", "feline", "osteosarcoma", "polmonare"}

    def embed_text(self, text: str) -> list[float]:
        words = set(text.lower().split())
        if words & self._OFF_TOPIC_MARKERS:
            # Off-topic: return a fixed orthogonal vector that produces
            # near-zero similarity with any on-topic corpus embedding.
            vec = [0.0] * 384
            vec[0] = -1.0
            return vec
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
        scored = []
        for chunk in self._chunks:
            sim = self._cosine_similarity(embedding, chunk.embedding)
            scored.append((chunk, sim))
        scored.sort(key=lambda x: x[1], reverse=True)
        top_results = scored[:top_k]
        if not top_results:
            return []
        max_sim = top_results[0][1]
        results = []
        for chunk, sim in top_results:
            results.append(replace(chunk, similarity=sim))
        return results

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

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


class InMemoryCaseRepository:
    """Fake case repository storing cases in memory."""

    def __init__(self) -> None:
        self._cases: dict[uuid.UUID, Case] = {}
        self._queries: dict[uuid.UUID, list[CaseQuery]] = {}

    async def create(self, case: Case) -> Case:
        self._cases[case.id] = case
        self._queries[case.id] = []
        return case

    async def get(self, case_id: uuid.UUID) -> Case | None:
        return self._cases.get(case_id)

    async def list_queries(self, case_id: uuid.UUID) -> list[CaseQuery]:
        return self._queries.get(case_id, [])

    def clear(self) -> None:
        self._cases.clear()
        self._queries.clear()


# ---------------------------------------------------------------------------
# Session-scoped fixtures (expensive setup, created once)
# ---------------------------------------------------------------------------


CANNED_SYNTHESIS = (
    "Il protocollo raccomandato e il CHOP, che produce remissione "
    "nell'80-90% dei casi [1][2]. La sopravvivenza mediana e di "
    "10-14 mesi per il linfoma B-cell [1][2][3]."
)

CANNED_Q2_SYNTHESIS = (
    "CHOP-19 e CHOP-25 hanno outcome equivalenti in termini di "
    "remissione e sopravvivenza [4]. Lo studio multicentrico di Sorenmo "
    "su 408 cani non ha trovato differenze significative tra i due "
    "protocolli [4][5]. La durata mediana della prima remissione era "
    "simile: 188 giorni per CHOP-19 contro 210 giorni per CHOP-25, "
    "senza differenze statisticamente significative [4][5][6].\n\n"
    '```json\n'
    '{"comparison_table": {'
    '"headers": ["Protocollo", "Tasso remissione", "Sopravvivenza mediana", "Citazione"], '
    '"columns": ["protocol", "remission_rate", "median_survival", "citation_id"], '
    '"rows": ['
    '{"protocol": "CHOP-19", "remission_rate": "80-90%", "median_survival": "10-12 mesi", "citation": "[4]", "citation_id": 4}, '
    '{"protocol": "CHOP-25", "remission_rate": "80-90%", "median_survival": "10-12 mesi", "citation": "[5]", "citation_id": 5}'
    ']}}\n'
    '```'
)

CANNED_Q3_SYNTHESIS = (
    "Per la recidiva precoce dopo CHOP, le opzioni di rescue "
    "includono LOPP [1], LAP [2] e protocolli a base di "
    "rabacfosadina [3]. La scelta dipende dalla risposta "
    "iniziale e dalla tolleranza del paziente."
)

CANNED_Q4_SYNTHESIS = (
    "Il linfoma B-cell ha una prognosi significativamente "
    "migliore rispetto al T-cell [1][2]. La sopravvivenza "
    "mediana per B-cell e di 10-14 mesi contro 5-8 mesi "
    "per T-cell [1][2]."
)

CANNED_Q5_SYNTHESIS = (
    "Per neutropenia di grado 1-2, si consiglia il ritardo di "
    "1 settimana senza riduzione della dose [1]. Per grado 3-4, "
    "riduzione del 20-25% della dose di doxorubicina e "
    "considerare lo switch a protocolli alternativi [1][2]."
)

QUERY_RESPONSES = {
    "recidiva precoce": CANNED_Q3_SYNTHESIS,
    "prognosi linfoma t-cell": CANNED_Q4_SYNTHESIS,
    "aggiustamento dose": CANNED_Q5_SYNTHESIS,
    "chop-19 vs chop-25": CANNED_Q2_SYNTHESIS,
    "verifica citazioni": CANNED_VERIFICATION_SYNTHESIS,
}


@pytest.fixture(scope="session")
def case_repo():
    """In-memory case repository shared across session."""
    return InMemoryCaseRepository()


@pytest.fixture(scope="session")
def paper_repo():
    """In-memory paper repository shared across session."""
    return InMemoryPaperRepository()


@pytest.fixture(scope="session")
def app(paper_repo, case_repo):
    """
    Create the ASIA FastAPI application with test configuration.

    Uses in-memory repository and mocked LLM provider.
    """
    from asia.main import app as fastapi_app
    from asia.services.case_service import CaseService
    from asia.services.rag_pipeline import RAGPipeline

    fake_llm = FakeLLMProvider(CANNED_SYNTHESIS, QUERY_RESPONSES)
    fake_embedder = FakeEmbeddingProvider()

    rag_pipeline = RAGPipeline(
        llm_provider=fake_llm,
        embedding_provider=fake_embedder,
        paper_repository=paper_repo,
    )

    fastapi_app.state.rag_pipeline = rag_pipeline
    fastapi_app.state.case_service = CaseService(case_repo)

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
def clean_cases(app, case_repo):
    """
    Remove all cases and query logs between tests.
    Papers/corpus data is preserved (session-scoped).
    """
    yield
    case_repo.clear()


# ---------------------------------------------------------------------------
# Mock providers for external services
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Shared BDD Background steps
# ---------------------------------------------------------------------------


@given("the ASIA application is running", target_fixture="running_app")
def asia_running(test_client, seeded_corpus):
    """Verify the application is reachable via the test client."""
    return test_client


@given(
    "the corpus contains papers about canine multicentric lymphoma",
    target_fixture="corpus",
)
def corpus_seeded(seeded_corpus):
    """Corpus is seeded as a session fixture."""
    return seeded_corpus


# ---------------------------------------------------------------------------
# Mock LLM responses fixture
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
