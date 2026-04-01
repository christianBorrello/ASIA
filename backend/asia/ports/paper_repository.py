from __future__ import annotations

import uuid
from typing import Protocol

from asia.domain.models import Paper


class PaperRepository(Protocol):
    async def find_similar(
        self, embedding: list[float], top_k: int = 10
    ) -> list[Paper]: ...

    async def get_by_doi(self, doi: str) -> Paper | None: ...

    async def save(self, paper: Paper) -> None: ...

    async def get_by_id(self, paper_id: uuid.UUID) -> Paper | None: ...
