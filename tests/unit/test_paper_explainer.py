"""Unit tests for PaperExplainer service.

Tests enter through PaperExplainer driving port and assert observable outcomes.
LLM and repository are mocked at port boundaries.

Test Budget: 3 behaviors x 2 = 6 max
  (paper in corpus -> structured summary, paper not found -> Italian error,
   empty DOI -> validation error)
Actual: 3 tests
"""
from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import pytest

from asia.domain.models import Chunk, Paper


# ---------------------------------------------------------------------------
# Fakes at port boundaries
# ---------------------------------------------------------------------------

CANNED_EXPLANATION = (
    "Obiettivo: Valutare il protocollo CHOP come trattamento di prima linea.\n"
    "Metodologia: Studio clinico prospettico su 120 cani.\n"
    "Risultati chiave: Tasso di risposta dell'86%, sopravvivenza mediana 397 giorni.\n"
    "Implicazioni pratiche: CHOP rimane il gold standard per linfoma B-cell.\n"
    "Contesto nel corpus: Questo studio e uno dei riferimenti principali per il protocollo CHOP."
)


class StubLLMProvider:
    """Stub LLM that returns a pre-canned explanation."""

    def __init__(self, response: str) -> None:
        self._response = response

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        return self._response

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        for word in self._response.split(" "):
            yield word + " "


class InMemoryPaperRepository:
    """Fake repository with DOI lookup."""

    def __init__(self, papers: list[Paper], chunks: list[Chunk] | None = None) -> None:
        self._papers = {p.id: p for p in papers}
        self._chunks = chunks or []

    async def get_by_doi(self, doi: str) -> Paper | None:
        for p in self._papers.values():
            if p.doi == doi:
                return p
        return None

    async def get_by_id(self, paper_id: uuid.UUID) -> Paper | None:
        return self._papers.get(paper_id)

    async def find_similar(
        self, embedding: list[float], top_k: int = 10
    ) -> list[Chunk]:
        return self._chunks[:top_k]

    async def save(self, paper: Paper, chunks: list[Chunk] | None = None) -> None:
        pass


def _make_paper(doi: str = "10.1111/jvim.12345") -> Paper:
    return Paper(
        id=uuid.uuid4(),
        title="CHOP-based chemotherapy for canine lymphoma",
        authors=[{"name": "Garrett LD"}, {"name": "Thamm DH"}],
        year=2014,
        source="seed",
        doi=doi,
        journal="Journal of Veterinary Internal Medicine",
        abstract_text="The CHOP protocol is the gold standard for canine lymphoma.",
        study_type="clinical_trial",
        sample_size=120,
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
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_explain_paper_in_corpus_returns_structured_summary():
    """PaperExplainer returns structured summary with 5 sections for paper in corpus."""
    from asia.services.paper_explainer import PaperExplainer

    paper = _make_paper(doi="10.1111/jvim.12345")
    chunk = _make_chunk(paper)
    repo = InMemoryPaperRepository(papers=[paper], chunks=[chunk])
    llm = StubLLMProvider(CANNED_EXPLANATION)

    explainer = PaperExplainer(paper_repository=repo, llm_provider=llm)
    result = await explainer.explain(doi="10.1111/jvim.12345")

    assert result["title"] == paper.title
    assert result["authors"] == paper.authors
    assert result["year"] == paper.year
    summary = result["summary"]
    summary_text = str(summary).lower()
    for section in ["obiettivo", "metodologia", "risultati", "implicazioni", "contesto"]:
        assert section in summary_text, f"Missing section '{section}' in summary"


@pytest.mark.anyio
async def test_explain_paper_not_in_corpus_returns_italian_error():
    """PaperExplainer returns Italian error message when DOI not found."""
    from asia.services.paper_explainer import PaperExplainer

    repo = InMemoryPaperRepository(papers=[])
    llm = StubLLMProvider("")

    explainer = PaperExplainer(paper_repository=repo, llm_provider=llm)
    result = await explainer.explain(doi="10.9999/nonexistent")

    assert result.get("error") is True
    message = result["message"].lower()
    assert "non" in message
    assert "doi" in message or "corpus" in message


@pytest.mark.anyio
async def test_explain_paper_empty_doi_returns_validation_error():
    """PaperExplainer returns validation error for empty DOI."""
    from asia.services.paper_explainer import PaperExplainer

    repo = InMemoryPaperRepository(papers=[])
    llm = StubLLMProvider("")

    explainer = PaperExplainer(paper_repository=repo, llm_provider=llm)
    result = await explainer.explain(doi="")

    assert result.get("error") is True
    message = result["message"].lower()
    assert "doi" in message
