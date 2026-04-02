"""Standalone seed runner -- populates the ASIA corpus from seed_papers.py.

Usage:
    cd backend && python3 -m db.seeds.run_seed

Connects to PostgreSQL, generates embeddings with sentence-transformers,
and inserts papers + chunks into the database.
"""
from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://asia:asia@localhost:5432/asia",
)


async def _seed(database_url: str) -> None:
    from asia.adapters.pg_paper_repository import PgPaperRepository
    from asia.adapters.sentence_transformer_embedder import SentenceTransformerEmbedder
    from asia.domain.models import Chunk, Paper
    from db.seeds.seed_papers import SEED_PAPERS

    model_name = os.environ.get("EMBEDDING_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
    repo = PgPaperRepository(database_url)
    embedder = SentenceTransformerEmbedder(model_name=model_name)

    total = len(SEED_PAPERS)
    inserted = 0
    skipped = 0

    print(f"Seeding {total} papers into {database_url.split('@')[-1]} ...")

    for idx, raw in enumerate(SEED_PAPERS, 1):
        doi = raw.get("doi", "")
        if doi:
            existing = await repo.get_by_doi(doi)
            if existing is not None:
                skipped += 1
                print(f"  [{idx}/{total}] SKIP (exists): {raw['title'][:60]}")
                continue

        paper_id = uuid.uuid4()
        paper = Paper(
            id=paper_id,
            title=raw["title"],
            authors=raw["authors"],
            year=raw["year"],
            source="seed",
            doi=doi or None,
            journal=raw.get("journal"),
            abstract_text=raw.get("abstract"),
            study_type=raw.get("study_type"),
            sample_size=raw.get("sample_size"),
            species="canine",
            cancer_type=_infer_cancer_type(raw),
            ingested_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Build chunk from abstract
        abstract = raw.get("abstract", "")
        chunks: list[Chunk] = []
        if abstract:
            embedding = embedder.embed_text(abstract)
            chunks.append(
                Chunk(
                    id=uuid.uuid4(),
                    paper_id=paper_id,
                    chunk_index=0,
                    chunk_text=abstract,
                    chunk_type="abstract",
                    embedding=embedding,
                    token_count=len(abstract.split()),
                    created_at=datetime.now(timezone.utc),
                )
            )

        await repo.save(paper, chunks)
        inserted += 1
        print(f"  [{idx}/{total}] OK: {raw['title'][:60]}")

    await repo.close()
    print(f"\nDone: {inserted} inserted, {skipped} skipped, {total} total.")


def _infer_cancer_type(paper: dict) -> str:
    """Infer cancer type from paper content for categorization."""
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    carcinoma_keywords = [
        "thymoma", "thymic carcinoma", "carcinoma", "adenocarcinoma",
        "hypercalcemia", "pthrp", "thyroidectomy", "cytokeratin",
    ]
    if any(kw in text for kw in carcinoma_keywords):
        return "carcinoma"
    return "multicentric_lymphoma"


def main() -> None:
    """Entry point for the seed runner."""
    asyncio.run(_seed(DATABASE_URL))


if __name__ == "__main__":
    main()
