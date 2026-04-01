"""
Acceptance test fixtures for ASIA Vet Oncology.

Test approach:
- Tests exercise API endpoints (driving ports) exclusively
- External services (Groq LLM, PubMed, Semantic Scholar) are mocked
- PostgreSQL + pgvector is real (via service container in CI, local in dev)
- All responses use pre-canned LLM fixtures for determinism
"""

import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Feature file discovery
# ---------------------------------------------------------------------------

FEATURE_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Session-scoped fixtures (expensive setup, created once)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def app():
    """
    Create the ASIA FastAPI application with test configuration.

    Uses real PostgreSQL but mocked external services:
    - LLM provider: returns pre-canned synthesis responses
    - Embedding provider: returns deterministic vectors
    - Paper fetcher: returns seeded paper data
    """
    # Implementation note for software-crafter:
    # 1. Import create_app from asia.main
    # 2. Override LLMProvider port with MockLLMProvider
    # 3. Override EmbeddingProvider port with MockEmbeddingProvider
    # 4. Override PaperFetcher port with MockPaperFetcher
    # 5. Use real PaperRepository (PostgreSQL + pgvector)
    # 6. Use real CaseRepository (PostgreSQL)
    raise NotImplementedError(
        "Wire FastAPI app with mocked external services. "
        "See asia.api.dependencies for port injection points."
    )


@pytest.fixture(scope="session")
def test_client(app):
    """
    HTTP test client for the ASIA API.

    All acceptance tests invoke through this client,
    exercising the API endpoints (driving ports).
    """
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def seeded_corpus(app):
    """
    Seed the test database with papers for the 5 critical queries.

    Papers include:
    - Garrett et al. (2002) - CHOP protocol outcomes
    - Simon et al. (2006) - CHOP protocol review
    - Sorenmo et al. (2020) - CHOP-19 vs CHOP-25 multicenter RCT, n=408
    - Vail et al. (2013) - Prognostic factors by immunophenotype
    - Additional papers for rescue protocols and dose adjustment

    Each paper has: title, authors, year, journal, DOI, abstract,
    study type, sample size, and pre-computed embedding vectors.
    """
    # Implementation note for software-crafter:
    # 1. Create Paper domain objects with realistic metadata
    # 2. Use deterministic embedding vectors (not real model)
    # 3. Insert via PaperRepository port
    # 4. Verify retrieval works for all 5 critical queries
    raise NotImplementedError(
        "Seed test database with papers for 5 critical queries. "
        "See design/pre-loaded-queries.md for expected papers."
    )


# ---------------------------------------------------------------------------
# Function-scoped fixtures (per-test isolation)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_cases(app):
    """
    Remove all cases and query logs between tests.
    Papers/corpus data is preserved (session-scoped).
    """
    yield
    # Implementation note for software-crafter:
    # Truncate cases and case_queries tables after each test
    # Do NOT truncate papers or chunks tables


