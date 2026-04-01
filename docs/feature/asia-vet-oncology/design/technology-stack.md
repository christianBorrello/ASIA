# Technology Stack -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DESIGN
**Date**: 2026-04-01

---

## Stack Overview

| Layer | Technology | Version | License | Rationale |
|-------|-----------|---------|---------|-----------|
| **Backend framework** | FastAPI | 0.110+ | MIT | Async Python, built-in SSE support, OpenAPI docs, lightweight |
| **Language (backend)** | Python | 3.12+ | PSF | Richest ML/NLP ecosystem, sentence-transformers compatibility |
| **Frontend framework** | Next.js | 14+ | MIT | React SSR, TypeScript support, good DX for solo dev |
| **Frontend language** | TypeScript | 5.x | Apache 2.0 | Type safety, IDE support, maintainability |
| **CSS framework** | Tailwind CSS | 3.x | MIT | Utility-first, rapid UI development, tablet-first responsive |
| **Database** | PostgreSQL | 16 | PostgreSQL License (permissive) | Mature RDBMS, JSON support, extensible |
| **Vector extension** | pgvector | 0.7+ | PostgreSQL License | Vector similarity search inside PostgreSQL, no separate vector DB needed |
| **LLM inference** | Groq API (Llama 3.3 70B) | -- | Groq free tier / Llama: Meta Community License | Zero cost, fast inference, Italian language capability |
| **LLM adapter** | Custom port interface | -- | Project (Apache 2.0) | Abstracts LLM provider, enables swap to Anthropic/OpenAI/Ollama |
| **Embeddings** | sentence-transformers | 3.x | Apache 2.0 | Local embedding, no API cost, multilingual models available |
| **Embedding model** | all-MiniLM-L6-v2 (primary) | -- | Apache 2.0 | 80MB, 384 dims, fits M1 8GB, good cross-lingual performance |
| **Embedding model (fallback)** | paraphrase-multilingual-MiniLM-L12-v2 | -- | Apache 2.0 | 420MB, better Italian-English cross-lingual if primary insufficient |
| **Task scheduling** | APScheduler | 3.x | MIT | Lightweight, in-process, no separate broker (unlike Celery) |
| **HTTP client** | httpx | 0.27+ | BSD-3 | Async HTTP for external API calls (PubMed, Semantic Scholar, Groq) |
| **Data validation** | Pydantic | 2.x | MIT | Request/response validation, settings management |
| **Containerization** | Docker Compose | 2.x | Apache 2.0 | Single-machine orchestration, works on M1 |
| **Python linting** | Ruff | 0.4+ | MIT | Fast Python linter + formatter, replaces flake8/black/isort |
| **Architecture enforcement (Python)** | import-linter | 2.x | BSD-2 | Enforces module boundary contracts |
| **Architecture enforcement (TS)** | eslint-plugin-boundaries | 4.x | MIT | Enforces frontend component boundaries |
| **Testing (Python)** | pytest | 8.x | MIT | Standard Python test framework |
| **Testing (TS)** | Vitest | 1.x | MIT | Fast Vite-native test runner for frontend |
| **Contract testing** | pact-python | 2.x | MIT | Consumer-driven contract tests for external APIs |
| **Pre-commit hooks** | pre-commit | 3.x | MIT | Git hook framework for automated checks |

---

## Selection Rationale

### Why FastAPI over Django/Flask

- **Django**: Too much built-in functionality not needed (admin, ORM, auth). Heavier for a single-purpose API.
- **Flask**: No built-in async support. SSE streaming requires additional libraries.
- **FastAPI**: Native async, built-in SSE via `StreamingResponse`, automatic OpenAPI docs, Pydantic integration. Ideal for a streaming RAG API.

### Why Next.js over Vite React / SvelteKit

- **Vite React (SPA)**: No SSR. For an MVP with a small number of pages, SSR is not critical, but Next.js provides better project structure and routing conventions.
- **SvelteKit**: Smaller ecosystem. Christian has React background, not Svelte.
- **Next.js**: React ecosystem (Christian's background), good TypeScript support, file-based routing simplifies the 3-4 page MVP.

### Why PostgreSQL + pgvector over Dedicated Vector DB

- **Pinecone/Weaviate/Qdrant**: Separate service, additional operational complexity, some require paid tiers for persistence.
- **ChromaDB**: Simpler but less mature, no production SQL alongside vector search.
- **PostgreSQL + pgvector**: Single database for both relational data (cases, query logs, paper metadata) and vector search. Eliminates an entire service from the stack. Well within performance needs for ~2000 papers.

### Why Groq over Ollama (Local LLM)

- **Ollama with 7B model**: Fits in 8GB RAM but quality insufficient for Italian medical synthesis.
- **Ollama with 70B model**: Does not fit in 8GB RAM.
- **Groq free tier (Llama 3.3 70B)**: 70B model quality at zero cost. Network dependency accepted for MVP (demo will have internet). LLM Adapter pattern enables future swap to local Ollama if needed.

### Why APScheduler over Celery

- **Celery**: Requires Redis or RabbitMQ as broker. Additional container, additional memory, additional complexity for a task that runs once daily.
- **APScheduler**: In-process scheduler, zero additional infrastructure. Sufficient for scheduled ingestion in MVP.

---

## Memory Budget (MacBook Air M1 8GB)

| Component | Estimated RAM | Notes |
|-----------|--------------|-------|
| macOS + system | ~2.5GB | Base OS consumption |
| Docker Desktop | ~500MB | Overhead |
| PostgreSQL 16 + pgvector | ~500MB | With ~2000 papers, IVFFlat index |
| FastAPI + sentence-transformers (all-MiniLM-L6-v2) | ~1.5GB | Model loaded at startup |
| Next.js dev server | ~300MB | Production build: ~150MB |
| Browser (testing) | ~500MB | 2-3 tabs |
| **Total** | **~5.8GB** | ~2.2GB headroom |

If using `paraphrase-multilingual-MiniLM-L12-v2` (420MB), total increases by ~340MB -- still within budget.

---

## License Compliance

All technologies use permissive open-source licenses (MIT, Apache 2.0, BSD, PostgreSQL License, PSF). No copyleft (GPL/AGPL) dependencies in the core stack. The project itself is Apache 2.0.

Meta Community License for Llama 3.3: Permits commercial use for organizations with <700M monthly active users. No concern for this project.
