"""Unit tests for RAG pipeline query flow.

Tests enter through the RAGPipeline driving port and assert observable outcomes.
LLM and repository are mocked at port boundaries.

Test Budget: 5 behaviors x 2 = 10 max
  (query produces synthesis, evidence scoring, comparison query detection,
   comparison query produces table, non-comparison query produces no table)
Actual: 5 tests (2 original + 1 parametrized detection + 1 comparison table + 1 no table)
"""
from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import pytest

from asia.domain.models import Chunk, Paper


# ---------------------------------------------------------------------------
# Fakes at port boundaries
# ---------------------------------------------------------------------------

class StubLLMProvider:
    """Stub LLM that returns a pre-canned synthesis."""

    def __init__(self, response: str) -> None:
        self._response = response

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
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


def _make_paper(
    study_type: str = "retrospective",
    sample_size: int = 100,
    year: int = 2020,
    title: str = "Test paper",
    doi: str | None = None,
) -> Paper:
    paper_id = uuid.uuid4()
    return Paper(
        id=paper_id,
        title=title,
        authors=[{"name": "Author A"}],
        year=year,
        source="seed",
        doi=doi or f"10.1234/{paper_id}",
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


SYNTHESIS_WITH_CITATIONS = (
    "Il protocollo CHOP produce remissione nell'80-90% dei casi [1][2]. "
    "La sopravvivenza mediana e di 10-14 mesi [1]."
)

SYNTHESIS_CITING_ONLY_FIRST_TWO = (
    "Il protocollo raccomandato e il CHOP [1][2]. "
    "La remissione e elevata [1]."
)


@pytest.mark.anyio
async def test_rag_pipeline_produces_synthesis_with_citations_and_evidence():
    """RAGPipeline.execute_query returns synthesis text, sources, and evidence level."""
    from asia.services.rag_pipeline import RAGPipeline

    paper1 = _make_paper(study_type="meta_analysis", sample_size=400)
    paper2 = _make_paper(study_type="randomized_controlled_trial", sample_size=200)
    chunk1 = _make_chunk(paper1)
    chunk2 = _make_chunk(paper2)

    pipeline = RAGPipeline(
        llm_provider=StubLLMProvider(SYNTHESIS_WITH_CITATIONS),
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper1, paper2],
            chunks=[chunk1, chunk2],
        ),
    )

    result = await pipeline.execute_query("Qual e il protocollo CHOP?")

    assert result["synthesis"] == SYNTHESIS_WITH_CITATIONS
    assert len(result["sources"]) >= 1
    assert result["evidence_level"] in ("ALTO", "MODERATO", "BASSO")
    for source in result["sources"]:
        assert "author" in source
        assert "year" in source
        assert "doi" in source


@pytest.mark.anyio
async def test_sources_match_citation_markers_one_to_one():
    """Source count equals unique citation marker count -- uncited papers excluded."""
    from asia.services.rag_pipeline import RAGPipeline

    paper1 = _make_paper(title="Cited paper 1", doi="10.1234/cited1")
    paper2 = _make_paper(title="Cited paper 2", doi="10.1234/cited2")
    paper3 = _make_paper(title="Uncited paper 3", doi="10.1234/uncited3")
    chunk1 = _make_chunk(paper1)
    chunk2 = _make_chunk(paper2)
    chunk3 = _make_chunk(paper3)

    pipeline = RAGPipeline(
        llm_provider=StubLLMProvider(SYNTHESIS_CITING_ONLY_FIRST_TWO),
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper1, paper2, paper3],
            chunks=[chunk1, chunk2, chunk3],
        ),
    )

    result = await pipeline.execute_query("Test query")

    import re
    unique_markers = set(re.findall(r"\[(\d+)\]", result["synthesis"]))
    sources = result["sources"]

    # 1:1 mapping: source count equals unique marker count
    assert len(sources) == len(unique_markers), (
        f"Sources ({len(sources)}) != markers ({len(unique_markers)})"
    )
    # Every marker has a corresponding source entry
    source_ids = {str(s["id"]) for s in sources}
    assert unique_markers.issubset(source_ids), (
        f"Unmatched markers: {unique_markers - source_ids}"
    )


@pytest.mark.parametrize(
    "study_types_and_sizes,expected_level",
    [
        # ALTO: meta_analysis(20) + count_bonus(3) + sample_bonus(~8) = 31+
        # actually need >= 40. meta_analysis(20) + 2 papers(6) + log2(600)~9.2->8 = 34
        # 3 papers: meta(20) + rct(15) + prospective(12) -> max(20) + count_bonus(9) + sample_bonus(8) = 37
        # Let's use 4 papers with strong types
        (
            [("meta_analysis", 500), ("randomized_controlled_trial", 300), ("prospective", 200), ("retrospective", 100)],
            "ALTO",
        ),
        # MODERATO: >= 20
        (
            [("retrospective", 100), ("case_series", 50)],
            "MODERATO",
        ),
        # BASSO: < 20
        (
            [("case_report", 5)],
            "BASSO",
        ),
    ],
    ids=["alto", "moderato", "basso"],
)
@pytest.mark.anyio
async def test_evidence_scoring_levels(study_types_and_sizes, expected_level):
    """Evidence level computed from cited papers matches expected threshold."""
    from asia.services.rag_pipeline import RAGPipeline

    papers = []
    chunks = []
    citation_refs = []
    for i, (study_type, sample_size) in enumerate(study_types_and_sizes, start=1):
        paper = _make_paper(study_type=study_type, sample_size=sample_size)
        papers.append(paper)
        chunks.append(_make_chunk(paper))
        citation_refs.append(f"[{i}]")

    synthesis = " ".join(f"Affermazione {citation_refs[i]}." for i in range(len(papers)))

    pipeline = RAGPipeline(
        llm_provider=StubLLMProvider(synthesis),
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(papers=papers, chunks=chunks),
    )

    result = await pipeline.execute_query("Test query")
    assert result["evidence_level"] == expected_level


