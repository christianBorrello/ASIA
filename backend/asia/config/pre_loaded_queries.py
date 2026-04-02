"""Pre-loaded clinical queries for the ASIA homepage.

Single source of truth for the clinical queries displayed as clickable cards.
Covers both lymphoma and carcinoma corpora.
See docs/feature/asia-vet-oncology/design/pre-loaded-queries.md for rationale.
"""

PRE_LOADED_QUERIES = [
    # --- Lymphoma queries ---
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
    # --- Carcinoma queries ---
    {
        "id": "Q6",
        "text": "Massa mediastinica nel cane: diagnosi differenziale tra timoma, carcinoma timico e linfoma",
        "topic": "Diagnosi differenziale mediastino",
    },
    {
        "id": "Q7",
        "text": "Ipercalcemia paraneoplastica nel cane: cause e approccio diagnostico",
        "topic": "Ipercalcemia paraneoplastica",
    },
    {
        "id": "Q8",
        "text": "Trattamento del timoma canino: chirurgia vs chemioterapia vs radioterapia",
        "topic": "Trattamento timoma",
    },
]
