# Wave Decisions -- ASIA Vet Oncology DESIGN

**Feature ID**: asia-vet-oncology
**Wave**: DESIGN
**Architect**: Morgan (Solution Architect)
**Date**: 2026-04-01
**Status**: Complete (pending peer review)

---

## Key Decisions Summary

| # | Decision | Rationale | ADR | Reversible? |
|---|----------|-----------|-----|-------------|
| D1 | Modular monolith with ports-and-adapters | Solo dev, 10-day timeline, testability via port mocking, Docker Compose simplicity | ADR-004 | Yes -- port boundaries enable future service extraction |
| D2 | LLM Adapter pattern (abstract LLMProvider port) | Zero-cost Groq MVP, must be swappable to Anthropic/OpenAI/Ollama without business logic changes | ADR-001 | N/A -- this is the abstraction enabling reversibility |
| D3 | Self-reflective RAG with 2-phase verification | Kill criterion: zero hallucinated citations. Generate then verify with SUPPORTA/PARZIALE/NON_SUPPORTA classification | ADR-002 | Yes -- can simplify to single-pass if verification proves unnecessary |
| D4 | Groq free tier (Llama 3.3 70B) as MVP LLM | EUR 0 budget, 70B model quality for Italian medical text, fast inference | ADR-003 | Yes -- adapter pattern, env var swap |
| D5 | all-MiniLM-L6-v2 as primary embedding model | 80MB fits M1 8GB, 384 dims, cross-lingual capability. Fallback: multilingual-MiniLM-L12-v2 | ADR-005 | Yes -- same dimensions, config change only |
| D6 | PostgreSQL 16 + pgvector (single DB) | Relational + vector in one service, no separate vector DB overhead on 8GB RAM | ADR-006 | Partially -- would require data migration to separate vector DB |
| D7 | SSE streaming with metadata-first event sequence | Send evidence level + sources before synthesis text for perceived speed | -- | Yes |
| D8 | Evidence scoring: ALTO/MODERATO/BASSO algorithm | Formula-based scoring from study type + count + sample size. Thresholds calibrated against 5 critical queries | -- | Yes -- thresholds are configuration |
| D9 | Batch citation verification (single LLM call) | All citation-claim pairs verified in one prompt to minimize latency | -- | Yes -- can switch to per-citation calls |
| D10 | Pre-loaded queries as backend config (not frontend) | Single source of truth, API-driven, prevents frontend/backend mismatch | -- | Yes |

---

## DISCUSS Peer Review Issues Resolved

| Issue | Priority | Resolution | Location |
|-------|----------|------------|----------|
| H1: Self-Reflective RAG Algorithm | HIGH | Defined 2-phase algorithm with SUPPORTA/PARZIALE/NON_SUPPORTA classification, pass/fail criteria, max iterations, timeout, example walkthrough | architecture-design.md Section 5 + ADR-002 |
| H2: Emotional Arc for Error Paths | HIGH | Defined emotional arcs for E1-E4 with timeline, UX elements, and design principles | architecture-design.md Section 6 |
| H3: Streaming Performance Metrics | HIGH | Defined precise metrics: first token <=3s, first text <=5s, evidence level before stream, final token <=30s, source panel <=32s | architecture-design.md Section 7 |
| M1: Version Pre-loaded Queries | MEDIUM | Created single-source-of-truth document with exact query texts, expected outputs, validation rules | pre-loaded-queries.md |
| M2: Evidence Level Scoring | MEDIUM | Defined formula with study type weights, count bonus, sample size bonus, and ALTO/MODERATO/BASSO thresholds | architecture-design.md Section 8 |
| M3: Case Context Injection Template | MEDIUM | Defined exact prompt template with behavior rules (empty fields omitted, context affects synthesis not retrieval) | architecture-design.md Section 9 |
| M4: Accessibility Criteria | MEDIUM | WCAG 2.1 AA baseline with 8 specific criteria and evidence level accessibility requirements | architecture-design.md Section 10 |

---

## Artifacts Produced

| Artifact | Path | Purpose |
|----------|------|---------|
| Architecture Design | `design/architecture-design.md` | Full architecture with C4 diagrams, RAG algorithm, error arcs, performance specs |
| Technology Stack | `design/technology-stack.md` | Stack decisions with rationale and memory budget |
| Component Boundaries | `design/component-boundaries.md` | Module structure, port interfaces, dependency rules, enforcement config |
| Data Models | `design/data-models.md` | PostgreSQL schema for papers, chunks, cases, queries, ingestion runs |
| Pre-loaded Queries | `design/pre-loaded-queries.md` | Single source of truth for 5 critical queries (resolves M1) |
| Wave Decisions | `design/wave-decisions.md` | This document |
| ADR-001 | `docs/adrs/ADR-001-llm-adapter-pattern.md` | LLM Adapter pattern |
| ADR-002 | `docs/adrs/ADR-002-self-reflective-rag.md` | Self-reflective RAG approach |
| ADR-003 | `docs/adrs/ADR-003-groq-mvp-llm-provider.md` | Groq as MVP LLM provider |
| ADR-004 | `docs/adrs/ADR-004-modular-monolith.md` | Modular monolith architecture |
| ADR-005 | `docs/adrs/ADR-005-embedding-model.md` | Embedding model selection |
| ADR-006 | `docs/adrs/ADR-006-postgresql-pgvector.md` | PostgreSQL + pgvector |

