"""Case management API routes.

Driving ports: POST /api/cases, GET /api/cases/{id}
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
    """Get a case by ID."""
    from asia.services.case_service import CaseService

    case_service: CaseService = request.app.state.case_service
    case = await case_service.get_case(case_id)
    if case is None:
        return JSONResponse(status_code=404, content={"detail": "Case not found"})
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
        "queries": [],
    }
