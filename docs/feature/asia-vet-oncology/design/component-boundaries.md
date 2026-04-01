# Component Boundaries -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DESIGN
**Date**: 2026-04-01

---

## Architectural Style

**Modular monolith with ports-and-adapters** (hexagonal architecture).

A single FastAPI process contains all backend logic. Modules communicate through well-defined interfaces (ports). External dependencies (LLM, database, external APIs) are accessed through adapter implementations behind port interfaces.

**Why**: Team of 1, timeline of 10 days, zero operational complexity budget. A modular monolith provides clean boundaries for testing and future evolution without the overhead of distributed systems.

---

## Backend Module Structure

```
backend/
  asia/
    __init__.py
    main.py                          # FastAPI app entry point

    domain/                          # Pure domain logic (no framework imports)
      models.py                      # Domain dataclasses: Paper, Chunk, Case, Query, Citation, EvidenceLevel
      evidence_scoring.py            # ALTO/MODERATO/BASSO scoring (pure function)
      query_types.py                 # Query classification (comparison vs standard)
      context_injection.py           # Case context template builder (pure function)

    ports/                           # Abstract interfaces (Python Protocols/ABCs)
      llm_provider.py                # LLMProvider: generate(), stream()
      embedding_provider.py          # EmbeddingProvider: embed_text(), embed_batch()
      paper_repository.py            # PaperRepository: find_similar(), get_by_doi(), save()
      case_repository.py             # CaseRepository: create(), get(), list_queries()
      query_log_repository.py        # QueryLogRepository: save(), get_history()
      paper_fetcher.py               # PaperFetcher: fetch_from_pubmed(), fetch_from_semantic_scholar()

    services/                        # Application services (orchestration, uses ports)
      rag_pipeline.py                # Orchestrates: embed -> retrieve -> synthesize -> verify
      citation_verifier.py           # Self-reflective verification logic
      synthesis_generator.py         # Prompt construction + LLM call for synthesis
      paper_explainer.py             # Explain This Paper service
      case_service.py                # Case CRUD + context injection
      ingestion_service.py           # Paper ingestion orchestration

    adapters/                        # Port implementations (framework-specific)
      groq_provider.py               # GroqProvider implements LLMProvider
      sentence_transformer_embedder.py  # Implements EmbeddingProvider
      pg_paper_repository.py         # PostgreSQL implements PaperRepository
      pg_case_repository.py          # PostgreSQL implements CaseRepository
      pg_query_log_repository.py     # PostgreSQL implements QueryLogRepository
      pubmed_fetcher.py              # PubMed E-utilities implements PaperFetcher
      semantic_scholar_fetcher.py    # Semantic Scholar API implements PaperFetcher

    api/                             # FastAPI routes (driving adapters / primary ports)
      routes/
        query.py                     # POST /api/query -> SSE
        cases.py                     # CRUD for cases
        explain_paper.py             # POST /api/explain-paper -> SSE
        metadata.py                  # GET /api/corpus-metadata, GET /api/pre-loaded-queries
      middleware/
        error_handler.py             # Italian error messages, no stack traces
      dependencies.py                # FastAPI dependency injection (wires ports to adapters)

    config/
      settings.py                    # Pydantic Settings: env vars, LLM config, thresholds
      pre_loaded_queries.py          # Single source of truth for 5 queries (see M1)

  tests/
    unit/                            # Tests with mocked ports
    integration/                     # Tests with real PostgreSQL
    critical_queries/                # The 5 critical query acceptance tests
```

---

## Dependency Rules

```
                     +------------------+
                     |    api/routes    |  <-- Driving adapters (inbound)
                     +--------+---------+
                              |
                              v
                     +------------------+
                     |    services/     |  <-- Application logic (orchestration)
                     +--------+---------+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
            +-------+------+    +------+-------+
            |   domain/    |    |   ports/     |  <-- Pure domain + interfaces
            +--------------+    +------+-------+
                                       ^
                                       |
                              +--------+---------+
                              |    adapters/     |  <-- Driven adapters (outbound)
                              +------------------+
```

### Dependency Inversion Rules

1. `domain/` imports NOTHING from `ports/`, `services/`, `adapters/`, `api/`
2. `ports/` imports only from `domain/` (for type definitions)
3. `services/` imports from `domain/` and `ports/` only (never from `adapters/`)
4. `adapters/` imports from `ports/` and `domain/` (implements port interfaces)
5. `api/` imports from `services/` and `domain/` (calls services, uses domain types)
6. `api/dependencies.py` wires adapters to ports (composition root)

### Enforcement

