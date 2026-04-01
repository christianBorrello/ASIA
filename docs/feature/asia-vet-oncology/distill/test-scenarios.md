# Test Scenarios -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DISTILL
**Designer**: Quinn (Acceptance Test Designer)
**Date**: 2026-04-01

---

## Scenario Inventory

**Total scenarios**: 30
- Walking skeletons: 3
- Focused happy path: 13
- Error/edge case: 12 (40%)
- Property-shaped: 2

### Error path ratio: 12/30 = 40% (meets >= 40% target)

---

## Walking Skeleton Scenarios (3)

| # | Feature File | Scenario | Story |
|---|-------------|----------|-------|
| WS-1 | walking-skeleton.feature | Veterinarian asks a clinical question and receives a cited synthesis in Italian | US-01, US-02 |
| WS-2 | walking-skeleton.feature | Veterinarian verifies a citation from the synthesis | US-02 |
| WS-3 | walking-skeleton.feature | Veterinarian discovers ASIA and understands its purpose | US-01 |

---

## Milestone 1: Demo Ready (19 scenarios)

### US-03: Pre-loaded Queries (7 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M1-1 | Homepage displays five pre-loaded clinical queries as clickable cards | Happy path |
| M1-2 | Clicking a pre-loaded query submits it to the evidence pipeline | Happy path |
| M1-3 | First-line protocol query produces an accurate cited response (Q1) | Happy path |
| M1-4 | Protocol comparison query produces an accurate cited response (Q2) | Happy path |
| M1-5 | Rescue protocol query produces an accurate cited response (Q3) | Happy path |
| M1-6 | Prognosis query produces an accurate cited response (Q4) | Happy path |
| M1-7 | Dose adjustment query produces an accurate cited response (Q5) | Happy path |

### US-04: Protocol Comparison Table (2 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M1-8 | Comparison query generates a structured protocol table | Happy path |
| M1-9 | Non-comparison query does not generate a table | Edge case |

### US-05: Error Handling (6 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M1-10 | Out-of-scope query returns an honest no-evidence message | Error path |
| M1-11 | ASIA never fabricates an answer when evidence is missing | Error path |
| M1-12 | Slow response shows progress feedback | Error path |
| M1-13 | Self-reflective verification removes an unsupported citation | Error path |
| M1-14 | Error messages are in Italian and suggest next steps | Error path |
| M1-15 | Streaming connection lost preserves partial content | Error path |

### Property Scenarios (2)

| # | Scenario | Type |
|---|----------|------|
| M1-P1 | No response ever contains fabricated citations | Property |
| M1-P2 | Medical disclaimer is visible on every page | Property |

---

## Milestone 2: Clinical Workflow (11 scenarios)

### US-06: Case Mode (6 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M2-1 | Veterinarian creates a new case with full patient information | Happy path |
| M2-2 | Veterinarian creates a case with only required fields | Edge case |
| M2-3 | Query within a case automatically includes patient context | Happy path |
| M2-4 | Case history shows all queries in chronological order | Happy path |
| M2-5 | Case data persists across sessions | Happy path |
| M2-6 | Case creation fails when required fields are missing | Error path |

### US-07: Explain This Paper (3 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M2-7 | Veterinarian gets a structured summary of a paper in the corpus | Happy path |
| M2-8 | Paper not in the corpus produces an abstract-based summary | Edge case |
| M2-9 | Invalid DOI returns a helpful error message | Error path |

### Cross-feature Error Paths (2 scenarios)

| # | Scenario | Type |
|---|----------|------|
| M2-10 | Query within a case with minimal context still produces a response | Edge case |
| M2-11 | Empty DOI input shows a validation message | Error path |

---

## Traceability Matrix

| Story | Scenarios | Walking Skeleton | Error/Edge |
|-------|-----------|-----------------|------------|
| US-01 | WS-1, WS-3, M1-P2 | 2 | 0 |
| US-02 | WS-1, WS-2, M1-P1 | 2 | 0 |
| US-03 | M1-1 through M1-7 | 0 | 0 |
| US-04 | M1-8, M1-9 | 0 | 1 |
| US-05 | M1-10 through M1-15 | 0 | 6 |
| US-06 | M2-1 through M2-6, M2-10 | 0 | 3 |
| US-07 | M2-7 through M2-9, M2-11 | 0 | 3 |

All 7 stories have at least 1 scenario. Traceability Check A: PASS.

---

## Environment Coverage

| Environment | Walking Skeleton Coverage |
|-------------|--------------------------|
| local-dev | WS-1 Background: "the ASIA application is running" covers Docker Compose local environment |
| ci | Background: "the corpus contains papers about canine multicentric lymphoma" covers CI with seeded pgvector service container |

Traceability Check B: PASS (both environments addressed).

---

## Implementation Sequence (One-at-a-Time)

Enable scenarios in this order. Each must pass before enabling the next.

1. **WS-1**: Core query flow (proves driving port works end-to-end)
2. **WS-2**: Citation verification (proves source panel works)
3. **WS-3**: Homepage discovery (proves metadata endpoints work)
4. **M1-1**: Pre-loaded queries displayed
5. **M1-2**: Pre-loaded query submission
6. **M1-3**: Q1 accuracy (first-line protocol)
7. **M1-4**: Q2 accuracy (protocol comparison)
8. **M1-5**: Q3 accuracy (rescue protocols)
9. **M1-6**: Q4 accuracy (prognosis)
10. **M1-7**: Q5 accuracy (dose adjustment)
11. **M1-8**: Comparison table generation
12. **M1-9**: Non-comparison table absence
13. **M1-10**: No-evidence message
14. **M1-11**: No fabrication
15. **M1-12**: Progress feedback
16. **M1-13**: Citation removal
17. **M1-14**: Italian error messages
18. **M1-15**: Connection loss
19. **M2-1**: Full case creation
20. **M2-2**: Minimal case creation
21. **M2-3**: Case context injection
22. **M2-4**: Case history
23. **M2-5**: Case persistence
24. **M2-6**: Case validation
25. **M2-7**: Paper explanation (in corpus)
26. **M2-8**: Paper explanation (abstract only)
27. **M2-9**: Invalid DOI
28. **M2-10**: Minimal case query
29. **M2-11**: Empty DOI validation
30. **M1-P1, M1-P2**: Property scenarios (last, as they validate invariants)
