"""Case management service -- driving port for case operations."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from asia.domain.context_injection import build_patient_context
from asia.domain.models import Case, CaseQuery
from asia.ports.case_repository import CaseRepository


class CaseService:
    """Application service for case management."""

    def __init__(self, case_repository: CaseRepository, rag_pipeline=None) -> None:
        self._case_repository = case_repository
        self._rag_pipeline = rag_pipeline

    async def create_case(
        self,
        patient_name: str,
        diagnosis: str,
        breed: str | None = None,
        age: str | None = None,
        stage: str | None = None,
        immunophenotype: str | None = None,
        notes: str | None = None,
    ) -> Case:
        now = datetime.now(timezone.utc)
        case = Case(
            id=uuid.uuid4(),
            patient_name=patient_name,
            diagnosis=diagnosis,
            breed=breed,
            age=age,
            stage=stage,
            immunophenotype=immunophenotype,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        return await self._case_repository.create(case)

    async def get_case(self, case_id: uuid.UUID) -> Case | None:
        return await self._case_repository.get(case_id)

    async def get_case_queries(self, case_id: uuid.UUID) -> list[CaseQuery]:
        return await self._case_repository.list_queries(case_id)

    async def query_case(self, case_id: uuid.UUID, query_text: str) -> dict:
        """Execute a query within a case context."""
        case = await self._case_repository.get(case_id)
        if case is None:
            raise ValueError(f"Case {case_id} not found")

        context_query = build_patient_context(
            patient_name=case.patient_name,
            diagnosis=case.diagnosis,
            query=query_text,
            breed=case.breed,
            age=case.age,
            stage=case.stage,
            immunophenotype=case.immunophenotype,
            notes=case.notes,
        )

        result = await self._rag_pipeline.execute_query(context_query)

        now = datetime.now(timezone.utc)
        case_query = CaseQuery(
            id=uuid.uuid4(),
            query_text=query_text,
            case_id=case_id,
            response_synthesis=result.get("synthesis"),
            response_citations=result.get("sources"),
            evidence_level=None,
            evidence_score=result.get("evidence_score"),
            study_count=result.get("study_count"),
            total_sample_size=result.get("total_sample_size"),
            created_at=now,
        )
        await self._case_repository.add_query(case_id, case_query)

        return result
