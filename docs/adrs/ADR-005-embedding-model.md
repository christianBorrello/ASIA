# ADR-005: Embedding Model Selection

## Status

Accepted (pending benchmark validation)

## Context

ASIA needs to embed Italian clinical queries and match them against English paper abstracts via cosine similarity in pgvector. The embedding model must:

- Run locally on MacBook Air M1 8GB (no API cost)
- Produce meaningful cross-lingual similarity (Italian query -> English abstract)
- Be small enough to coexist with PostgreSQL, FastAPI, and Next.js in Docker
- Produce consistent-dimension vectors for pgvector indexing

## Decision

Use `all-MiniLM-L6-v2` as the primary embedding model (80MB, 384 dimensions). If cross-lingual quality is insufficient during benchmarking against the 5 critical queries, fall back to `paraphrase-multilingual-MiniLM-L12-v2` (420MB, 384 dimensions, explicitly trained for multilingual paraphrase detection).

Both models are from the sentence-transformers library and share the same 384-dimension output, so switching requires only changing the model name in configuration -- no schema changes.

## Alternatives Considered

### 1. PubMedBERT / BiomedBERT

Domain-specific biomedical model. **Rejected** because: (a) ~2GB model size, would consume most of the 8GB RAM budget, (b) trained on English biomedical text -- cross-lingual performance (Italian query) is unknown and likely poor, (c) the domain specificity advantage is offset by the language mismatch.

### 2. OpenAI text-embedding-3-small (API)

High-quality embeddings via API. **Rejected** because: (a) requires API cost (EUR 0 budget), (b) adds network dependency for every embedding operation (ingestion and query-time), (c) vendor lock-in for a core operation.

### 3. Cohere embed-multilingual-v3.0 (API)

Excellent multilingual embeddings. **Rejected** for the same reasons as OpenAI: cost and network dependency. However, this could be a future adapter if API budget becomes available.

### 4. e5-large-v2 or BGE-large

Larger open-source models (~1.3GB). **Rejected** because: (a) too large for 8GB RAM budget alongside other services, (b) 1024-dimension vectors increase pgvector storage and index size, (c) quality improvement over MiniLM is marginal for this corpus size.

## Consequences

### Positive

- 80MB model fits comfortably in RAM alongside all other services
- 384 dimensions keeps pgvector index small (~20MB for 5000 chunks)
- sentence-transformers library is well-maintained (Apache 2.0)
- Same dimension for both primary and fallback model -- zero schema impact on switch
- Local execution: no API cost, no network dependency for embedding

### Negative

- MiniLM cross-lingual quality is "good enough" but not optimal for Italian-English
- If both MiniLM models prove insufficient, would need to consider API-based embeddings (cost impact)
- 384 dimensions is lower than state-of-the-art (1024+) -- may miss subtle semantic distinctions in medical text
- Must benchmark early: run the 5 critical queries and verify retrieval quality before investing in the full pipeline
