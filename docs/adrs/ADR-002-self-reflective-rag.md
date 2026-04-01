# ADR-002: Self-Reflective RAG Approach

## Status

Accepted

## Context

ASIA's kill criterion is zero hallucinated citations. A standard RAG pipeline (retrieve -> synthesize) has no verification step -- the LLM may generate plausible-sounding claims with citation markers that do not actually match the retrieved papers. In veterinary oncology, a wrong dosage or fabricated paper reference could lead to clinical harm.

The system needs a mechanism to verify that every citation in the synthesis genuinely supports its associated claim before presenting it to the vet.

## Decision

Implement a two-phase self-reflective RAG pipeline:

**Phase 1 (Generate)**: Standard RAG -- embed query, retrieve top-k chunks, synthesize Italian response with citation markers and a structured citation-claim mapping.

**Phase 2 (Verify)**: Send each (claim, cited chunk) pair to the LLM for verification. The LLM classifies each pair as SUPPORTA, PARZIALE, or NON_SUPPORTA. Citations classified as NON_SUPPORTA are removed, PARZIALE claims are softened, and the synthesis is regenerated if changes occurred.

**Constraints**: Maximum 3 LLM calls total (1 synthesis + 1 batch verification + 1 optional regeneration). Total timeout: 25 seconds. Verification is batched (all pairs in one call) to minimize latency.

## Alternatives Considered

### 1. No verification (standard RAG)

Generate synthesis from retrieved chunks without any verification pass. **Rejected** because: (a) citation hallucination is the project's kill criterion, (b) LLMs are known to fabricate plausible citations, (c) the cost of a wrong citation in a clinical context is too high.

### 2. Retrieval-only verification (no LLM)

Verify citations by checking if the cited chunk appears in the retrieval results (string matching or embedding similarity). **Rejected** because: (a) a chunk can be retrieved but not actually support the specific claim made, (b) the LLM may synthesize a correct retrieval into an incorrect claim, (c) semantic verification requires language understanding, not just retrieval matching.

### 3. Multi-agent verification (separate verifier model)

Use a different LLM or model specifically for verification (e.g., a smaller, faster model for fact-checking). **Rejected** for MVP because: (a) adds a second model to load or a second API to manage, (b) 8GB RAM constraint, (c) the same LLM can verify its own output with a different prompt at acceptable quality for MVP. This approach can be revisited post-MVP if verification quality is insufficient.

### 4. Human-in-the-loop verification

Require the vet to manually verify each citation before the response is marked as "verified." **Rejected** because: (a) defeats the purpose of the tool (saving time), (b) appropriate for post-MVP quality improvement but not for the synthesis workflow.

## Consequences

### Positive

- Reduces citation hallucination risk significantly
- Transparency note builds trust when citations are removed
- The verification prompt can be improved iteratively without changing architecture
- Soft verification (PARZIALE) preserves useful but imprecise citations with appropriate language

### Negative

- Adds 1-2 additional LLM calls per query (latency impact: ~5-10 seconds)
- Verification quality depends on the LLM's ability to assess its own output
- The 25-second timeout means complex queries with many citations may skip verification under time pressure
- LLM self-verification is not 100% reliable -- some hallucinations may pass verification
