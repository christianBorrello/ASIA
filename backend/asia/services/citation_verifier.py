"""CitationVerifier service -- self-reflective verification of citation claims."""
from __future__ import annotations

import re

from asia.ports.llm_provider import LLMProvider

VERIFICATION_PROMPT = (
    "Sei un revisore scientifico. Per ogni citazione nella sintesi seguente, "
    "verifica se il paper citato supporta effettivamente l'affermazione.\n\n"
    "Sintesi:\n{synthesis}\n\n"
    "Contesto dei paper citati:\n{context}\n\n"
    "Per ogni citazione [N], classifica come:\n"
    "- SUPPORTA: il paper supporta il claim\n"
    "- PARZIALE: supporto parziale\n"
    "- NON_SUPPORTA: non supporta il claim\n\n"
    "Rispondi nel formato:\n"
    "[N]: SUPPORTA/PARZIALE/NON_SUPPORTA - breve spiegazione"
)


class CitationVerifier:
    """Verifies citations via LLM self-reflection and removes unsupported ones."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm = llm_provider

    async def verify(
        self,
        synthesis: str,
        chunks: list,
        papers: dict,
    ) -> dict:
        """Verify citations and return cleaned synthesis with metadata.

        Returns dict with keys:
            synthesis: cleaned synthesis with unsupported citations removed
            reflection_note: transparency note if citations were removed (or None)
            removed_count: number of citations removed
        """
        context_parts = self._build_context(chunks, papers)
        prompt = VERIFICATION_PROMPT.format(
            synthesis=synthesis,
            context="\n".join(context_parts),
        )

        verification_response = await self._llm.generate(prompt)
        classifications = self._parse_classifications(verification_response)

        non_supporta_ids = {
            cid for cid, classification in classifications.items()
            if classification == "NON_SUPPORTA"
        }

        if not non_supporta_ids:
            return {
                "synthesis": synthesis,
                "reflection_note": None,
                "removed_count": 0,
            }

        cleaned_synthesis = self._remove_citations(synthesis, non_supporta_ids)
        renumbered_synthesis = self._renumber_citations(cleaned_synthesis, non_supporta_ids)

        reflection_note = (
            f"{len(non_supporta_ids)} citazione/i inizialmente identificata/e "
            "e stata/e rimossa/e perche non supportava/no adeguatamente "
            "l'affermazione associata."
        )

        return {
            "synthesis": renumbered_synthesis,
            "reflection_note": reflection_note,
            "removed_count": len(non_supporta_ids),
        }

    @staticmethod
    def _build_context(chunks: list, papers: dict) -> list[str]:
        """Build context strings for each cited chunk."""
        parts: list[str] = []
        for i, chunk in enumerate(chunks, start=1):
            paper = papers.get(chunk.paper_id)
            if paper:
                parts.append(f"[{i}] {paper.title} ({paper.year}): {chunk.chunk_text[:200]}")
        return parts

    @staticmethod
    def _parse_classifications(response: str) -> dict[int, str]:
        """Parse LLM verification response into citation -> classification map."""
        classifications: dict[int, str] = {}
        for line in response.strip().split("\n"):
            match = re.match(r"\[(\d+)\]:\s*(SUPPORTA|PARZIALE|NON_SUPPORTA)", line.strip())
            if match:
                citation_id = int(match.group(1))
                classification = match.group(2)
                classifications[citation_id] = classification
        return classifications

    @staticmethod
    def _remove_citations(synthesis: str, remove_ids: set[int]) -> str:
        """Remove sentences containing only unsupported citation markers."""
        sentences = re.split(r'(?<=[.!?])\s+', synthesis)
        kept_sentences: list[str] = []
        for sentence in sentences:
            markers_in_sentence = {int(m) for m in re.findall(r'\[(\d+)\]', sentence)}
            if markers_in_sentence and markers_in_sentence.issubset(remove_ids):
                continue
            cleaned = sentence
            for rid in remove_ids:
                cleaned = re.sub(rf'\[{rid}\]', '', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            if cleaned:
                kept_sentences.append(cleaned)
        return " ".join(kept_sentences)

    @staticmethod
    def _renumber_citations(synthesis: str, removed_ids: set[int]) -> str:
        """Renumber remaining citation markers to be sequential."""
        existing = sorted(set(int(m) for m in re.findall(r'\[(\d+)\]', synthesis)))
        if not existing:
            return synthesis
        renumber_map = {}
        new_id = 1
        for old_id in existing:
            renumber_map[old_id] = new_id
            new_id += 1

        def replace_marker(match: re.Match) -> str:
            old = int(match.group(1))
            return f"[{renumber_map.get(old, old)}]"

        return re.sub(r'\[(\d+)\]', replace_marker, synthesis)
