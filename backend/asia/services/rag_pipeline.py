"""RAG pipeline service -- orchestrates embed, retrieve, synthesize, score."""
from __future__ import annotations

import json
import re
import uuid

from asia.domain.evidence_scoring import compute_evidence_level
from asia.domain.models import Chunk, Paper
from asia.domain.query_types import is_comparison_query
from asia.ports.embedding_provider import EmbeddingProvider
from asia.ports.llm_provider import LLMProvider
from asia.services.synthesis_generator import SynthesisGenerator


class RAGPipeline:
    """Orchestrates the full RAG query flow.

    1. Embed query text
    2. Retrieve similar chunks via pgvector
    3. Resolve chunk -> paper mappings
    4. Generate synthesis with citations via LLM
    5. Compute evidence level from cited papers
    6. Extract comparison table if comparison query
    7. Return structured response
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        embedding_provider: EmbeddingProvider,
        paper_repository,
        top_k: int = 10,
    ) -> None:
        self._embedder = embedding_provider
        self._repo = paper_repository
        self._synthesis = SynthesisGenerator(llm_provider)
        self._top_k = top_k

    async def execute_query(self, query_text: str) -> dict:
        """Execute the full RAG pipeline and return structured result."""
        embedding = self._embedder.embed_text(query_text)

        chunks: list[Chunk] = await self._repo.find_similar(embedding, self._top_k)

        papers = await self._resolve_papers(chunks)

        comparison = is_comparison_query(query_text)

        synthesis = await self._synthesis.generate(
            query_text, chunks, papers, is_comparison=comparison
        )

        comparison_table = None
        if comparison:
            comparison_table, synthesis = self._extract_comparison_table(synthesis)

        cited_papers = self._extract_cited_papers(synthesis, chunks, papers)

        evidence_level, evidence_score = compute_evidence_level(cited_papers)

        sources = self._build_sources(synthesis, chunks, papers)

        result = {
            "synthesis": synthesis,
            "evidence_level": evidence_level.value,
            "evidence_score": evidence_score,
            "sources": sources,
            "study_count": len(cited_papers),
            "total_sample_size": sum(p.sample_size or 0 for p in cited_papers),
        }

        if comparison_table is not None:
            result["comparison_table"] = comparison_table

        return result

    @staticmethod
    def _extract_comparison_table(synthesis: str) -> tuple[dict | None, str]:
        """Extract JSON comparison table from LLM response.

        Returns (table_dict, cleaned_synthesis) where cleaned_synthesis
        has the JSON block removed.
        """
        pattern = r"```json\s*(\{.*?\"comparison_table\".*?\})\s*```"
        match = re.search(pattern, synthesis, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                table = parsed.get("comparison_table")
                cleaned = synthesis[: match.start()].rstrip()
                return table, cleaned
            except (json.JSONDecodeError, KeyError):
                pass
        return None, synthesis

    async def _resolve_papers(
        self, chunks: list[Chunk]
    ) -> dict[uuid.UUID, Paper]:
        """Resolve paper_id -> Paper for all chunks."""
        papers: dict[uuid.UUID, Paper] = {}
        seen: set[uuid.UUID] = set()
        for chunk in chunks:
            if chunk.paper_id not in seen:
                seen.add(chunk.paper_id)
                paper = await self._repo.get_by_id(chunk.paper_id)
                if paper:
                    papers[paper.id] = paper
        return papers

    def _extract_cited_papers(
        self,
        synthesis: str,
        chunks: list[Chunk],
        papers: dict[uuid.UUID, Paper],
    ) -> list[Paper]:
        """Extract papers referenced by citation markers [N] in synthesis."""
        markers = set(re.findall(r"\[(\d+)\]", synthesis))
        cited: list[Paper] = []
        seen_ids: set[uuid.UUID] = set()
        for marker in sorted(markers, key=int):
            index = int(marker) - 1
            if 0 <= index < len(chunks):
                paper_id = chunks[index].paper_id
                if paper_id not in seen_ids:
                    paper = papers.get(paper_id)
                    if paper:
                        cited.append(paper)
                        seen_ids.add(paper_id)
        return cited

    def _build_sources(
        self,
        synthesis: str,
        chunks: list[Chunk],
        papers: dict[uuid.UUID, Paper],
    ) -> list[dict]:
        """Build source citation objects only for papers cited in synthesis."""
        cited_markers = set(re.findall(r"\[(\d+)\]", synthesis))
        sources: list[dict] = []
        seen: set[uuid.UUID] = set()
        for i, chunk in enumerate(chunks, start=1):
            if str(i) not in cited_markers:
                continue
            if chunk.paper_id in seen:
                continue
            seen.add(chunk.paper_id)
            paper = papers.get(chunk.paper_id)
            if paper:
                author_str = paper.authors[0].get("name", "") if paper.authors else ""
                sources.append({
                    "id": i,
                    "author": author_str,
                    "year": paper.year,
                    "journal": paper.journal or "",
                    "doi": paper.doi,
                    "title": paper.title,
                })
        return sources
