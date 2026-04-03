"""SynthesisGenerator service -- builds prompts and calls LLM for synthesis."""
from __future__ import annotations

from asia.domain.models import Chunk, Paper
from asia.ports.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "Sei un assistente scientifico veterinario specializzato in oncologia. "
    "Rispondi SEMPRE in italiano. "
    "Fornisci una sintesi DETTAGLIATA e COMPLETA delle evidenze scientifiche. "
    "Usa marcatori di citazione [1], [2], ecc. per riferire a papers specifici. "
    "CITA IL MAGGIOR NUMERO POSSIBILE di paper forniti nel contesto — ogni affermazione "
    "deve essere supportata da almeno una citazione. Cerca di citare almeno 6-10 fonti diverse "
    "se disponibili. Non raggruppare le citazioni alla fine: distribuiscile inline nel testo. "
    "Non inventare mai citazioni o dati non presenti nei paper forniti. "
    "La risposta deve essere lunga e approfondita, non un breve riassunto."
)

COMPARISON_PROMPT_SUFFIX = (
    "\n\nQuesta e una domanda di confronto tra protocolli. "
    "Includi una tabella comparativa in formato JSON alla fine della risposta, "
    "racchiusa in un blocco ```json. La tabella deve avere questa struttura:\n"
    '{"comparison_table": {"headers": ["Protocollo", "Tasso remissione", '
    '"Sopravvivenza mediana", "Citazione"], "rows": [{"protocol": "...", '
    '"remission_rate": "...", "median_survival": "...", "citation": "[N]"}]}}'
)


def build_user_prompt(
    query_text: str,
    chunks: list[Chunk],
    papers: dict,
    is_comparison: bool = False,
) -> str:
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

    prompt = (
        f"Domanda clinica: {query_text}\n\n"
        f"Evidenze disponibili:\n\n{context_block}\n\n"
        "Sintetizza le evidenze in italiano con citazioni [N]."
    )

    if is_comparison:
        prompt += COMPARISON_PROMPT_SUFFIX

    return prompt


class SynthesisGenerator:
    """Generates clinical synthesis by combining retrieved evidence with LLM."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm = llm_provider

    async def generate(
        self,
        query_text: str,
        chunks: list[Chunk],
        papers: dict,
        is_comparison: bool = False,
    ) -> str:
        """Generate synthesis from query and retrieved chunks."""
        system = SYSTEM_PROMPT
        if is_comparison:
            system += (
                " Per domande di confronto, includi una tabella comparativa "
                "in formato JSON."
            )
        user_prompt = build_user_prompt(
            query_text, chunks, papers, is_comparison=is_comparison
        )
        return await self._llm.generate(user_prompt, system_prompt=system)
