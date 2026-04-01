# Walking Skeleton -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DISTILL

---

## What the Walking Skeleton Proves

The walking skeleton answers one question: **Can a veterinarian ask a clinical question about canine lymphoma and receive a cited, Italian-language synthesis?**

This is the core value proposition of ASIA in its minimum form. If this works, the demo has a foundation. If this fails, nothing else matters.

---

## Three Walking Skeleton Scenarios

### WS-1: Core Query Flow (US-01, US-02)

**User goal**: Ask a clinical question, get an answer with citations.

**What it exercises (end-to-end)**:
- API endpoint accepts an Italian clinical question (POST /api/query)
- Query embedding produces a vector
- pgvector retrieves relevant paper chunks
- LLM generates an Italian synthesis with citation markers
- Evidence level is computed and returned
- Medical disclaimer is available

**Observable outcome**: A synthesis in Italian with at least 1 citation marker and an evidence level indicator.

**Demo-able to stakeholder**: Yes. A vet can type a question and see a real answer.

### WS-2: Citation Verification (US-02)

**User goal**: Verify that cited papers are real and match the claims.

**What it exercises**:
- Source panel returns author, year, DOI for each citation
- Citation markers in synthesis map 1:1 to source panel entries

**Observable outcome**: Each citation has verifiable details. No phantom references.

**Demo-able to stakeholder**: Yes. A vet can check that [1] corresponds to a real paper.

### WS-3: Homepage Discovery (US-01)

**User goal**: Understand what ASIA offers on first visit.

**What it exercises**:
- Corpus metadata endpoint returns date
- Pre-loaded queries endpoint returns 5 queries
- Homepage elements are available (search, case mode, explain paper)

**Observable outcome**: A vet sees the search box, pre-loaded queries, and disclaimer.

**Demo-able to stakeholder**: Yes. A vet understands the tool on first glance.

---

## Walking Skeleton Litmus Test

| Criterion | WS-1 | WS-2 | WS-3 |
|-----------|-------|-------|-------|
| Title describes user goal? | Yes: "asks a clinical question and receives a cited synthesis" | Yes: "verifies a citation from the synthesis" | Yes: "discovers ASIA and understands its purpose" |
| Given/When describe user actions? | Yes: opens homepage, submits question | Yes: views source panel | Yes: opens homepage |
| Then describe user observations? | Yes: synthesis in Italian, citation markers, evidence level | Yes: author, year, link for each citation | Yes: search box, buttons, disclaimer, corpus date |
| Non-technical stakeholder confirms? | Yes: "that is what users need" | Yes: "that is what users need" | Yes: "that is what users need" |

All 3 walking skeletons pass the litmus test.

---

## Implementation Priority

WS-1 is the first scenario to implement. It must fail for a business logic reason (e.g., "no synthesis generated" or "no citations found"), not a technical reason (e.g., "connection refused" or "import error").

Once WS-1 passes, the software-crafter has proven that the core pipeline works. WS-2 and WS-3 follow immediately.