# ---------------------------------------------------------------------------
# Comparison query tests (Step 02-08)
# Test Budget: 3 behaviors x 2 = 6 max | Actual: 3 tests
# ---------------------------------------------------------------------------

COMPARISON_SYNTHESIS_WITH_TABLE = (
    "CHOP-19 e CHOP-25 hanno outcome equivalenti [1][2].\n\n"
    '```json\n'
    '{"comparison_table": {'
    '"headers": ["Protocollo", "Tasso remissione", "Sopravvivenza mediana", "Citazione"], '
    '"rows": ['
    '{"protocol": "CHOP-19", "remission_rate": "80-90%", "median_survival": "12 mesi", "citation": "[1]"}, '
    '{"protocol": "CHOP-25", "remission_rate": "80-90%", "median_survival": "12 mesi", "citation": "[2]"}'
    ']}}\n'
    '```'
)


class KeywordRoutingLLMStub:
    """Stub LLM that returns comparison table JSON when query contains comparison keywords."""

    def __init__(self, default_response: str, comparison_response: str) -> None:
        self._default = default_response
        self._comparison = comparison_response

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        if "tabella comparativa" in (system_prompt or "").lower() or "tabella comparativa" in prompt.lower():
            return self._comparison
        return self._default

    async def stream(self, prompt: str, system_prompt: str | None = None):
        response = await self.generate(prompt, system_prompt)
        for word in response.split(" "):
            yield word + " "


@pytest.mark.parametrize(
    "query_text,expected_is_comparison",
    [
        ("CHOP-19 vs CHOP-25: differenze negli outcome?", True),
        ("Confronto tra CHOP e LOPP", True),
        ("Differenze tra protocolli di rescue", True),
        ("Rispetto a CHOP, come funziona LOPP?", True),
        ("CHOP-19 versus CHOP-25", True),
        ("Comparazione protocolli chemioterapici", True),
        ("Meglio tra CHOP e COP?", True),
        ("Qual e il protocollo di prima linea?", False),
        ("Prognosi linfoma T-cell?", False),
        ("Aggiustamento dose doxorubicina per neutropenia?", False),
    ],
    ids=[
        "vs-keyword", "confronto", "differenze", "rispetto-a",
        "versus", "comparazione", "meglio-tra",
        "standard-first-line", "standard-prognosis", "standard-dose",
    ],
)
def test_comparison_query_detection(query_text, expected_is_comparison):
    """is_comparison_query classifies Italian comparison keywords correctly."""
    from asia.domain.query_types import is_comparison_query

    assert is_comparison_query(query_text) is expected_is_comparison


@pytest.mark.anyio
async def test_comparison_query_produces_comparison_table():
    """RAGPipeline returns comparison_table with rows and citations for comparison queries."""
    from asia.services.rag_pipeline import RAGPipeline

    paper1 = _make_paper(title="CHOP-19 study", doi="10.1234/chop19")
    paper2 = _make_paper(title="CHOP-25 study", doi="10.1234/chop25")
    chunk1 = _make_chunk(paper1)
    chunk2 = _make_chunk(paper2)

    pipeline = RAGPipeline(
        llm_provider=KeywordRoutingLLMStub(
            default_response=SYNTHESIS_WITH_CITATIONS,
            comparison_response=COMPARISON_SYNTHESIS_WITH_TABLE,
        ),
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper1, paper2],
            chunks=[chunk1, chunk2],
        ),
    )

    result = await pipeline.execute_query("CHOP-19 vs CHOP-25: differenze negli outcome?")

    assert "comparison_table" in result
    table = result["comparison_table"]
    assert "rows" in table
    assert len(table["rows"]) >= 2
    for row in table["rows"]:
        assert "protocol" in row
        assert "remission_rate" in row
        assert "median_survival" in row
        assert "citation" in row


@pytest.mark.anyio
async def test_non_comparison_query_has_no_comparison_table():
    """RAGPipeline returns no comparison_table for standard queries."""
    from asia.services.rag_pipeline import RAGPipeline

    paper1 = _make_paper()
    chunk1 = _make_chunk(paper1)

    pipeline = RAGPipeline(
        llm_provider=KeywordRoutingLLMStub(
            default_response=SYNTHESIS_WITH_CITATIONS,
            comparison_response=COMPARISON_SYNTHESIS_WITH_TABLE,
        ),
        embedding_provider=StubEmbeddingProvider(),
        paper_repository=InMemoryPaperRepository(
            papers=[paper1],
            chunks=[chunk1],
        ),
    )

    result = await pipeline.execute_query("Qual e il protocollo di prima linea?")

    assert result.get("comparison_table") is None
