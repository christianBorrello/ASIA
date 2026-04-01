"""SynthesisGenerator service -- builds prompts and calls LLM for synthesis."""
from __future__ import annotations

from asia.domain.models import Chunk, Paper
from asia.ports.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "Sei un assistente scientifico veterinario specializzato in oncologia. "
    "Rispondi SEMPRE in italiano. "
    "Sintetizza le evidenze scientifiche fornite. "
    "Usa marcatori di citazione [1], [2], ecc. per riferire a papers specifici. "
    "Non inventare mai citazioni o dati non presenti nei paper forniti. "
    "Cita solo i paper forniti nel contesto."
)


def build_user_prompt(query_text: str, chunks: list[Chunk], papers: dict) -> str:
    """Build user prompt with query, chunk texts, and paper metadata."""
    context_parts: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        paper = papers.get(chunk.paper_id)
        if paper:
            header = f"[{i}] {paper.title} ({paper.year})"
            if paper.journal:
                header += f", {paper.journal}"
        else:
            header = f"[{i}] Fonte sconosciuta"
        context_parts.append(f"{header}\n{chunk.chunk_text}")

    context_block = "\n\n".join(context_parts)

    return (
        f"Domanda clinica: {query_text}\n\n"
        f"Evidenze disponibili:\n\n{context_block}\n\n"
        "Sintetizza le evidenze in italiano con citazioni [N]."
    )


class SynthesisGenerator:
    """Generates clinical synthesis by combining retrieved evidence with LLM."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm = llm_provider

    async def generate(
        self,
        query_text: str,
        chunks: list[Chunk],
        papers: dict,
    ) -> str:
        """Generate synthesis from query and retrieved chunks."""
        user_prompt = build_user_prompt(query_text, chunks, papers)
        return await self._llm.generate(user_prompt, system_prompt=SYSTEM_PROMPT)
