"""Case management service -- driving port for case operations."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from asia.domain.models import Case
from asia.ports.case_repository import CaseRepository


class CaseService:
    """Application service for case management."""

    def __init__(self, case_repository: CaseRepository) -> None:
        self._case_repository = case_repository

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
        raise NotImplementedError("Case creation not yet implemented")

    async def get_case(self, case_id: uuid.UUID) -> Case | None:
        raise NotImplementedError("Case retrieval not yet implemented")
