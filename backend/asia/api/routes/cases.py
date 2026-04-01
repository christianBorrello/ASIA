"""Case management API routes.

Driving ports: POST /api/cases, GET /api/cases/{id}, POST /api/cases/{id}/query
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/cases", tags=["cases"])


class CreateCaseRequest(BaseModel):
    patient_name: str
    diagnosis: str
    breed: str | None = None
    age: str | None = None
    stage: str | None = None
    immunophenotype: str | None = None
    notes: str | None = None


class CaseQueryRequest(BaseModel):
    text: str


@router.post("")
async def create_case(body: CreateCaseRequest, request: Request):
    """Create a new patient case."""
    from asia.services.case_service import CaseService

    case_service: CaseService = request.app.state.case_service
    case = await case_service.create_case(
        patient_name=body.patient_name,
        diagnosis=body.diagnosis,
        breed=body.breed,
        age=body.age,
        stage=body.stage,
        immunophenotype=body.immunophenotype,
        notes=body.notes,
    )
    return JSONResponse(
        status_code=201,
        content={
            "id": str(case.id),
            "patient_name": case.patient_name,
            "diagnosis": case.diagnosis,
            "breed": case.breed,
            "age": case.age,
            "stage": case.stage,
            "immunophenotype": case.immunophenotype,
            "notes": case.notes,
            "created_at": case.created_at.isoformat() if case.created_at else None,
            "updated_at": case.updated_at.isoformat() if case.updated_at else None,
        },
    )


@router.get("/{case_id}")
async def get_case(case_id: uuid.UUID, request: Request):
    """Get a case by ID with query history."""
    from asia.services.case_service import CaseService

    case_service: CaseService = request.app.state.case_service
    case = await case_service.get_case(case_id)
    if case is None:
        return JSONResponse(status_code=404, content={"detail": "Case not found"})

    queries = await case_service.get_case_queries(case_id)
    sorted_queries = sorted(queries, key=lambda q: q.created_at or "", reverse=True)

    return {
        "id": str(case.id),
        "patient_name": case.patient_name,
        "diagnosis": case.diagnosis,
        "breed": case.breed,
        "age": case.age,
        "stage": case.stage,
        "immunophenotype": case.immunophenotype,
        "notes": case.notes,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "updated_at": case.updated_at.isoformat() if case.updated_at else None,
        "queries": [
            {
                "id": str(q.id),
                "query_text": q.query_text,
                "synthesis": q.response_synthesis,
                "sources": q.response_citations or [],
                "evidence_score": q.evidence_score,
                "study_count": q.study_count,
                "created_at": q.created_at.isoformat() if q.created_at else None,
            }
            for q in sorted_queries
        ],
    }


@router.post("/{case_id}/query")
async def query_case(case_id: uuid.UUID, body: CaseQueryRequest, request: Request):
    """Submit a query within a case context."""
    from asia.services.case_service import CaseService

    case_service: CaseService = request.app.state.case_service
    try:
        result = await case_service.query_case(case_id, body.text)
    except ValueError:
        return JSONResponse(status_code=404, content={"detail": "Case not found"})
    return result