---

## Quality Gates Checklist

- [x] Requirements traced to components (US-01 through US-07 mapped to modules)
- [x] Component boundaries with clear responsibilities (component-boundaries.md)
- [x] Technology choices in ADRs with alternatives (6 ADRs, each with 2+ alternatives)
- [x] Quality attributes addressed: correctness (self-reflective RAG), performance (streaming specs), reliability (error handling), maintainability (ports-and-adapters)
- [x] Dependency-inversion compliance (ports/adapters, import-linter enforcement)
- [x] C4 diagrams: L1 (System Context) + L2 (Container) + L3 (RAG Pipeline Component)
- [x] Integration patterns specified (REST/SSE, Groq API, PubMed/Semantic Scholar)
- [x] OSS preference validated (all technologies OSS with permissive licenses)
- [x] AC behavioral, not implementation-coupled
- [x] External integrations annotated with contract test recommendation (Groq, PubMed, Semantic Scholar)
- [x] Architectural enforcement tooling recommended (import-linter, eslint-plugin-boundaries)
- [x] Peer review completed and approved (iteration 1)

---

## Peer Review Proof

```yaml
review_id: "arch_rev_20260401_001"
reviewer: "solution-architect-reviewer"
artifact: "design/architecture-design.md, design/*.md, docs/adrs/ADR-001 through ADR-006"
iteration: 1

strengths:
  - "Quality-attribute-driven architecture: correctness > time-to-market > maintainability ordering consistently reflected in all decisions"
  - "Every ADR has 2-4 considered alternatives with clear rejection rationale (ADR-001 through ADR-006)"
  - "C4 diagrams at all 3 levels (L1 System Context, L2 Container, L3 Component for RAG pipeline) with labeled arrows"
  - "Self-reflective RAG algorithm is concretely specified with pass/fail criteria, example walkthrough, and timeout constraints"
  - "Memory budget calculated and validated against M1 8GB constraint (5.8GB / 8GB)"
  - "All 7 DISCUSS peer review issues resolved with traceable locations"
  - "Architecture proportional to scope: modular monolith for 1 developer, no over-engineering"

issues_identified:
  architectural_bias:
    - issue: "No bias detected. All technology choices justified by constraints (budget, RAM, team size)."
      severity: "none"
  decision_quality:
    - issue: "ADR-005 has 'pending benchmark validation' status"
      severity: "low"
      location: "ADR-005"
      recommendation: "Appropriate given uncertainty. Ensure benchmark happens in first 2 days of development."
  completeness_gaps:
    - issue: "Missing observability/logging strategy"
      severity: "medium"
      location: "architecture-design.md Section 14"
      recommendation: "Add structured logging section for RAG pipeline decisions"
      resolution: "RESOLVED -- added Observability subsection to Section 14 with structlog, key log events, and RAG pipeline logging"
  implementation_feasibility:
    - issue: "No feasibility concerns. Stack aligns with developer background (React -> Next.js, learning Python -> FastAPI)."
      severity: "none"
  priority_validation:
    q1_largest_bottleneck:
      evidence: "Citation accuracy is kill criterion. Self-reflective RAG directly addresses this."
      assessment: "YES"
    q2_simple_alternatives:
      assessment: "ADEQUATE -- every ADR documents simpler rejected alternatives"
    q3_constraint_prioritization:
      assessment: "CORRECT -- EUR 0, 8GB RAM, solo dev constraints drive all decisions"
    q4_data_justified:
      assessment: "JUSTIFIED -- memory budget quantified, performance targets defined, corpus size estimated"

approval_status: "approved"
critical_issues_count: 0
high_issues_count: 0
```

### Revisions Made

| Issue | Severity | Action |
|-------|----------|--------|
| Missing observability/logging strategy | MEDIUM | Added "Observability (MVP-appropriate)" subsection to Section 14 of architecture-design.md with structlog, key log events, RAG pipeline logging |

No critical or high issues found. Architecture approved after iteration 1.

---

## Handoff Notes for Acceptance Designer (DISTILL Wave)

1. The 5 critical queries (pre-loaded-queries.md) are the primary acceptance criteria
2. Self-reflective RAG verification is defined algorithmically in architecture-design.md Section 5 -- acceptance tests should verify citation removal behavior
3. Error paths E1-E4 have defined emotional arcs -- acceptance tests should cover each error scenario
4. Streaming performance targets are quantified in Section 7 -- acceptance tests should measure time-to-first-token and total response time
5. Evidence level scoring has defined thresholds -- acceptance tests should verify ALTO/MODERATO/BASSO classification against known paper sets

## Handoff Notes for Platform Architect (DEVOPS Wave)

1. Docker Compose with 4 services: frontend, api, db, ingestion
2. Memory budget documented in technology-stack.md -- must fit in 8GB
3. External integrations requiring contract tests: Groq API, PubMed E-utilities, Semantic Scholar API. Recommended: consumer-driven contracts via pact-python in CI acceptance stage.
4. Architecture enforcement: import-linter (Python) and eslint-plugin-boundaries (TypeScript) should run in CI
5. Development paradigm: Python backend is multi-paradigm functional-leaning (pure functions for RAG pipeline, dataclasses for models, side effects at adapter boundaries)
