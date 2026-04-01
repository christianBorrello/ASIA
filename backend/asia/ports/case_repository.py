from __future__ import annotations

import uuid
from typing import Protocol

from asia.domain.models import Case, CaseQuery


class CaseRepository(Protocol):
    async def create(self, case: Case) -> Case: ...

    async def get(self, case_id: uuid.UUID) -> Case | None: ...

    async def add_query(self, case_id: uuid.UUID, query: CaseQuery) -> CaseQuery: ...

    async def list_queries(self, case_id: uuid.UUID) -> list[CaseQuery]: ...
