"""Query endpoint -- POST /api/query for clinical question synthesis."""
from __future__ import annotations

import json
import logging

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/query", tags=["query"])

DISCLAIMER = (
    "ASIA fornisce sintesi basate sulla letteratura scientifica. "
    "Non sostituisce il giudizio clinico del veterinario."
)


class QueryRequest(BaseModel):
    text: str
    case_id: str | None = None
    stream: bool = False


@router.post("")
async def submit_query(body: QueryRequest, request: Request):
    """Submit a clinical query and receive synthesis with citations."""
    from asia.services.rag_pipeline import RAGPipeline

    rag_pipeline: RAGPipeline = request.app.state.rag_pipeline
    result = await rag_pipeline.execute_query(body.text)

    if body.stream:
        return _stream_response(result)

    if result.get("synthesis") is None and "message" in result:
        return {
            "query_text": body.text,
            "synthesis": None,
            "evidence_level": None,
            "sources": [],
            "message": result["message"],
            "scope_explanation": result.get("scope_explanation", result.get("scope", "")),
            "suggestions": result.get("suggestions", []),
            "disclaimer": DISCLAIMER,
        }

    response = {
        "query_text": body.text,
        "synthesis": result["synthesis"],
        "evidence_level": result["evidence_level"],
        "evidence_score": result.get("evidence_score"),
        "sources": result["sources"],
        "study_count": result.get("study_count"),
        "total_sample_size": result.get("total_sample_size"),
        "disclaimer": DISCLAIMER,
    }

    if "comparison_table" in result:
        response["comparison_table"] = result["comparison_table"]

    return response


def _stream_response(result: dict) -> StreamingResponse:
    """Return SSE streaming response."""

    async def event_generator():
        metadata = {
            "evidence_level": result["evidence_level"],
            "study_count": result.get("study_count"),
            "disclaimer": DISCLAIMER,
        }
        yield f"event: metadata\ndata: {json.dumps(metadata)}\n\n"

        sources = result["sources"]
        yield f"event: sources\ndata: {json.dumps(sources)}\n\n"

        synthesis = result["synthesis"]
        for i in range(0, len(synthesis), 20):
            token = synthesis[i : i + 20]
            yield f"event: token\ndata: {json.dumps({'text': token})}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
