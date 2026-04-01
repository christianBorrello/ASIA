# ASIA — Project Configuration

## Development Paradigm
This project follows the **object-oriented** paradigm with functional elements for domain logic (pure functions for evidence scoring, query classification, context injection). Use @nw-software-crafter for implementation.

## Mutation Testing Strategy
Mutation testing is **disabled**. Test quality validated through code review and CI coverage. Enable per-feature post-MVP.

## Stack
- Backend: FastAPI (Python 3.12+)
- Frontend: Next.js + TypeScript + Tailwind
- Database: PostgreSQL 16 + pgvector
- LLM: Groq free tier (Llama 3.3 70B) via LLM adapter pattern
- Embedding: sentence-transformers (all-MiniLM-L6-v2)
- Container: Docker Compose

## Architecture
Modular monolith with ports-and-adapters (hexagonal). See docs/feature/asia-vet-oncology/design/ for details.
