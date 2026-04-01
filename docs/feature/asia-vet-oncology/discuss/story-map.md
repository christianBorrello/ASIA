# Story Map: ASIA Vet Oncology MVP

## User: Dott.ssa Giulia Mancini (Italian vet, general practice, oncology cases)
## Goal: Get evidence-based treatment answers for canine lymphoma cases in Italian, with verifiable citations

---

## Backbone

| Discover ASIA | Ask a Question | Read the Answer | Verify Sources | Manage a Case | Understand a Paper |
|---------------|----------------|-----------------|----------------|---------------|-------------------|
| Open homepage | Type query | Read synthesis | Click DOI | Create case | Paste DOI |
| See pre-loaded queries | Click pre-loaded query | See evidence level | Read source details | Associate queries | Read clinical summary |
| Read disclaimer | Submit query | Expand source panel | Verify claims | View case history | See study positioning |
| | | See comparison table | | Re-query with context | |
| | | | | | |

---

## Walking Skeleton

The thinnest possible end-to-end slice: one query in, one answer out, one citation verified.

| Activity | Walking Skeleton Task |
|----------|----------------------|
| Discover ASIA | Homepage with search box and disclaimer |
| Ask a Question | Submit a single clinical query in Italian |
| Read the Answer | Receive streaming synthesis in Italian with at least 1 citation |
| Verify Sources | Click DOI link, opens real paper in new tab |
| Manage a Case | *(not in walking skeleton -- query works without a case)* |
| Understand a Paper | *(not in walking skeleton -- secondary feature)* |

**Walking skeleton delivers**: A vet types a question about canine lymphoma, gets an Italian synthesis with a verifiable citation. That is the core value proposition in its minimum form.

---

## Release Slices

### Walking Skeleton: "One Question, One Answer" (WS)

**Outcome**: A vet can ask a clinical question and receive a synthesized, cited answer in Italian.

| Activity | Task | Story Ref |
|----------|------|-----------|
| Discover ASIA | Homepage with search box + disclaimer | US-01 |
| Ask a Question | Submit free-text query, get streaming response | US-02 |
| Read the Answer | Italian synthesis with inline citations + evidence level + source panel | US-02 |
| Verify Sources | DOI links resolve to real papers | US-02 |

**Stories**: US-01 (Homepage), US-02 (Clinical Query with RAG)

---

### Release 1: "Demo Ready" (R1)

**Outcome**: The vet team demo succeeds -- 5 critical queries answered accurately, comparison table works, pre-loaded queries provide safe entry.

| Activity | Task | Story Ref |
|----------|------|-----------|
| Discover ASIA | 5 pre-loaded queries as clickable cards | US-03 |
| Ask a Question | Pre-loaded query click triggers response | US-03 |
| Read the Answer | Protocol comparison table for comparison queries | US-04 |
| Read the Answer | Error handling: no evidence, slow response, citation removed | US-05 |

**Stories**: US-03 (Pre-loaded Queries), US-04 (Protocol Comparison Table), US-05 (Graceful Error Handling)

---

### Release 2: "Clinical Workflow" (R2)

**Outcome**: The vet can manage ongoing cases and dive deeper into individual papers.

| Activity | Task | Story Ref |
|----------|------|-----------|
| Manage a Case | Create case with patient info | US-06 |
| Manage a Case | Associate queries with case, view history | US-06 |
| Manage a Case | Automatic context injection into RAG | US-06 |
| Understand a Paper | Paste DOI, get structured clinical summary | US-07 |

**Stories**: US-06 (Basic Case Mode), US-07 (Explain This Paper)

---

## Scope Assessment: PASS

- **Stories**: 7 user stories
- **Bounded contexts**: 2 (RAG pipeline, Frontend/UX)
- **Estimated effort**: ~10 days (walking skeleton ~3 days, R1 ~4 days, R2 ~3 days)
- **Integration points**: 3 (Frontend-Backend API, RAG pipeline-LLM, Ingestion-pgvector)

Right-sized for a single delivery cycle. No splitting needed.
