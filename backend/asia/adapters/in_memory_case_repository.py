"""In-memory CaseRepository for MVP — no database needed for cases."""
from __future__ import annotations

import uuid

from asia.domain.models import Case, CaseQuery


class InMemoryCaseRepository:
    """Stores cases in memory. Data lost on restart — sufficient for MVP demo."""

    def __init__(self) -> None:
        self._cases: dict[uuid.UUID, Case] = {}
        self._queries: dict[uuid.UUID, list[CaseQuery]] = {}

    async def create(self, case: Case) -> Case:
        self._cases[case.id] = case
        self._queries[case.id] = []
        return case

    async def get(self, case_id: uuid.UUID) -> Case | None:
        return self._cases.get(case_id)

    async def add_query(self, case_id: uuid.UUID, query: CaseQuery) -> CaseQuery:
        if case_id not in self._queries:
            self._queries[case_id] = []
        self._queries[case_id].append(query)
        return query

    async def list_queries(self, case_id: uuid.UUID) -> list[CaseQuery]:
        return self._queries.get(case_id, [])
