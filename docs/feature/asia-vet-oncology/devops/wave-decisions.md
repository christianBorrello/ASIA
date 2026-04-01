# Wave Decisions -- ASIA Vet Oncology DEVOPS

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## Decision Summary

| # | Decision | Rationale | Reversible? |
|---|----------|-----------|-------------|
| 1 | **Deployment Target**: Local MacBook Air M1 8GB, Docker Compose | EUR 0 budget, demo to 1-3 vets, no cloud needed | Yes -- containerized, portable to any Docker host |
| 2 | **Container Orchestration**: Docker Compose | Lightweight, single-machine, appropriate for 3 services | Yes -- Compose files map to K8s manifests if needed |
| 3 | **CI/CD Platform**: GitHub Actions | Free for public repos, native GitHub integration | Yes -- pipeline logic is in YAML, portable to other CI |
| 4 | **Existing Infrastructure**: None (greenfield) | No prior infrastructure exists for this project | N/A |
| 5 | **Observability**: Structured JSON logs to stdout only | No room in 8GB RAM for Prometheus+Grafana; `docker compose logs` sufficient for demo | Yes -- add Prometheus endpoint post-MVP |
| 6 | **Deployment Strategy**: Recreate (stop-and-replace) | Local demo, no uptime requirement, simplest possible | Yes -- upgrade to rolling/blue-green if deployed to server |
| 7 | **Continuous Learning**: Deferred | Focus on foundational setup for 10-day timeline | N/A |
| 8 | **Git Branching**: Trunk-based development | 1 developer, no coordination overhead, short-lived feature branches | Yes -- add develop branch if team grows |
| 9 | **Mutation Testing**: Disabled | MVP prototype, 10-day timeline, test quality via code review + CI coverage gate (70%) | Yes -- enable per-feature post-MVP |

---

## Rejected Alternatives

### Decision 1: Deployment Target

| Alternative | Why Rejected |
|-------------|-------------|
| AWS/GCP free tier | Adds operational complexity (networking, security, IAM), EUR 0 means no risk of accidental charges, demo is local |
| Raspberry Pi cluster | Insufficient RAM, over-engineered for demo |
| Native (no Docker) | Viable fallback documented in platform-architecture.md. Docker chosen for reproducibility. |

### Decision 5: Observability

| Alternative | Why Rejected |
|-------------|-------------|
| Prometheus + Grafana in Docker Compose | ~500MB additional RAM, operational overhead for zero-user demo |
| OpenTelemetry Collector | Same RAM concern, plus configuration complexity |
| Application-level metrics endpoint only (no dashboard) | Partial solution -- could add `/metrics` endpoint cheaply but no viewer. Deferred. |

### Decision 6: Deployment Strategy

| Alternative | Why Rejected |
|-------------|-------------|
| Rolling update | Requires multiple replicas per service -- not applicable to single-instance Docker Compose |
| Blue-green | Requires 2x resource allocation -- does not fit in 8GB |
| Canary | Requires traffic splitting -- not applicable to localhost |

### Decision 9: Mutation Testing

| Alternative | Why Rejected |
|-------------|-------------|
| Per-feature mutation testing (5-15 min) | 10-day timeline, solo developer learning Python -- mutation testing overhead not justified for MVP |
| Nightly-delta mutation testing | No CI/CD nightly runs for MVP; pipeline is push-triggered only |

---

## Quality Gates Applied

- [x] Every decision justified with constraints (budget, RAM, team size, timeline)
- [x] Simpler alternatives documented for decisions with >3 components
- [x] Rollback procedure documented (platform-architecture.md Section 9)
- [x] Local quality gates mirror CI (pre-commit/pre-push hooks)
- [x] Security scanning included (gitleaks in hooks + CI)
- [x] DORA metrics baseline established (see below)

---

## DORA Metrics Baseline (MVP)

| Metric | Current (no infrastructure) | Target (with this design) | Accelerate Level |
|--------|---------------------------|--------------------------|-----------------|
| Deployment frequency | N/A (no deployments) | On-demand (local `docker compose up`) | N/A (local) |
| Lead time for changes | N/A | < 5 min (push to CI pass) | Elite |
| Change failure rate | N/A | Target < 15% (CI gates catch failures before merge) | Elite |
| Time to restore | N/A | < 5 min (`docker compose down -v && docker compose up`) | Elite |

DORA metrics are aspirational for MVP. The CI pipeline and pre-commit hooks are designed to catch issues before they reach `main`, keeping change failure rate low. Recovery is fast because the entire state can be rebuilt from scratch in minutes.

---

## Artifacts Produced

| Artifact | Path | Purpose |
|----------|------|---------|
| Platform Architecture | `devops/platform-architecture.md` | Docker Compose design, resource limits, local dev setup |
| CI/CD Pipeline | `devops/ci-cd-pipeline.md` | GitHub Actions workflow, quality gates, pre-commit hooks |
| Observability Design | `devops/observability-design.md` | Structured logging strategy, log event taxonomy |
| KPI Instrumentation | `devops/kpi-instrumentation.md` | How to measure 6 outcome KPIs from DISCUSS |
| Branching Strategy | `devops/branching-strategy.md` | Trunk-based development for solo developer |
| Environment Inventory | `devops/environments.yaml` | Environment definitions for DISTILL handoff |
| Wave Decisions | `devops/wave-decisions.md` | This document |

---

## Handoff Notes for Acceptance Designer (DISTILL Wave)

1. **Two environments exist**: `local-dev` (Docker Compose) and `ci` (GitHub Actions). No staging or production.
2. **Acceptance tests run in CI** against a PostgreSQL service container (`pgvector/pgvector:pg16`). The `backend-test` job provides this.
3. **The 5 critical queries** should be implemented as integration tests in `backend/tests/critical_queries/` and added to CI after the RAG pipeline is functional.
4. **Pre-commit hooks** enforce formatting and linting locally. Acceptance tests run in CI only (too slow for local hooks).
5. **Coverage threshold is 70%** for MVP (not the standard 80%). This is a deliberate decision given the 10-day timeline.
6. **No deployment pipeline exists** -- demo deployment is manual `docker compose up` on Christian's MacBook.
7. **KPI measurement is manual** (questionnaire + observation). Application instrumentation provides supporting data only (response times, citation verification logs).
