"""Ingestion service orchestrating paper seeding with embeddings."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from asia.domain.models import Chunk, IngestionRun, Paper
from asia.ports.embedding_provider import EmbeddingProvider

logger = logging.getLogger(__name__)


class IngestionService:
    """Orchestrates ingestion: takes raw paper data, generates embeddings, stores via repository."""

    def __init__(self, embedding_provider: EmbeddingProvider, paper_repository) -> None:
        self._embedder = embedding_provider
        self._repo = paper_repository

    async def ingest_seed_papers(self, papers_data: list[dict]) -> IngestionRun:
        run = IngestionRun(
            id=uuid.uuid4(),
            started_at=datetime.now(timezone.utc),
            status="running",
            source="seed",
        )

        errors: list[dict] = []
        papers_new = 0

        for paper_data in papers_data:
            try:
                paper = Paper(
                    id=uuid.uuid4(),
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

                chunks = self._create_chunks(paper)
                await self._repo.save(paper, chunks)
                papers_new += 1
                logger.info("Ingested paper: %s", paper.title)

            except Exception as exc:
                error_entry = {"paper": paper_data.get("title", "unknown"), "error": str(exc)}
                errors.append(error_entry)
                logger.error("Failed to ingest paper '%s': %s", paper_data.get("title"), exc)

        run.completed_at = datetime.now(timezone.utc)
        run.status = "completed" if not errors else "completed_with_errors"
        run.papers_fetched = len(papers_data)
        run.papers_new = papers_new
        run.errors = errors if errors else None

        await self._repo.save_ingestion_run(run)
        return run

    def _create_chunks(self, paper: Paper) -> list[Chunk]:
        chunks: list[Chunk] = []
        texts_to_embed: list[str] = []
        chunk_metas: list[tuple[int, str, str]] = []

        if paper.abstract_text:
            texts_to_embed.append(paper.abstract_text)
            chunk_metas.append((0, paper.abstract_text, "abstract"))

        title_text = f"{paper.title}. {paper.abstract_text or ''}"
        texts_to_embed.append(title_text)
        chunk_metas.append((len(chunk_metas), title_text, "title_abstract"))

        if not texts_to_embed:
            return chunks

        embeddings = self._embedder.embed_batch(texts_to_embed)

        for (index, text, chunk_type), embedding in zip(chunk_metas, embeddings):
            chunks.append(
                Chunk(
                    id=uuid.uuid4(),
                    paper_id=paper.id,
                    chunk_index=index,
                    chunk_text=text,
                    chunk_type=chunk_type,
                    embedding=embedding,
                    token_count=len(text.split()),
                )
            )

        return chunks
