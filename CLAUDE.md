# ASIA — AI Assistant Guide

## Project Overview

ASIA (AI-powered Scientific Information Assistant) is a RAG-powered clinical decision support system for Italian veterinary oncologists. It retrieves and synthesizes scientific literature to answer clinical queries, with citation verification and evidence scoring.

**Language note:** The entire UI, LLM prompts, and responses are in **Italian**.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.12+), uvicorn |
| Frontend | Next.js 14 + TypeScript 5.5 + React 18 + Tailwind CSS 3 |
| Database | PostgreSQL 16 + pgvector (cosine similarity, 384-dim vectors) |
| LLM | Groq free tier (Llama 3.3 70B, fallback: Llama 3.1 8B) |
| Embedding | sentence-transformers (all-MiniLM-L6-v2, 384 dimensions) |
| Container | Docker Compose |

## Architecture

**Modular monolith with ports-and-adapters (hexagonal architecture).**

```
backend/asia/
├── domain/          # Pure domain models & functions (no I/O)
│   ├── models.py           # Dataclasses: Paper, Chunk, Case, EvidenceLevel
│   ├── evidence_scoring.py # Pure fn: compute_evidence_level()
│   ├── context_injection.py# Pure fn: build_patient_context()
│   └── query_types.py      # Pure fn: is_comparison_query()
├── ports/           # Protocol interfaces (abstract contracts)
│   ├── llm_provider.py         # generate(), stream()
│   ├── embedding_provider.py   # embed_text(), embed_batch()
│   ├── paper_repository.py     # find_similar(), get_by_doi(), save()
│   └── case_repository.py      # create(), get(), add_query()
├── adapters/        # Concrete implementations of ports
│   ├── groq_provider.py                # LLM with retry + fallback
│   ├── sentence_transformer_embedder.py# Embedding (multilingual MiniLM)
│   ├── pg_paper_repository.py          # PostgreSQL + pgvector (async)
│   ├── in_memory_case_repository.py    # MVP in-memory case store
│   ├── pubmed_fetcher.py               # PubMed data ingestion
│   └── semantic_scholar_fetcher.py     # Semantic Scholar ingestion
├── services/        # Application logic / orchestration
│   ├── rag_pipeline.py         # Core RAG: embed → retrieve → synthesize → verify → score
│   ├── synthesis_generator.py  # Italian synthesis with inline citations [N]
│   ├── citation_verifier.py    # LLM self-reflection: SUPPORTA/PARZIALE/NON_SUPPORTA
│   ├── case_service.py         # Case lifecycle management
│   └── paper_explainer.py      # Structured clinical summaries by DOI
├── api/             # HTTP layer
│   ├── main.py                 # FastAPI app + lifespan (startup/shutdown)
│   ├── dependencies.py         # DI via lru_cache factory functions
│   ├── middleware/              # Error handler
│   └── routes/                 # query, cases, metadata, explain_paper
└── config/
    ├── settings.py             # Pydantic BaseSettings (env vars)
    └── pre_loaded_queries.py   # Hardcoded Italian clinical queries
```

```
frontend/src/
├── app/             # Next.js App Router pages
│   ├── page.tsx             # Home: hero, corpus metadata, pre-loaded queries
│   ├── query/page.tsx       # Query execution with streaming synthesis
│   ├── explain/page.tsx     # Paper explanation by DOI
│   ├── cases/               # Case CRUD: list, new, [id] detail
│   └── layout.tsx
├── components/      # React components
│   ├── Navigation, SearchBox, Disclaimer, EvidenceLevel (shared)
│   ├── SynthesisView, SourcePanel, ComparisonTable (query)
│   ├── BodyMap, BodySystemPanel (cases)
│   └── PreLoadedQueryCard (home)
└── lib/
    ├── api.ts               # Fetch wrapper for all API calls
    ├── types.ts             # TypeScript interfaces matching backend models
    └── constants.ts
```

## Development Paradigm

**Object-oriented** with functional elements for domain logic. Pure functions for evidence scoring, query classification, and context injection. Services use constructor injection.

