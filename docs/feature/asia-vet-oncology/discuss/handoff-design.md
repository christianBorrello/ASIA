# DISCUSS Wave Handoff -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**From**: DISCUSS wave (product-owner)
**To**: DESIGN wave (solution-architect)
**Date**: 2026-04-01
**Status**: Ready for handoff

---

## Handoff Package Contents

| Artifact | Path | Purpose |
|----------|------|---------|
| Journey Visual | `discuss/journey-vet-clinical-query-visual.md` | ASCII mockups + emotional arc + TUI mockups for all 5 journey steps + error paths |
| Journey Schema | `discuss/journey-vet-clinical-query.yaml` | Structured YAML: steps, shared artifacts, emotional states, integration checkpoints |
| Gherkin Scenarios | `discuss/journey-vet-clinical-query.feature` | 20 testable scenarios (17 behavioral + 4 @property) |
| Story Map | `discuss/story-map.md` | Backbone, walking skeleton, 3 release slices |
| Prioritization | `discuss/prioritization.md` | Priority scoring, MoSCoW, dependencies, build sequence |
| Shared Artifacts | `discuss/shared-artifacts-registry.md` | 10 artifacts with source, consumers, risk, validation |
| Outcome KPIs | `discuss/outcome-kpis.md` | 6 KPIs with measurement plan + kill criteria |
| User Stories | `discuss/user-stories.md` | 7 LeanUX stories with BDD scenarios + DoR validation |
| Coherence Validation | `discuss/coherence-validation.md` | 6-dimension validation (all PASS) |
| Peer Review | `discuss/peer-review.md` | Review iteration 1: APPROVED (0 critical, 0 high) |

---

## Executive Summary

ASIA is a RAG-powered clinical query tool for Italian veterinarians managing canine lymphoma cases. The MVP has 6 features mapped to 7 user stories across 3 release slices:

1. **Walking Skeleton** (WS, ~3 days): Homepage + one clinical query with RAG synthesis and citations
2. **Demo Ready** (R1, ~4 days): 5 pre-loaded queries, comparison table, error handling
3. **Clinical Workflow** (R2, ~3 days): Case mode with context injection, Explain This Paper

The validation instrument is a demo to Asia's vet team (1-3 vets). Success = 4/5 critical queries rated accurate + at least 1 vet commits to using it for a real case.

---

## Key Constraints for DESIGN Wave

| Constraint | Impact |
|-----------|--------|
| EUR 0 operating cost | Groq free tier (Llama 3.3 70B) with LLM adapter pattern for future swap |
| Tablet-first | Responsive design: tablet (768px) primary, desktop secondary |
| No authentication | Demo in controlled context; auth is post-MVP |
| Italian synthesis | LLM must produce natural Italian medical terminology |
| Citation accuracy | Zero tolerance for hallucinated citations (kill criterion) |
| Self-reflective RAG | Generate -> verify citations -> refine (max 2 iterations) |
| Docker Compose | Single-machine deployment for demo |
| Apache 2.0 | Open source license |

---

## Critical Design Decisions Needed

These are questions for the solution-architect to resolve in DESIGN wave:

1. **RAG pipeline architecture**: Single-pass vs multi-pass retrieval? How many chunks per query? Reranking strategy for small corpus?
2. **Confidence threshold**: What score triggers "no evidence" vs synthesis? How is it computed?
3. **Evidence level algorithm**: What criteria define ALTO/MODERATO/BASSO? (Study type weights, count thresholds, sample size thresholds)
4. **Comparison table detection**: How does the system decide when a query warrants a comparison table? (LLM-based vs keyword-based)
5. **Context injection format**: How is case data prepended to the RAG prompt? (Template structure)
6. **SSE streaming**: Token-by-token vs sentence-by-sentence streaming? How to handle mid-stream errors?
7. **Embedding model**: Which sentence-transformer model for Italian medical text? Benchmarking needed.

---

## Risk Summary

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| LLM produces poor Italian medical terminology | Medium | High | Benchmark with 5 critical queries before demo; consider Mixtral if Llama insufficient |
| Citation hallucination | Medium | Critical | Self-reflective RAG with max 2 verification passes |
| Groq free tier rate limits during demo | Low | Medium | Pre-warm cache for 5 critical queries; consider local LLM fallback |
| Corpus too small for complex queries | Medium | Medium | Focus on multicentric lymphoma; honest "no evidence" for out-of-scope |
| Vet team gives polite but uncommitted feedback | Medium | Medium | Use commitment test framework from interview-log.md |

---

## Acceptance Criteria Summary (5 Critical Queries)

These are the demo's acceptance test. All 5 must produce responses before the demo:

| # | Query | Must Include |
|---|-------|-------------|
| Q1 | Protocollo prima linea B-cell stadio III | CHOP, relevant citations, accurate remission rates |
| Q2 | CHOP-19 vs CHOP-25 differenze | Equivalence per European multicenter study, comparison table |
| Q3 | Rescue per recidiva precoce dopo CHOP | Multiple rescue options (Tanovea, LAP, LOPP, DMAC) with evidence |
| Q4 | Prognosi T-cell vs B-cell | B-cell better prognosis, specific survival data |
| Q5 | Aggiustamento dose doxorubicina per neutropenia | Grade-specific guidance: delay vs reduce vs switch |

---

## Discovery Artifacts Reference

For full context, DESIGN wave should also review:

| Artifact | Path | Key Content |
|----------|------|-------------|
| Problem Validation | `discover/problem-validation.md` | Market gap evidence, founder experience |
| Opportunity Tree | `discover/opportunity-tree.md` | 10 opportunities scored, top 3: O1 (16), O2 (16), O3 (14) |
| Solution Testing | `discover/solution-testing.md` | 5 hypotheses (H1-H5), test plan, kill signals |
| Lean Canvas | `discover/lean-canvas.md` | 9-box canvas, 4 big risks assessment |
| Interview Log | `discover/interview-log.md` | Questionnaire design (Italian), interpretation guide |
| MVP Definition | `docs/mvp.md` | 6 features, stack, constraints, acceptance criteria |
