# Coherence Validation -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: DISCUSS -- Phase 3 Coherence Validation
**Date**: 2026-04-01

---

## 1. UI Vocabulary Consistency

| Term | Used In | Consistent? |
|------|---------|-------------|
| "Scrivi la tua domanda clinica..." | Homepage search placeholder | Yes -- single instance |
| "Crea nuovo caso" | Homepage CTA, US-06 | Yes |
| "Explain a Paper" / "Analizza" | Homepage CTA, US-07 | Yes |
| "Fonti" | Source panel header | Yes -- single instance |
| "Sintesi" | Response section header | Yes -- single instance |
| "Confronto protocolli" | Comparison table header | Yes -- single instance |
| Evidence levels: ALTO/MODERATO/BASSO | Response page badge | Yes -- consistent 3-level scale |
| Disclaimer text | All pages | Yes -- single source constant |
| Corpus date | Homepage + response footer | Yes -- single API source |

### Verdict: PASS

No vocabulary inconsistencies detected. Italian terminology is consistent across all stories and mockups.

---

## 2. Emotional Arc Coherence

| Step | Entry Emotion | Exit Emotion | Transition |
|------|--------------|-------------|------------|
| 1. Arrive | Skeptical, time-pressed | Curious | Pre-loaded queries lower barrier; professional design |
| 2. Query | Curious | Engaged | Immediate streaming response |
| 3. Read | Engaged | Focused, building trust | Italian synthesis makes sense; citations are specific |
| 4. Verify | Building trust | Trusting | DOI links resolve to real papers; claims match |
| 5. Decide | Trusting | Satisfied | Has what she needs; saved time |

**Transition analysis**:
- No jarring transitions (no positive-to-negative without buffer)
- Confidence builds progressively through small wins: click -> see response -> verify citation -> trust
- Error paths (E1-E4) redirect to helpful guidance, preventing frustration spirals
- The emotional peak (Step 3-4) is where trust is built or broken -- citation accuracy is the critical moment

### Verdict: PASS

Emotional arc is coherent, progressive, and accounts for error states.

---

## 3. Shared Artifacts -- Single Source of Truth

| Artifact | Source | Consumers | Risk | Status |
|----------|--------|-----------|------|--------|
| disclaimer_text | Backend constants | 4 pages | HIGH | Tracked |
| corpus_date | Ingestion metadata | 2 pages | MEDIUM | Tracked |
| pre_loaded_queries | Backend config | 1 page | LOW | Tracked |
| query_text | User input / config | 3 consumers | MEDIUM | Tracked |
| synthesis_text | RAG output | 2 consumers | HIGH | Tracked |
| citations | RAG retrieval + verification | 2 consumers | CRITICAL | Tracked |
| evidence_level | RAG scoring | 1 consumer | MEDIUM | Tracked |
| comparison_table | RAG extraction | 1 consumer | MEDIUM | Tracked |
| case_data | User input | 3 consumers | MEDIUM | Tracked |
| doi_urls | Ingestion metadata | 2 consumers | HIGH | Tracked |

**All 10 shared artifacts documented in shared-artifacts-registry.md with source, consumers, risk level, and validation method.**

### Verdict: PASS

No untracked artifacts. All ${variables} in mockups have documented sources.

---

## 4. Horizontal Integration

### Integration Checkpoint Validation

| Checkpoint | Description | Stories Involved | Status |
|------------|-------------|-----------------|--------|
| CP1 | Query-to-Response Integrity | US-02, US-03 | Defined |
| CP2 | Citation Consistency (markers match sources) | US-02, US-05 | Defined |
| CP3 | Disclaimer Consistency across pages | US-01, US-02, US-06, US-07 | Defined |
| CP4 | Case Context Injection | US-06 + US-02 | Defined |
| CP5 | Corpus Date Accuracy | US-01 + ingestion pipeline | Defined |

### Cross-Story Dependencies

| Story | Depends On | Status |
|-------|-----------|--------|
| US-02 | US-01 (entry point), ingestion pipeline | Tracked |
| US-03 | US-02 (RAG query execution) | Tracked |
| US-04 | US-02 (RAG response format) | Tracked |
| US-05 | US-02 (error states from RAG) | Tracked |
| US-06 | US-01 (CTA), US-02 (query execution) | Tracked |
| US-07 | US-01 (CTA), ingestion pipeline (DOI metadata) | Tracked |

### Verdict: PASS

All integration checkpoints defined. All dependencies tracked.

---

## 5. Web UX Compliance

| Heuristic | Coverage | Status |
|-----------|----------|--------|
| Visibility of system status | Streaming SSE, progress indicator, loading state | PASS |
| Match real world | Italian medical terminology, vet domain language | PASS |
| User control and freedom | Back to homepage, past queries re-accessible | PASS |
| Consistency and standards | Single vocabulary, consistent evidence levels | PASS |
| Error prevention | Pre-loaded queries reduce error; confidence threshold prevents hallucination | PASS |
| Recognition over recall | Pre-loaded queries, case context injection | PASS |
| Flexibility and efficiency | Free-text + pre-loaded; case mode for power users | PASS |
| Aesthetic and minimalist | Clean, professional, tablet-first, no decorative clutter | PASS |
| Help with errors | Italian error messages with explanation + suggestions + PubMed link | PASS |
| Help and documentation | Disclaimer, corpus date, evidence level explanation | PARTIAL (no tooltip for evidence levels -- minor) |

### Verdict: PASS (1 minor item noted)

Minor improvement opportunity: add tooltip explaining ALTO/MODERATO/BASSO evidence levels. Not blocking.

---

## 6. Story Sizing

| Story | Estimated Days | UAT Scenarios | Demonstrates In | Verdict |
|-------|---------------|---------------|-----------------|---------|
| US-01 | 1 | 4 | Single session | Right-sized |
| US-02 | 2-3 | 5 | Single session | Right-sized |
| US-03 | 1 | 3 | Single session | Right-sized |
| US-04 | 1-2 | 3 | Single session | Right-sized |
| US-05 | 1-2 | 4 | Single session | Right-sized |
| US-06 | 2-3 | 4 | Single session | Right-sized |
| US-07 | 1-2 | 3 | Single session | Right-sized |

### Verdict: PASS

All stories are 1-3 days with 3-5 UAT scenarios. No oversized stories.

---

## Overall Coherence Assessment: PASS

All 6 validation dimensions pass. The DISCUSS wave artifacts are ready for peer review and handoff.
