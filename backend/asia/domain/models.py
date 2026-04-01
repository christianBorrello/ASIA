from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime


class EvidenceLevel(enum.Enum):
    ALTO = "ALTO"
    MODERATO = "MODERATO"
    BASSO = "BASSO"


@dataclass
class Paper:
    id: uuid.UUID
    title: str
    authors: list[dict]
    year: int
    source: str
    pmid: str | None = None
    doi: str | None = None
    journal: str | None = None
    abstract_text: str | None = None
    study_type: str | None = None
    sample_size: int | None = None
    species: str = "canine"
    cancer_type: str = "multicentric_lymphoma"
    citation_count: int = 0
    tldr: str | None = None
    is_retracted: bool = False
    is_open_access: bool = False
    quality_score: float | None = None
    ingested_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Chunk:
    id: uuid.UUID
    paper_id: uuid.UUID
    chunk_index: int
    chunk_text: str
    chunk_type: str
    embedding: list[float]
    token_count: int | None = None
    created_at: datetime | None = None
    similarity: float | None = None


@dataclass
class Case:
    id: uuid.UUID
    patient_name: str
    diagnosis: str
    breed: str | None = None
    age: str | None = None
    stage: str | None = None
    immunophenotype: str | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Citation:
    paper_id: uuid.UUID
    title: str
    authors: list[str]
    year: int
    relevance_score: float


@dataclass
class CaseQuery:
    id: uuid.UUID
    query_text: str
    case_id: uuid.UUID | None = None
    response_synthesis: str | None = None
    response_citations: list[dict] | None = None
    evidence_level: EvidenceLevel | None = None
    evidence_score: float | None = None
    study_count: int | None = None
    total_sample_size: int | None = None
    comparison_table: list[dict] | None = None
    reflection_note: str | None = None
    retrieval_chunks: list[dict] | None = None
    response_time_ms: int | None = None
    created_at: datetime | None = None


@dataclass
class IngestionRun:
    id: uuid.UUID
    started_at: datetime
    status: str
    completed_at: datetime | None = None
    papers_fetched: int = 0
    papers_new: int = 0
    papers_updated: int = 0
    errors: list[dict] | None = None
    source: str | None = None
