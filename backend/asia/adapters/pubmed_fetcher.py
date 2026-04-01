"""PubMed fetcher stub -- real API integration in a future step."""
from __future__ import annotations

from asia.domain.models import Paper


class PubMedFetcher:
    """Stub: PubMed paper fetcher (not yet implemented)."""

    async def fetch(self, query: str, max_results: int = 50) -> list[Paper]:
        raise NotImplementedError(
            "PubMed API integration not yet implemented -- use seed_papers.py for MVP"
        )