## Key Patterns

- **Dependency Injection**: `lru_cache` factory functions in `dependencies.py`; lifespan context manager wires services into `app.state`
- **Port/Adapter**: Protocol-based interfaces in `ports/`, swappable implementations in `adapters/`
- **RAG Pipeline**: embed query → retrieve similar chunks → resolve papers → generate synthesis → verify citations → compute evidence → extract comparison table
- **Groq Fallback**: On 429 (rate limit) → immediate fallback to smaller model; on 503 → exponential backoff retry (1s, 2s)
- **Evidence Scoring Formula**: `study_type_score + count_bonus + sample_size_bonus` → ALTO (>=40), MODERATO (>=20), BASSO (<20)
- **Citation Verification**: LLM self-reflection classifies each citation, removes unsupported ones, renumbers

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/query` | RAG synthesis (text, case_id, stream) |
| POST | `/api/cases` | Create clinical case |
| GET | `/api/cases/{id}` | Get case details |
| POST | `/api/cases/{id}/query` | Query within case context |
| GET | `/api/corpus-metadata` | Corpus stats |
| GET | `/api/pre-loaded-queries` | Pre-loaded Italian queries |
| GET | `/api/llm-status` | Groq availability check |
| POST | `/api/explain-paper` | Paper clinical summary by DOI |
| GET | `/api/health` | Health check |

## Database

Schema defined in `backend/db/migrations/001_initial_schema.sql`. Key tables:
- **papers** — scientific papers with metadata (JSONB authors, study_type, species, cancer_type)
- **chunks** — text chunks with `vector(384)` embeddings, IVFFlat cosine index (lists=50)
- **cases** — clinical cases (patient, breed, diagnosis, stage)
- **case_queries** — query history with full response data (JSONB citations, comparison_table)
- **ingestion_runs** — data ingestion tracking

Extensions: `uuid-ossp`, `pgvector`

## Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests (requires PostgreSQL)
pytest tests/integration/

# Acceptance tests (BDD steps)
pytest tests/acceptance/
```

- **Framework**: pytest with `anyio` plugin (asyncio_mode: auto)
- **Config**: Root `pyproject.toml` (pythonpath includes `backend/`)
- **Mutation testing**: Disabled (enable per-feature post-MVP)
- Tests cover: RAG pipeline, Groq fallback/retry, embedding, citation verification, evidence scoring, context injection, API endpoints, seed data

## Running Locally

```bash
# Full dev environment (validates prerequisites, starts DB + backend + frontend)
./start.sh

# Or via Docker Compose
docker-compose up

# Backend only (from backend/)
uvicorn asia.api.main:app --reload --port 8000

# Frontend only (from frontend/)
npm run dev
```

**Required env vars** (see `.env.example`):
- `DATABASE_URL` — PostgreSQL connection string
- `GROQ_API_KEY` — Groq API key for LLM
- `EMBEDDING_MODEL_NAME` — defaults to `all-MiniLM-L6-v2`
- `RETRIEVAL_TOP_K` — number of chunks to retrieve (default: 10)
- `CONFIDENCE_THRESHOLD` — minimum similarity score (default: 0.35)

## Conventions

### Code Style
- **Python**: Type hints throughout, async/await, Protocol-based interfaces, dataclasses for domain models
- **TypeScript**: Strict mode, interfaces for API contracts, path aliases (`@/*`)
- **Naming**: Python classes `CamelCase`, functions `snake_case`, private `_leading_underscore`; React components `PascalCase`; API routes `kebab-case`

### Design Rules
- Domain layer has **zero I/O** — pure dataclasses and functions only
- Services receive dependencies via **constructor injection**
- All LLM interactions go through the `LLMProvider` port — never call Groq directly
- New adapters must implement the corresponding Protocol in `ports/`
- Frontend API calls go through `lib/api.ts` — never use raw `fetch` in components

### Documentation
- Architecture docs: `docs/feature/asia-vet-oncology/design/`
- ADRs: `docs/adrs/`
- Vision & market research: `docs/vision.md`, `docs/market-research.md`
