# ADR-006: PostgreSQL + pgvector for Vector Storage

## Status

Accepted

## Context

ASIA needs both relational storage (cases, query logs, paper metadata, ingestion runs) and vector similarity search (embedding-based retrieval for RAG). The system runs on a MacBook Air M1 8GB via Docker Compose.

The corpus is small (~2000 papers, ~5000 chunks) and the concurrent user count is 1-3 (demo).

## Decision

Use PostgreSQL 16 with the pgvector extension as a single database for both relational and vector storage. Use IVFFlat indexing with ~50 lists for approximate nearest neighbor search.

## Alternatives Considered

### 1. PostgreSQL (relational) + Qdrant (vector)

Separate dedicated vector database. **Rejected** because: (a) adds an entire Docker service consuming ~500MB additional RAM on an 8GB machine, (b) requires synchronizing paper metadata between two databases, (c) operational complexity of managing two data stores for a solo developer, (d) Qdrant's advantages (filtering, HNSW, scale) are unnecessary for 5000 chunks.

### 2. PostgreSQL (relational) + ChromaDB (vector)

ChromaDB as lightweight vector store. **Rejected** because: (a) ChromaDB persistence is less mature than pgvector, (b) still two data stores to manage, (c) ChromaDB's DuckDB+Parquet backend adds storage complexity, (d) pgvector achieves comparable performance for this corpus size.

### 3. SQLite + sqlite-vss

Ultra-lightweight single-file database with vector extension. **Rejected** because: (a) sqlite-vss is less mature than pgvector, (b) SQLite lacks concurrent write support (problematic if ingestion runs while queries are served), (c) no JSONB type for flexible citation/metadata storage, (d) harder to migrate to a production database later.

### 4. Pinecone (managed vector DB)

Fully managed vector search service. **Rejected** because: (a) requires paid plan for persistence beyond free tier limits, (b) EUR 0 budget, (c) network dependency for every retrieval query, (d) vendor lock-in for a core operation.

## Consequences

### Positive

- Single database for all data: simpler operations, simpler backups, simpler Docker Compose
- pgvector IVFFlat performs well for <100K vectors with minimal tuning
- PostgreSQL 16 JSONB provides flexible metadata storage
- Zero additional cost (PostgreSQL License, permissive)
- Well-supported Docker image for ARM64 (M1)
- Migration path: if the corpus grows significantly, pgvector HNSW index can replace IVFFlat without application changes

### Negative

- pgvector IVFFlat requires rebuilding the index after significant data changes (acceptable for batch ingestion)
- Vector search performance is lower than dedicated vector DBs at scale (irrelevant for 5000 chunks)
- Embedding dimension is fixed at table creation -- changing embedding model requires schema migration
- No built-in vector metadata filtering (must use WHERE clauses alongside vector search -- pgvector supports this but it is less optimized than dedicated vector DBs)
