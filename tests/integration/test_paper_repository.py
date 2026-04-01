"""Integration tests for PgPaperRepository adapter.

Validates real PostgreSQL + pgvector interaction:
- save paper with chunks and embeddings
- find_similar returns relevant chunks by cosine similarity
- get_by_doi retrieves saved paper
- ingestion run is logged
"""
import uuid
from datetime import datetime, timezone

import pytest

from asia.domain.models import Chunk, IngestionRun, Paper


@pytest.fixture
def db_url():
    return "postgresql://asia:asia@localhost:5432/asia"


@pytest.fixture
def paper_factory():
    def _make(doi_suffix: str = "001") -> Paper:
        return Paper(
            id=uuid.uuid4(),
            title=f"CHOP Protocol for Canine Lymphoma {doi_suffix}",
            authors=[{"name": "Smith J"}],
            year=2023,
            source="seed",
            doi=f"10.1234/test-{doi_suffix}-{uuid.uuid4().hex[:8]}",
            journal="Vet Oncology",
            abstract_text="CHOP chemotherapy protocol is the standard first-line treatment for canine multicentric B-cell lymphoma.",
            study_type="clinical_trial",
            sample_size=50,
        )

    return _make


@pytest.fixture
def chunk_factory():
    def _make(paper_id: uuid.UUID, embedding: list[float], index: int = 0) -> Chunk:
        return Chunk(
            id=uuid.uuid4(),
            paper_id=paper_id,
            chunk_index=index,
            chunk_text="CHOP protocol combines cyclophosphamide, doxorubicin, vincristine, and prednisone for B-cell lymphoma treatment.",
            chunk_type="abstract",
            embedding=embedding,
            token_count=20,
        )

    return _make


@pytest.mark.anyio
async def test_save_and_find_similar(db_url, paper_factory, chunk_factory):
    """Save a paper with chunks, then find similar chunks via vector search."""
    from asia.adapters.pg_paper_repository import PgPaperRepository

    repo = PgPaperRepository(db_url)
    try:
        paper = paper_factory("sim")
        # 384-dim embedding simulating CHOP-related content
        embedding = [0.1] * 384
        chunk = chunk_factory(paper.id, embedding)

        await repo.save(paper, [chunk])

        # Query with a similar embedding
        query_embedding = [0.1] * 384
        results = await repo.find_similar(query_embedding, top_k=5)

        assert len(results) >= 1
        found_texts = [c.chunk_text for c in results]
        assert any("CHOP" in t for t in found_texts)
    finally:
        await repo.close()


@pytest.mark.anyio
async def test_get_by_doi(db_url, paper_factory, chunk_factory):
    """Save a paper and retrieve it by DOI."""
    from asia.adapters.pg_paper_repository import PgPaperRepository

    repo = PgPaperRepository(db_url)
    try:
        paper = paper_factory("doi")
        embedding = [0.05] * 384
        chunk = chunk_factory(paper.id, embedding)

        await repo.save(paper, [chunk])

        retrieved = await repo.get_by_doi(paper.doi)
        assert retrieved is not None
        assert retrieved.title == paper.title
        assert retrieved.doi == paper.doi
    finally:
        await repo.close()


@pytest.mark.anyio
async def test_save_ingestion_run(db_url):
    """Log an ingestion run to the database."""
    from asia.adapters.pg_paper_repository import PgPaperRepository

    repo = PgPaperRepository(db_url)
    try:
        run = IngestionRun(
            id=uuid.uuid4(),
            started_at=datetime.now(timezone.utc),
            status="completed",
            papers_fetched=5,
            papers_new=5,
            source="seed",
        )
        await repo.save_ingestion_run(run)

        saved_run = await repo.get_ingestion_run(run.id)
        assert saved_run is not None
        assert saved_run.status == "completed"
        assert saved_run.papers_fetched == 5
    finally:
        await repo.close()
