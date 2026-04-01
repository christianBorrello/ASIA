"""Pre-loaded clinical queries for the ASIA homepage.

Single source of truth for the 5 critical queries displayed as clickable cards.
See docs/feature/asia-vet-oncology/design/pre-loaded-queries.md for rationale.
"""

PRE_LOADED_QUERIES = [
    {
        "id": "Q1",
        "text": "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?",
        "topic": "Protocollo prima linea",
    },
    {
        "id": "Q2",
        "text": "CHOP-19 vs CHOP-25: differenze negli outcome?",
        "topic": "Confronto protocolli",
    },
    {
        "id": "Q3",
        "text": "Protocolli di rescue per recidiva precoce dopo CHOP?",
        "topic": "Protocolli di rescue",
    },
    {
        "id": "Q4",
        "text": "Prognosi linfoma T-cell vs B-cell?",
        "topic": "Prognosi per immunofenotipo",
    },
    {
        "id": "Q5",
        "text": "Aggiustamento dose doxorubicina per neutropenia?",
        "topic": "Gestione tossicita",
    },
]
