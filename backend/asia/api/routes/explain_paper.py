"""Explain Paper endpoint -- POST /api/explain-paper for paper summaries."""
from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/explain-paper", tags=["explain-paper"])


class ExplainPaperRequest(BaseModel):
    doi: str


@router.post("")
async def explain_paper(body: ExplainPaperRequest, request: Request):
    """Submit a DOI and receive a structured clinical summary."""
    from asia.services.paper_explainer import PaperExplainer

    paper_explainer: PaperExplainer = request.app.state.paper_explainer

    result = await paper_explainer.explain(body.doi)

    if result.get("error"):
        from fastapi.responses import JSONResponse

        # Empty DOI -> 400, not found -> 404
        status = 400 if not body.doi.strip() else 404
        return JSONResponse(
            status_code=status,
            content=result,
        )

    return result
