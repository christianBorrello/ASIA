# Prioritization: ASIA Vet Oncology MVP

---

## Release Priority

| Priority | Release | Target Outcome | KPI | Rationale |
|----------|---------|---------------|-----|-----------|
| 1 | Walking Skeleton (WS) | End-to-end flow works: one query, one cited answer | Response accuracy verified by vet | Validates core assumption: RAG can produce accurate Italian synthesis |
| 2 | Demo Ready (R1) | 5 critical queries pass, comparison table, safe entry | 4/5 queries rated "accurate" by vet team | De-risks the demo: pre-loaded queries guarantee quality, comparison table is highest-value tangible output |
| 3 | Clinical Workflow (R2) | Vet can manage cases and explore papers | At least 1 vet creates a case for a real patient | Validates stickiness: will vets return beyond the first try? |

---

## Priority Scoring

| Story | Release | Value (1-5) | Urgency (1-5) | Effort (1-5) | Score | Priority |
|-------|---------|-------------|----------------|--------------|-------|----------|
| US-01: Homepage & Disclaimer | WS | 3 | 5 | 1 | 20.0 | P1 |
| US-02: Clinical Query (RAG) | WS | 5 | 5 | 4 | 12.5 | P1 |
| US-03: Pre-loaded Queries | R1 | 4 | 5 | 1 | 40.0 | P2 |
| US-04: Protocol Comparison Table | R1 | 5 | 4 | 3 | 13.3 | P2 |
| US-05: Graceful Error Handling | R1 | 3 | 4 | 2 | 10.0 | P2 |
| US-06: Basic Case Mode | R2 | 4 | 3 | 3 | 8.0 | P3 |
| US-07: Explain This Paper | R2 | 4 | 3 | 3 | 8.0 | P3 |

**Formula**: (Value x Urgency) / Effort

**Tie-breaking rule**: Walking Skeleton > Riskiest Assumption > Highest Value

---

## Riskiest Assumption Order

| Priority | Assumption | Validated By |
|----------|-----------|--------------|
| 1st | RAG can produce accurate Italian synthesis with correct citations (A4, feasibility) | US-02 (Walking Skeleton) |
| 2nd | Vets find ASIA answers accurate and clinically useful (A1, value) | US-03 + demo with 5 critical queries (R1) |
| 3rd | Vets will adopt and return (A2, adoption) | US-06 (Case Mode, R2) |

---

## MoSCoW Classification

| Category | Stories | Rationale |
|----------|---------|-----------|
| **Must Have** | US-01 (Homepage), US-02 (Clinical Query RAG), US-03 (Pre-loaded Queries), US-04 (Protocol Comparison), US-05 (Error Handling) | Without these, the demo has no value. These are the MVP. |
| **Should Have** | US-06 (Case Mode), US-07 (Explain This Paper) | Significant value for showing clinical workflow. Workaround: vet manually re-types context in each query. |
| **Could Have** | *(none in current scope)* | |
| **Won't Have** | Complication Advisor, Owner Communication, Auth, Multi-tumor, Offline mode | Explicitly deferred (see mvp.md excluded features) |

---

## Dependencies

```
US-01 (Homepage)
  |
  +---> US-02 (Clinical Query RAG) -- depends on US-01 for entry point
  |       |
  |       +---> US-03 (Pre-loaded Queries) -- depends on US-02 for query execution
  |       |
  |       +---> US-04 (Protocol Comparison) -- depends on US-02 for RAG response format
  |       |
  |       +---> US-05 (Error Handling) -- depends on US-02 for error states
  |       |
  |       +---> US-07 (Explain This Paper) -- depends on US-02 for paper retrieval
  |
  +---> US-06 (Case Mode) -- depends on US-01 for navigation + US-02 for query execution
```

---

## Build Sequence

1. **Week 1 (WS)**: US-01 + US-02 -- Homepage exists, one query works end-to-end with citations
2. **Week 2 (R1)**: US-03 + US-04 + US-05 -- Pre-loaded queries, comparison table, error handling
3. **Week 3 (R2)**: US-06 + US-07 -- Case mode, Explain This Paper
4. **Demo**: Present to Asia's vet team with all 3 releases
