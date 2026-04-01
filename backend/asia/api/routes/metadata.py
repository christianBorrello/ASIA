"""Metadata API routes for corpus info and pre-loaded queries.

Driving ports: GET /api/corpus-metadata, GET /api/pre-loaded-queries
"""

from fastapi import APIRouter

from asia.config.pre_loaded_queries import PRE_LOADED_QUERIES

router = APIRouter(prefix="/api", tags=["metadata"])

CORPUS_DATE = "2026-04-01"
PAPER_COUNT = 23
DISCLAIMER_TEXT = (
    "Questo strumento è un supporto informativo alla decisione clinica. "
    "Non sostituisce il giudizio del veterinario."
)


@router.get("/corpus-metadata")
async def get_corpus_metadata() -> dict:
    return {
        "corpus_date": CORPUS_DATE,
        "paper_count": PAPER_COUNT,
        "disclaimer_text": DISCLAIMER_TEXT,
    }


@router.get("/pre-loaded-queries")
async def get_pre_loaded_queries() -> dict:
    return {"queries": PRE_LOADED_QUERIES}
