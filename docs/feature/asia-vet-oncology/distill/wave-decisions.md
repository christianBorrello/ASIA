# Wave Decisions -- ASIA Vet Oncology DISTILL

**Feature ID**: asia-vet-oncology
**Wave**: DISTILL
**Designer**: Quinn (Acceptance Test Designer)
**Date**: 2026-04-01

---

## Decision Summary

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | **Feature scope**: Core application functionality | All 7 stories covered. Not infrastructure testing. |
| D2 | **Test framework**: pytest-bdd | Matches Python backend stack. BDD Given-When-Then structure. |
| D3 | **Integration approach**: Mocked externals only | Groq/PubMed/Semantic Scholar mocked with pre-canned fixtures. Real PostgreSQL + pgvector. |
| D4 | **Infrastructure testing**: No | Functional acceptance tests only. Local demo, not production. |
| D5 | **Driving ports**: API endpoints exclusively | POST /api/query, POST /api/explain-paper, POST /api/cases, GET /api/cases/{id}, POST /api/cases/{id}/query, GET /api/pre-loaded-queries, GET /api/corpus-metadata |
| D6 | **Walking skeletons**: 3 | Core query flow, citation verification, homepage discovery |
| D7 | **Scenario count**: 30 total | 3 walking skeletons + 13 happy path + 12 error/edge + 2 property |
| D8 | **Error path ratio**: 40% | 12 error/edge scenarios out of 30 total |
| D9 | **Skip strategy**: All scenarios except WS-1 tagged @skip | Enable one at a time as implemented |
| D10 | **Language**: Italian query text and expected responses in fixtures | Matches production usage |

---

## Mandate Compliance Evidence

### CM-A: Hexagonal Boundary Enforcement

All step definitions invoke through API endpoints (driving ports). No internal service imports.

**Driving port usage in step files**:
- `query_steps.py`: `test_client.post("/api/query", ...)`, `test_client.get("/api/pre-loaded-queries")`, `test_client.get("/api/corpus-metadata")`
- `case_steps.py`: `test_client.post("/api/cases", ...)`, `test_client.get("/api/cases/{id}")`, `test_client.post("/api/cases/{id}/query", ...)`
- `paper_steps.py`: `test_client.post("/api/explain-paper", ...)`

**Zero internal imports**: No step file imports from `asia.services`, `asia.domain`, `asia.adapters`, or `asia.ports` directly. All interactions go through `test_client` (FastAPI TestClient = HTTP driving port).

### CM-B: Business Language Purity

**Gherkin audit**: Zero technical terms in feature files. No HTTP verbs, status codes, JSON, database, API, REST, SSE, or framework references in scenario text.

**Business terms used**: veterinarian, clinical question, synthesis, citation, evidence level, pre-loaded query, corpus, case, patient, diagnosis, protocol, paper, DOI.

### CM-C: Walking Skeleton + Focused Scenario Counts

- Walking skeletons: 3 (user value E2E)
- Focused scenarios: 27 (boundary tests with mocked externals)
- Ratio: 3:27 (within 2-5 : 15-20+ recommended range)

### CM-D: Pure Function Extraction

Pure functions identified for extraction during DELIVER:
- `evidence_scoring.py`: compute_evidence_level(study_metadata) -> ALTO/MODERATO/BASSO
- `query_types.py`: is_comparison_query(query_text) -> bool
- `context_injection.py`: build_case_context(case_data) -> prompt_text

These are tested directly in unit tests. Fixture parametrization applies only to the database adapter layer (real PostgreSQL in CI, real PostgreSQL locally).

---

## Artifacts Produced

| Artifact | Path |
|----------|------|
| Walking skeleton feature | `tests/acceptance/asia-vet-oncology/walking-skeleton.feature` |
| Milestone 1 feature | `tests/acceptance/asia-vet-oncology/milestone-1-demo-ready.feature` |
| Milestone 2 feature | `tests/acceptance/asia-vet-oncology/milestone-2-clinical-workflow.feature` |
| Test fixtures | `tests/acceptance/asia-vet-oncology/conftest.py` |
| Query steps | `tests/acceptance/asia-vet-oncology/steps/query_steps.py` |
| Case steps | `tests/acceptance/asia-vet-oncology/steps/case_steps.py` |
| Paper steps | `tests/acceptance/asia-vet-oncology/steps/paper_steps.py` |
| Scenario inventory | `docs/feature/asia-vet-oncology/distill/test-scenarios.md` |
| Walking skeleton doc | `docs/feature/asia-vet-oncology/distill/walking-skeleton.md` |
| Wave decisions | `docs/feature/asia-vet-oncology/distill/wave-decisions.md` |

---

## Handoff Notes for Software Crafter (DELIVER Wave)

1. **Start with WS-1**: Enable the first walking skeleton. It must fail for a business logic reason, not a wiring error.
2. **Fixture wiring in conftest.py**: The `app`, `test_client`, and `seeded_corpus` fixtures have `NotImplementedError` stubs. Wire them to the real FastAPI app with mocked LLM/embedding providers.
3. **Pre-canned LLM responses**: `mock_llm_responses` fixture contains deterministic responses for all 5 critical queries. Use these to configure the MockLLMProvider.
4. **One scenario at a time**: Remove `@skip` from one scenario, implement until it passes, commit, repeat.
5. **Property scenarios**: Tagged `@property`. Implement as property-based tests with Hypothesis generators in the inner loop.
6. **SSE streaming scenarios**: M1-12 (progress) and M1-15 (connection loss) require SSE client testing. Consider httpx-sse or a custom SSE test helper.
7. **Frontend scenarios**: Several Then steps (disclaimer visibility, search box rendering) are marked as frontend concerns. Create separate frontend acceptance tests or verify via API metadata endpoints.
