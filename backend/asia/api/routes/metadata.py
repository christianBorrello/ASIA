"""Metadata API routes for corpus info, pre-loaded queries, and LLM status.

Driving ports: GET /api/corpus-metadata, GET /api/pre-loaded-queries, GET /api/llm-status
"""

from datetime import date

from fastapi import APIRouter, Request

from asia.config.pre_loaded_queries import PRE_LOADED_QUERIES

router = APIRouter(prefix="/api", tags=["metadata"])

DISCLAIMER_TEXT = (
    "Questo strumento è un supporto informativo alla decisione clinica. "
    "Non sostituisce il giudizio del veterinario."
)


@router.get("/corpus-metadata")
async def get_corpus_metadata(request: Request) -> dict:
    """Return corpus stats from the database."""
    repo = request.app.state.rag_pipeline._repo

    try:
        pool = await repo._get_pool()
        async with pool.acquire() as conn:
            paper_count = await conn.fetchval("SELECT COUNT(*) FROM papers")
            latest_date = await conn.fetchval(
                "SELECT MAX(ingested_at)::date FROM papers"
            )
    except Exception:
        paper_count = 0
        latest_date = None

    return {
        "corpus_date": str(latest_date) if latest_date else str(date.today()),
        "paper_count": paper_count or 0,
        "disclaimer_text": DISCLAIMER_TEXT,
    }


@router.get("/pre-loaded-queries")
async def get_pre_loaded_queries() -> dict:
    return {"queries": PRE_LOADED_QUERIES}


@router.get("/llm-status")
async def get_llm_status(request: Request) -> dict:
    """Check primary LLM model availability."""
    llm = request.app.state.rag_pipeline._llm
    available = await llm.check_availability()
    return {
        "primary_available": available,
        "model": llm._model,
    }
