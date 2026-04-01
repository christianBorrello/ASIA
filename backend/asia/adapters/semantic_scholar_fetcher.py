"""Semantic Scholar fetcher stub -- real API integration in a future step."""
from __future__ import annotations

from asia.domain.models import Paper


class SemanticScholarFetcher:
    """Stub: Semantic Scholar paper fetcher (not yet implemented)."""

    async def fetch(self, query: str, max_results: int = 50) -> list[Paper]:
        raise NotImplementedError(
            "Semantic Scholar API integration not yet implemented -- use seed_papers.py for MVP"
        )
