"""PaperExplainer service -- structured clinical summary of a paper by DOI."""
from __future__ import annotations


class PaperExplainer:
    """Application service for explaining papers from the corpus.

    Driving port: explain(doi) -> structured summary dict
    Driven ports: PaperRepository (get_by_doi), LLMProvider (generate)
    """

    SYSTEM_PROMPT = (
        "Sei un assistente per veterinari oncologi. "
        "Analizza il seguente paper e fornisci un riassunto clinico "
        "strutturato in italiano con queste sezioni:\n"
        "- Obiettivo\n"
        "- Metodologia\n"
        "- Risultati chiave\n"
        "- Implicazioni pratiche\n"
        "- Contesto nel corpus"
    )

    def __init__(self, paper_repository, llm_provider) -> None:
        self._repo = paper_repository
        self._llm = llm_provider

    async def explain(self, doi: str) -> dict:
        """Explain a paper identified by DOI."""
        if not doi or not doi.strip():
            return {
                "error": True,
                "message": (
                    "Inserisci un DOI o un titolo del paper. "
                    "Il campo DOI non puo essere vuoto."
                ),
            }

        paper = await self._repo.get_by_doi(doi)

        if paper is None:
            return {
                "error": True,
                "message": (
                    "Paper non trovato nel corpus. "
                    "Verifica il DOI o prova con il titolo del paper."
                ),
            }

        prompt = self._build_prompt(paper)
        explanation = await self._llm.generate(prompt, system_prompt=self.SYSTEM_PROMPT)

        return {
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "doi": paper.doi,
            "summary": explanation,
        }

    @staticmethod
    def _build_prompt(paper) -> str:
        """Build explanation prompt from paper metadata and content."""
        parts = [
            f"Titolo: {paper.title}",
            f"Autori: {', '.join(a.get('name', '') for a in paper.authors)}",
            f"Anno: {paper.year}",
        ]
        if paper.journal:
            parts.append(f"Rivista: {paper.journal}")
        if paper.abstract_text:
            parts.append(f"Abstract: {paper.abstract_text}")
        if paper.study_type:
            parts.append(f"Tipo di studio: {paper.study_type}")
        if paper.sample_size:
            parts.append(f"Dimensione campione: {paper.sample_size}")
        return "\n".join(parts)
