"""PaperRepository adapter using asyncpg + pgvector."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

import asyncpg
from pgvector.asyncpg import register_vector

from asia.domain.models import Chunk, IngestionRun, Paper


class PgPaperRepository:
    """PostgreSQL adapter for paper storage and vector similarity search."""

    def __init__(self, database_url: str) -> None:
        self._database_url = database_url
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                self._database_url,
                min_size=1,
                max_size=5,
                init=register_vector,
            )
        return self._pool

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def save(self, paper: Paper, chunks: list[Chunk] | None = None) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO papers (
                        id, pmid, doi, title, authors, journal, year,
                        abstract_text, study_type, sample_size, species,
                        cancer_type, citation_count, tldr, is_retracted,
                        is_open_access, quality_score, source, ingested_at, updated_at
                    ) VALUES (
                        $1, $2, $3, $4, $5::jsonb, $6, $7,
                        $8, $9, $10, $11,
                        $12, $13, $14, $15,
                        $16, $17, $18, $19, $20
                    )
                    ON CONFLICT (doi) DO UPDATE SET
                        title = EXCLUDED.title,
                        updated_at = NOW()
                    """,
                    paper.id,
                    paper.pmid,
                    paper.doi,
                    paper.title,
                    json.dumps(paper.authors),
                    paper.journal,
                    paper.year,
                    paper.abstract_text,
                    paper.study_type,
                    paper.sample_size,
                    paper.species,
                    paper.cancer_type,
                    paper.citation_count,
                    paper.tldr,
                    paper.is_retracted,
                    paper.is_open_access,
                    paper.quality_score,
                    paper.source,
                    paper.ingested_at or datetime.now(timezone.utc),
                    paper.updated_at or datetime.now(timezone.utc),
                )

                if chunks:
                    for chunk in chunks:
                        await conn.execute(
                            """
                            INSERT INTO chunks (
                                id, paper_id, chunk_index, chunk_text,
                                chunk_type, embedding, token_count, created_at
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                            """,
                            chunk.id,
                            chunk.paper_id,
                            chunk.chunk_index,
                            chunk.chunk_text,
                            chunk.chunk_type,
                            chunk.embedding,
                            chunk.token_count,
                            chunk.created_at or datetime.now(timezone.utc),
                        )

    async def find_similar(
        self, embedding: list[float], top_k: int = 10
    ) -> list[Chunk]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, paper_id, chunk_index, chunk_text, chunk_type,
                       embedding, token_count, created_at
                FROM chunks
                ORDER BY embedding <=> $1
                LIMIT $2
                """,
                embedding,
                top_k,
            )
            return [
                Chunk(
                    id=row["id"],
                    paper_id=row["paper_id"],
                    chunk_index=row["chunk_index"],
                    chunk_text=row["chunk_text"],
                    chunk_type=row["chunk_type"],
                    embedding=list(row["embedding"]),
                    token_count=row["token_count"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]

    async def get_by_doi(self, doi: str) -> Paper | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM papers WHERE doi = $1", doi
            )
            if row is None:
                return None
            return self._row_to_paper(row)

    async def get_by_id(self, paper_id: uuid.UUID) -> Paper | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM papers WHERE id = $1", paper_id
            )
            if row is None:
                return None
            return self._row_to_paper(row)

    async def save_ingestion_run(self, run: IngestionRun) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO ingestion_runs (
                    id, started_at, completed_at, status,
                    papers_fetched, papers_new, papers_updated,
                    errors, source
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9)
                """,
                run.id,
                run.started_at,
                run.completed_at,
                run.status,
                run.papers_fetched,
                run.papers_new,
                run.papers_updated,
                json.dumps(run.errors) if run.errors else None,
                run.source,
            )

    async def get_ingestion_run(self, run_id: uuid.UUID) -> IngestionRun | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM ingestion_runs WHERE id = $1", run_id
            )
            if row is None:
                return None
            return IngestionRun(
                id=row["id"],
                started_at=row["started_at"],
                status=row["status"],
                completed_at=row["completed_at"],
                papers_fetched=row["papers_fetched"],
                papers_new=row["papers_new"],
                papers_updated=row["papers_updated"],
                errors=row["errors"],
                source=row["source"],
            )

    @staticmethod
    def _row_to_paper(row: asyncpg.Record) -> Paper:
        authors = row["authors"]
        if isinstance(authors, str):
            authors = json.loads(authors)
        return Paper(
            id=row["id"],
            title=row["title"],
            authors=authors,
            year=row["year"],
            source=row["source"],
            pmid=row["pmid"],
            doi=row["doi"],
            journal=row["journal"],
            abstract_text=row["abstract_text"],
            study_type=row["study_type"],
            sample_size=row["sample_size"],
            species=row["species"],
            cancer_type=row["cancer_type"],
            citation_count=row["citation_count"],
            tldr=row["tldr"],
            is_retracted=row["is_retracted"],
            is_open_access=row["is_open_access"],
            quality_score=row["quality_score"],
            ingested_at=row["ingested_at"],
            updated_at=row["updated_at"],
        )
