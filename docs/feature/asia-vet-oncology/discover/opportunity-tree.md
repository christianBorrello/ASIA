# Opportunity Solution Tree -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: 2 -- Opportunity Mapping
**Date**: 2026-03-31
**Status**: Mapped from market research + brainstorm evidence (pending vet validation)

---

## Desired Outcome

**Minimize the time it takes for an Italian veterinarian to access synthesized, evidence-based information for oncology clinical decisions.**

---

## Job Map: Managing a Veterinary Oncology Case

| Step | Job | Current Experience | Pain Level |
|------|-----|-------------------|------------|
| Define | Identify what type of cancer the animal has | Complex: requires cytology, histopathology, immunophenotyping, staging. Asia's case took months | High |
| Locate | Find relevant scientific literature for this case | PubMed search in English, read abstracts, no clinical filtering | High |
| Prepare | Synthesize findings into actionable clinical knowledge | Manual: read papers, mentally translate, compare protocols | High |
| Confirm | Verify that chosen protocol is supported by evidence | Cross-reference multiple papers, check for contradictions | Medium |
| Execute | Administer treatment protocol | Well-defined once protocol is chosen (CHOP schedules are clear) | Low |
| Monitor | Track response and manage complications | Micro-decisions on dose adjustments, side effects need fast answers | High |
| Modify | Adjust treatment if relapse or complications | Rescue protocol selection requires literature review again | High |
| Conclude | Communicate outcomes and prognosis to owner | 15-20 min per case explaining in Italian; no tool support | Medium |

---

## Opportunity Scoring

**Formula**: Score = Importance + Max(0, Importance - Satisfaction)

Scores are estimated from market research and founder experience. They will be refined with vet questionnaire data.

| # | Opportunity | Importance (1-10) | Satisfaction (1-10) | Score | Action |
|---|-------------|-------------------|---------------------|-------|--------|
| O1 | Fast access to synthesized evidence for a specific case | 9 | 2 | 16 | Pursue |
| O2 | Evidence-based micro-decision support during chemo (side effects, dose adjustments) | 9 | 2 | 16 | Pursue |
| O3 | Protocol comparison with structured outcome data | 8 | 2 | 14 | Pursue |
| O4 | Literature in Italian (or synthesized into Italian) | 7 | 1 | 13 | Evaluate |
| O5 | Rescue protocol guidance after relapse | 8 | 3 | 13 | Evaluate |
| O6 | Prognostic data structured by subtype/stage | 8 | 3 | 13 | Evaluate |
| O7 | Owner communication support | 6 | 2 | 10 | Evaluate |
| O8 | Monitoring schedule generation per protocol | 6 | 3 | 9 | Evaluate |
| O9 | New evidence alerts for active cases | 5 | 1 | 9 | Evaluate |
| O10 | Open source / auditability of answers | 5 | 1 | 9 | Evaluate |

**Note on scoring**: Satisfaction scores are uniformly low because no tool currently serves these jobs for Italian vet oncology. Importance scores are estimated. The questionnaire includes questions to validate both dimensions.

---

## Opportunity Solution Tree

```
Desired Outcome: Minimize time for Italian vets to access synthesized oncology evidence
|
+-- O1: Fast synthesized evidence for specific case [16] *** TOP PRIORITY
|     +-- S1a: RAG-powered clinical query in Italian (MVP core)
|     +-- S1b: Pre-computed protocol summaries (static, no AI)
|     +-- S1c: Curated FAQ database for top 20 clinical questions
|
+-- O2: Micro-decision support during chemo [16] *** TOP PRIORITY
|     +-- S2a: Complication Advisor module (post-MVP)
|     +-- S2b: Side effect decision trees (pre-indexed)
|     +-- S2c: Quick-reference dosing cards with evidence links
|
+-- O3: Protocol comparison with outcome data [14] *** TOP PRIORITY
|     +-- S3a: Auto-generated comparison tables from literature (MVP feature)
|     +-- S3b: Static curated comparison table (manually maintained)
|     +-- S3c: Interactive protocol selector wizard
|
+-- O4: Italian-language synthesis [13]
|     +-- S4a: LLM synthesis in Italian with medical terminology QA
|     +-- S4b: Bilingual mode (English source + Italian summary)
|
+-- O5: Rescue protocol guidance [13]
|     +-- S5a: Dedicated rescue protocol query path in RAG
|     +-- S5b: Decision tree: "relapse after X, try Y"
|
+-- O6: Prognostic data by subtype/stage [13]
|     +-- S6a: Structured prognostic data extraction in RAG responses
|     +-- S6b: Static prognostic tables from meta-analyses
|
+-- O7: Owner communication support [10]
|     +-- S7a: Owner Communication Generator (post-MVP)
|
+-- O8: Monitoring schedule per protocol [9]
|     +-- S8a: Auto-generated monitoring checklists (post-MVP)
|
+-- O9: New evidence alerts [9]
|     +-- S9a: Literature monitoring with notification (Phase C)
|
+-- O10: Auditability / open source [9]
|     +-- S10a: Full source visibility in every answer
|     +-- S10b: Open-source codebase (Apache 2.0)
```

---

## Top 3 Opportunities for MVP

### 1. O1: Fast Synthesized Evidence (Score: 16)

**Solution chosen**: S1a -- RAG-powered clinical query in Italian.

This is the core MVP. One interface, one input field, one synthesized answer with citations. The "first five minutes" test hinges entirely on this.

**Hypothesis**: We believe that providing RAG-synthesized, citation-backed answers in Italian for canine lymphoma queries will reduce the time vets spend finding evidence from hours to minutes. We will know this is TRUE when vets report the answers are accurate, well-cited, and clinically useful. We will know this is FALSE when vets say the answers are inaccurate, superficial, or not trustworthy enough to influence decisions.

### 2. O3: Protocol Comparison Tables (Score: 14)

**Solution chosen**: S3a -- Auto-generated comparison tables from literature.

This is the highest-value "tangible output" -- a vet can see CHOP-19 vs CHOP-25 vs COP side by side with remission rates, survival data, evidence level. No tool does this today. Can be part of the MVP RAG response format.

**Hypothesis**: We believe that auto-generated protocol comparison tables will be the single most valued output of ASIA. We will know this is TRUE when vets cite the tables as a reason to return. We will know this is FALSE when vets say they already know this information or the tables add no value.

### 3. O2: Micro-Decision Support During Chemo (Score: 16)

**Solution chosen for MVP**: Addressed through S1a (the core RAG handles complication queries like "neutropenia after doxorubicin, what to do?"). Dedicated Complication Advisor (S2a) is post-MVP.

**Hypothesis**: We believe that vets managing active chemo cases will use ASIA for urgent micro-decisions on side effects and dose adjustments. We will know this is TRUE when the query logs show complication-related queries during active treatment. We will know this is FALSE when vets only use ASIA for initial protocol selection and never return during treatment.

---

## G2 Gate Assessment -- Adapted

| Criterion | Standard Target | ASIA Status | Assessment |
|-----------|----------------|-------------|------------|
| Opportunities identified | 5+ distinct | 10 identified | PASS |
| Top scores | >8 (max 20) | Top 3: 16, 16, 14 | PASS |
| Job step coverage | 80%+ | 7 of 8 job steps addressed | PASS (87.5%) |
| Team alignment | Confirmed | Solo founder; alignment implicit | N/A (adapted) |

### G2 Decision: PROCEED

The opportunity space is clear. The top opportunities score high because satisfaction is near zero (no tool exists). The key uncertainty is whether Importance scores hold up when validated with actual vets -- the questionnaire will test this.