```ini
# .importlinter configuration
[importlinter:contract:domain-purity]
name = Domain must not import from any other module
type = forbidden
source_modules = asia.domain
forbidden_modules = asia.ports, asia.services, asia.adapters, asia.api

[importlinter:contract:services-no-adapters]
name = Services must not import from adapters
type = forbidden
source_modules = asia.services
forbidden_modules = asia.adapters, asia.api

[importlinter:contract:ports-no-adapters]
name = Ports must not import from adapters
type = forbidden
source_modules = asia.ports
forbidden_modules = asia.adapters, asia.api, asia.services
```

---

## Frontend Module Structure

```
frontend/
  src/
    app/                             # Next.js App Router pages
      page.tsx                       # Homepage (search box, pre-loaded queries, CTAs)
      query/[id]/page.tsx            # Response page (synthesis, sources, evidence level)
      cases/page.tsx                 # Case list
      cases/new/page.tsx             # Case creation form
      cases/[id]/page.tsx            # Case detail + query history
      explain/page.tsx               # Explain This Paper
      layout.tsx                     # Root layout (disclaimer footer, nav)

    components/
      shared/
        Disclaimer.tsx               # Persistent disclaimer (single source)
        CorpusDate.tsx               # Corpus date from API
        SearchBox.tsx                 # Clinical query input
      home/
        PreLoadedQueryCard.tsx        # Clickable query card
      query/
        SynthesisStream.tsx           # SSE streaming text renderer
        SourcePanel.tsx               # Expandable citation list
        EvidenceLevel.tsx             # ALTO/MODERATO/BASSO badge
        ComparisonTable.tsx           # Protocol comparison table
        TransparencyNote.tsx          # Citation removal note
        ProgressIndicator.tsx         # Slow response progress
        ErrorMessage.tsx              # No evidence / connection lost
      cases/
        CaseForm.tsx                  # Case creation/edit form
        CaseHeader.tsx                # Case summary header
        QueryHistory.tsx              # Chronological query list

    lib/
      api.ts                         # API client (fetch + SSE helpers)
      types.ts                       # TypeScript interfaces matching API schemas
      constants.ts                   # Disclaimer text, evidence level labels

    hooks/
      useSSEStream.ts                # Custom hook for SSE streaming
      useQuery.ts                    # Query submission hook
```

---

## Port Interfaces (Behavioral Contracts)

### LLMProvider Port

```
Responsibilities:
  - Generate text completion from a prompt
  - Stream text completion token-by-token
  - Handle rate limiting and retries internally

Behavioral contract:
  - generate(prompt, max_tokens, temperature) -> text
  - stream(prompt, max_tokens, temperature) -> AsyncIterator[text_chunk]
  - Both raise LLMProviderError on failure (not provider-specific exceptions)
  - Timeout: 30 seconds per call
  - Retry: 3 attempts with exponential backoff for transient errors

Implementations:
  - GroqProvider (MVP)
  - Future: AnthropicProvider, OpenAIProvider, OllamaProvider
```

### EmbeddingProvider Port

```
Responsibilities:
  - Convert text to vector embedding
  - Batch embedding for ingestion efficiency

Behavioral contract:
  - embed_text(text) -> vector[float]
  - embed_batch(texts) -> list[vector[float]]
  - Embedding dimension is consistent (384 for MiniLM)
  - Deterministic: same text always produces same vector

Implementations:
  - SentenceTransformerEmbedder (local, MVP)
  - Future: OpenAI embeddings, Cohere embeddings
```

### PaperRepository Port

```
Responsibilities:
  - Store and retrieve papers with metadata and embeddings
  - Vector similarity search for RAG retrieval

Behavioral contract:
  - find_similar(query_vector, top_k) -> list[ChunkWithMetadata]
  - get_by_doi(doi) -> Paper | None
  - save(paper) -> Paper
  - get_corpus_metadata() -> CorpusMetadata (date, count)

Implementations:
  - PgPaperRepository (PostgreSQL + pgvector)
```

---

## Module Responsibility Matrix

| Module | Responsibility | Does NOT |
|--------|---------------|----------|
| `domain/` | Data models, evidence scoring, query classification, context templates | Call external services, access database, use framework APIs |
| `ports/` | Define behavioral contracts for external dependencies | Contain any implementation logic |
| `services/` | Orchestrate business workflows through ports | Know which adapter implements which port |
| `adapters/` | Implement ports with specific technologies | Contain business logic |
| `api/` | HTTP routing, request validation, SSE streaming, DI wiring | Contain RAG logic, database queries |
| `config/` | Application settings, feature flags, pre-loaded query data | Contain business logic |
