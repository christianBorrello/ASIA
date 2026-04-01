# KPI Instrumentation -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## 1. Context

The 6 outcome KPIs from `discuss/outcome-kpis.md` are measured primarily through a **one-time demo** with 1-3 veterinarians, using questionnaires and observation. There is no production traffic to measure. Instrumentation therefore focuses on:

- Application-side data collection that supports demo observation
- Log events that provide backup evidence for timing and accuracy claims
- A lightweight post-demo data structure for recording results

---

## 2. KPI Instrumentation Matrix

### KPI #1: Accuracy Rating (4/5 queries rated >= 4/5)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Questionnaire Part 2, Q19 (manual, paper/digital form) |
| **Application support** | None required -- vets rate accuracy after reading the response |
| **Backup data** | Log event `query.completed` with `evidence_level` and `citation_count` provides context if accuracy disputes arise |
| **Demo preparation** | Pre-run the 5 critical queries and record expected outputs for comparison |

### KPI #2: Time to Answer (< 2 minutes)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Observation during demo + vet self-report |
| **Application support** | Log event `query.completed` records `total_ms` (pipeline time). Frontend could display "Risposta in X secondi" after completion. |
| **Instrumentation** | The `total_ms` field in `query.completed` log events captures end-to-end pipeline time. The `case_queries.response_time_ms` database column persists this per query. |
| **Backup data** | Query `case_queries` table after demo: `SELECT query_text, response_time_ms FROM case_queries ORDER BY created_at` |
| **Note** | "2 minutes" includes vet reading time, not just pipeline time. Pipeline target is < 30s. The remaining ~90s is reading + comprehension. |

### KPI #3: Trust Rating (>= 3/5)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Questionnaire Part 2, Q23 (manual) |
| **Application support** | The transparency note (citation removal notification) is a trust-building UX element logged via `verification.citation_removed` |
| **Supporting data** | Count of `verification.result` events with `status: SUPPORTA` vs total -- higher verification rate correlates with trustworthiness |

### KPI #4: Commitment Signal (North Star)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Questionnaire Part 3, Q26-Q28 (manual) |
| **Application support** | None -- this is a behavioral/intent metric captured via interview |
| **Supporting context** | If a vet asks to try their own clinical case during the demo (not a pre-loaded query), log that as organic engagement via `query.received` with `has_context: true` |

### KPI #5: Italian Language Quality (0 "mediocre"/"inaccettabile" ratings)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Questionnaire Part 2, Q22 (manual) |
| **Application support** | None -- language quality is subjective, assessed by native speakers |
| **Demo preparation** | Pre-review the 5 critical query responses with a native Italian speaker before the demo |

### KPI #6: Citation Accuracy (0 hallucinated citations -- Guardrail)

| Aspect | Design |
|--------|--------|
| **Primary measurement** | Vet manual verification during demo + DOI link checking |
| **Application support** | Every citation includes a clickable DOI link. The source panel shows author, year, journal, study type for quick verification. |
| **Instrumentation** | `verification.result` log events record SUPPORTA/PARZIALE/NON_SUPPORTA for each citation. `verification.citation_removed` logs any citation that failed self-reflective check. |
| **Backup data** | `case_queries.response_citations` JSONB stores all citations with DOIs and verification status. Query after demo: `SELECT response_citations FROM case_queries` |
| **Pre-demo validation** | Run all 5 critical queries and manually verify every DOI resolves to a real paper that supports the claim. Document results. |

---

## 3. Demo Data Collection Checklist

Before the demo:

- [ ] Pre-run 5 critical queries, verify all DOIs, document expected outputs
- [ ] Prepare printed/digital questionnaire (Parts 1-3)
- [ ] Test `docker compose logs -f api` filtering for post-demo analysis
- [ ] Verify `case_queries` table is capturing `response_time_ms` and `response_citations`

During the demo:

- [ ] Start screen recording (backup for timing observation)
- [ ] Note which queries each vet runs (pre-loaded vs. free-form)
- [ ] Time from query submission to "I have what I need" (KPI #2)
- [ ] Note any DOI clicks and verification attempts (KPI #6)
- [ ] Capture vet reactions to transparency notes (KPI #3 supporting data)

After the demo:

- [ ] Collect completed questionnaires
- [ ] Export query logs: `docker compose logs api --no-log-prefix > demo-logs.json`
- [ ] Export query history: SQL query on `case_queries` table
- [ ] Score each KPI against target

---

## 4. Post-Demo Results Template

```markdown
# Demo Results -- ASIA Vet Oncology MVP

**Date**: ____
**Vets present**: ____
**Duration**: ____

## KPI Results

| # | KPI | Target | Result | Status |
|---|-----|--------|--------|--------|
| 1 | Accuracy rating | 4/5 queries >= 4/5 | __/5 queries at __/5 | PASS/FAIL |
| 2 | Time to answer | < 2 min | Avg: __ seconds | PASS/FAIL |
| 3 | Trust rating | >= 3/5 | Avg: __/5 | PASS/FAIL |
| 4 | Commitment signal | >= 1 vet commits | __ vets committed | PASS/FAIL |
| 5 | Language quality | 0 "mediocre"/"inaccettabile" | __ negative ratings | PASS/FAIL |
| 6 | Citation accuracy | 0 hallucinated | __ hallucinated found | PASS/FAIL |

## Kill Criteria Check

- [ ] No hallucinated citations (KPI #6)
- [ ] No factual errors with clinical impact
- [ ] Not all vets rejected (universal rejection test)
- [ ] No "inaccettabile" language rating (KPI #5)

## Pipeline Performance (from logs)

| Metric | Value |
|--------|-------|
| Avg response time (pipeline) | __ ms |
| Avg retrieval similarity score | __ |
| Citation verification rate (SUPPORTA) | __% |
| Citations removed by self-reflection | __ |

## Qualitative Notes

(Vet reactions, questions asked, suggestions made)
```

---

## 5. Post-MVP KPI Instrumentation

If the demo validates the MVP (KPI #4 passes), these post-demo KPIs require server-side instrumentation:

| KPI | Instrumentation |
|-----|----------------|
| #7 Return visits within 7 days | Add `query.received` log aggregation by unique session/IP per day |
| #8 Queries per session | Add session tracking (cookie or simple session ID) and count queries per session |
| #9 Referrals | Self-report only (no application instrumentation) |

These are deferred. Do not build session tracking or analytics for MVP.
