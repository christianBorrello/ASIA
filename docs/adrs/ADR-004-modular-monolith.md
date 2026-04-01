# ADR-004: Modular Monolith with Ports-and-Adapters

## Status

Accepted

## Context

ASIA needs an architectural style that supports:
- A single developer building and maintaining the entire system
- A 10-day MVP timeline
- Clean testability (mock LLM, mock database for unit tests)
- Future extensibility (new LLM providers, new data sources, new features)
- Easy deployment (Docker Compose on a MacBook Air)

The quality attribute priorities are: correctness > time-to-market > maintainability > testability.

## Decision

Adopt a modular monolith with ports-and-adapters (hexagonal architecture) for the Python backend. A single FastAPI process contains all business logic organized into domain modules with explicit dependency boundaries enforced by import-linter.

Structure:
- `domain/`: Pure domain models and logic (no external dependencies)
- `ports/`: Abstract interfaces for external dependencies
- `services/`: Application orchestration (uses ports, never adapters)
- `adapters/`: Concrete implementations of ports
- `api/`: FastAPI routes and dependency injection wiring

Dependencies flow inward: api -> services -> ports <- adapters. Domain is dependency-free.

## Alternatives Considered

### 1. Microservices (separate RAG service, ingestion service, API gateway)

Split into independently deployable services. **Rejected** because: (a) team size = 1, microservices require operational maturity (service discovery, distributed tracing, deployment orchestration) that a solo developer cannot maintain, (b) 10-day timeline leaves no room for distributed system debugging, (c) inter-service communication adds latency to the RAG pipeline, (d) Docker Compose on 8GB RAM cannot run 3+ services with PostgreSQL simultaneously.

### 2. Simple layered architecture (controller -> service -> repository)

Traditional three-layer architecture without explicit ports. **Rejected** because: (a) no clean way to swap LLM providers without touching service layer, (b) testing requires mocking concrete implementations rather than interfaces, (c) dependency direction is not enforced -- services tend to directly import adapter-level code over time.

### 3. Serverless / FaaS (AWS Lambda or similar)

Deploy each endpoint as a serverless function. **Rejected** because: (a) cold start latency incompatible with 3-second first-token target, (b) sentence-transformers model loading on each cold start is prohibitive, (c) adds cloud provider dependency to an open-source project designed for local deployment, (d) EUR 0 budget (free tiers exist but add operational complexity).

## Consequences

### Positive

- Single process: simple deployment, simple debugging, simple mental model
- Ports-and-adapters: LLM provider swap requires only a new adapter + env var
- import-linter: architectural rules are automatically enforced in CI
- One developer can hold the entire system in their head
- Docker Compose: `docker compose up` and the system runs

### Negative

- All components share a process: a bug in ingestion could affect the API (mitigated by running ingestion as a separate Docker service sharing the same codebase)
- Cannot scale components independently (not needed for 1-3 demo users)
- If the project grows to multiple developers, module boundaries may need to evolve toward separate services (the port boundaries make this migration path clean)