# ---------------------------------------------------------------------------
# Mock providers for external services
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def mock_llm_responses():
    """
    Pre-canned LLM responses for the 5 critical queries.

    Each response includes:
    - Italian synthesis text with citation markers [1], [2], etc.
    - Citation-claim mappings for verification
    - Evidence level metadata
    - Comparison table data (for Q2 only)

    These fixtures ensure deterministic, reviewable test behavior
    without calling the real Groq API.
    """
    return {
        "Q1_first_line_protocol": {
            "synthesis": (
                "Il protocollo raccomandato e il CHOP, che produce remissione "
                "nell'80-90% dei casi [1][2]. La sopravvivenza mediana e di "
                "10-14 mesi per il linfoma B-cell [1][2][3]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Garrett",
                    "year": 2002,
                    "claim": "80-90% remission",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Simon",
                    "year": 2006,
                    "claim": "80-90% remission",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 3,
                    "author": "Vail",
                    "year": 2013,
                    "claim": "10-14 months survival",
                    "verification": "PARZIALE",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 3,
            "total_sample_size": 285,
        },
        "Q2_chop_comparison": {
            "synthesis": (
                "CHOP-19 e CHOP-25 hanno outcome equivalenti in termini di "
                "remissione e sopravvivenza [1]. Lo studio multicentrico "
                "randomizzato su 408 cani non ha trovato differenze "
                "significative [1]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Sorenmo",
                    "year": 2020,
                    "claim": "equivalent outcomes",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "ALTO",
            "study_count": 1,
            "total_sample_size": 408,
            "comparison_table": {
                "columns": [
                    "protocol",
                    "remission_rate",
                    "median_survival",
                    "sample_size",
                ],
                "rows": [
                    {
                        "protocol": "CHOP-19",
                        "remission_rate": "80-90%",
                        "median_survival": "10-12 mesi",
                        "sample_size": 204,
                        "citation_id": 1,
                    },
                    {
                        "protocol": "CHOP-25",
                        "remission_rate": "80-90%",
                        "median_survival": "10-12 mesi",
                        "sample_size": 204,
                        "citation_id": 1,
                    },
                ],
            },
        },
        "Q3_rescue_protocols": {
            "synthesis": (
                "Per la recidiva precoce dopo CHOP, le opzioni di rescue "
                "includono LOPP [1], LAP [2] e protocolli a base di "
                "rabacfosadina [3]. La scelta dipende dalla risposta "
                "iniziale e dalla tolleranza del paziente."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Griessmayr",
                    "year": 2007,
                    "claim": "LOPP rescue",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Saba",
                    "year": 2009,
                    "claim": "LAP rescue",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 3,
                    "author": "Thamm",
                    "year": 2017,
                    "claim": "rabacfosadine",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 3,
            "total_sample_size": 142,
        },
        "Q4_prognosis_immunophenotype": {
            "synthesis": (
                "Il linfoma B-cell ha una prognosi significativamente "
                "migliore rispetto al T-cell [1][2]. La sopravvivenza "
                "mediana per B-cell e di 10-14 mesi contro 5-8 mesi "
                "per T-cell [1][2]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Vail",
                    "year": 2013,
                    "claim": "B-cell better prognosis",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Aresu",
                    "year": 2015,
                    "claim": "survival differences",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "MODERATO",
            "study_count": 2,
            "total_sample_size": 310,
        },
        "Q5_dose_adjustment": {
            "synthesis": (
                "Per neutropenia di grado 1-2, si consiglia il ritardo di "
                "1 settimana senza riduzione della dose [1]. Per grado 3-4, "
                "riduzione del 20-25% della dose di doxorubicina e "
                "considerare lo switch a protocolli alternativi [1][2]."
            ),
            "citations": [
                {
                    "id": 1,
                    "author": "Chun",
                    "year": 2007,
                    "claim": "dose adjustment by grade",
                    "verification": "SUPPORTA",
                },
                {
                    "id": 2,
                    "author": "Rau",
                    "year": 2010,
                    "claim": "protocol switch for grade 3-4",
                    "verification": "SUPPORTA",
                },
            ],
            "evidence_level": "BASSO",
            "study_count": 2,
            "total_sample_size": 89,
        },
        "no_evidence": {
            "synthesis": None,
            "message": (
                "Non sono state trovate evidenze sufficienti nel corpus "
                "per rispondere a questa domanda."
            ),
            "scope_explanation": "Il corpus attuale copre il linfoma multicentrico canino.",
            "suggestions": [
                "Prova a riformulare la domanda",
                "Consulta le query pre-caricate",
                "Cerca direttamente su PubMed",
            ],
        },
        "citation_removed": {
            "synthesis": (
                "Il protocollo CHOP e il trattamento di riferimento [1][2]. "
                "La remissione e elevata [1]."
            ),
            "original_citation_count": 5,
            "final_citation_count": 4,
            "removed_citation_id": 4,
            "transparency_note": (
                "Una citazione inizialmente identificata e stata rimossa "
                "perche non supportava adeguatamente l'affermazione."
            ),
        },
    }
