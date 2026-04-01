# Pre-Loaded Queries -- Single Source of Truth (Resolves M1)

**Feature ID**: asia-vet-oncology
**Wave**: DESIGN
**Date**: 2026-04-01

---

## Purpose

These 5 queries serve as:
1. **Demo safety net**: Guaranteed high-quality first impression
2. **Acceptance criteria**: The 5 critical queries that validate the MVP
3. **Pre-loaded homepage cards**: Clickable entry points for first-time users
4. **Integration test suite**: Automated tests verify these produce valid responses

This document is the **single source of truth**. The backend configuration file (`config/pre_loaded_queries.py`) must reference these exact strings. The frontend renders whatever the API returns -- it does not hardcode query text.

---

## The 5 Critical Queries

| ID | Query Text (Italian) | Clinical Topic | Expected Response Must Include |
|----|---------------------|----------------|-------------------------------|
| Q1 | Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III? | First-line protocol selection | CHOP protocol, 80-90% remission rate, relevant citations (Garrett 2002, Simon 2006, Sorenmo 2020) |
| Q2 | CHOP-19 vs CHOP-25: differenze negli outcome? | Protocol comparison | Equivalence finding, Sorenmo 2020 multicenter RCT, comparison table, n=408 |
| Q3 | Protocolli di rescue per recidiva precoce dopo CHOP? | Rescue protocols | Multiple options (LOPP, LAP, DMAC, Tanovea/rabacfosadine), evidence for each |
| Q4 | Prognosi linfoma T-cell vs B-cell? | Prognostic factors | B-cell better prognosis, specific survival differences, immunophenotype as prognostic factor |
| Q5 | Aggiustamento dose doxorubicina per neutropenia? | Dose modification | Grade-specific guidance (Grade 1-4), delay vs dose reduction vs protocol switch |

---

## Backend Configuration Contract

The backend exposes these queries via `GET /api/pre-loaded-queries`. The response format:

```json
{
  "queries": [
    {
      "id": "Q1",
      "text": "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?",
      "topic": "Protocollo prima linea"
    },
    {
      "id": "Q2",
      "text": "CHOP-19 vs CHOP-25: differenze negli outcome?",
      "topic": "Confronto protocolli"
    },
    {
      "id": "Q3",
      "text": "Protocolli di rescue per recidiva precoce dopo CHOP?",
      "topic": "Protocolli di rescue"
    },
    {
      "id": "Q4",
      "text": "Prognosi linfoma T-cell vs B-cell?",
      "topic": "Prognosi per immunofenotipo"
    },
    {
      "id": "Q5",
      "text": "Aggiustamento dose doxorubicina per neutropenia?",
      "topic": "Gestione tossicita"
    }
  ]
}
```

---

## Version History

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 1.0 | 2026-04-01 | Initial 5 queries defined | DISCUSS wave output, confirmed in mvp.md and story-map.md |

---

## Validation Rules

1. Frontend must render query cards from the API response, never from hardcoded strings
2. When a vet clicks a card, the exact `text` string from the API is sent back as the query
3. The query text displayed on the response page must match the card text character-for-character
4. All 5 queries must be pre-tested before any demo to verify they produce accurate, well-cited responses
5. If any query consistently produces poor results, the query text may be refined (update this document first, then backend config)
