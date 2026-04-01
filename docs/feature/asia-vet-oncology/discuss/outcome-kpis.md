# Outcome KPIs: ASIA Vet Oncology MVP

---

## Objective

Demonstrate that ASIA delivers accurate, trustworthy, time-saving clinical evidence synthesis to Italian veterinarians managing canine lymphoma cases -- validated through a demo to Asia's vet team.

---

## Outcome KPIs

| # | Who | Does What | By How Much | Baseline | Measured By | Type |
|---|-----|-----------|-------------|----------|-------------|------|
| 1 | Vet using ASIA for first time | Rates the clinical query response as accurate | 4 of 5 critical queries rated >= 4/5 accuracy | No tool exists (baseline = 0 accurate AI responses) | Questionnaire Part 2, Q19 (accuracy rating per query) | Leading |
| 2 | Vet using ASIA for first time | Gets a useful answer in under 2 minutes from first interaction | <2 minutes from query to "I have what I need" | Current: 30-60+ minutes searching PubMed in English (questionnaire Q7) | Observation during demo + self-report | Leading |
| 3 | Vet evaluating ASIA | Trusts the response enough to consider it in clinical decisions | Trust rating >= 3/5 | No AI tool trusted for clinical decisions (baseline = 0) | Questionnaire Part 2, Q23 (trust rating) | Leading |
| 4 | Vet evaluating ASIA | Expresses genuine commitment to use ASIA for next oncology case | At least 1 vet gives a commitment signal (not just a compliment) | No tool adoption (baseline = 0) | Questionnaire Part 3, Q26-Q28 (commitment test) | Leading |
| 5 | Vet evaluating ASIA | Rates Italian medical terminology as natural or acceptable | 0 vets rate language as "mediocre" or "inaccettabile" | No Italian AI synthesis exists (baseline = English-only papers) | Questionnaire Part 2, Q22 (language quality) | Leading |
| 6 | Vet evaluating citations | Verifies that citations correspond to real, relevant papers | 0 hallucinated citations found across 5 critical queries | No RAG tool for vet oncology (baseline = N/A) | Vet review during demo + DOI link verification | Leading |

---

## Metric Hierarchy

- **North Star**: KPI #4 -- At least 1 vet commits to using ASIA for their next oncology case. This is the single metric that proves product-market fit at MVP scale.
- **Leading Indicators**: KPI #1 (accuracy), KPI #3 (trust), KPI #5 (language quality) -- these predict whether commitment will follow.
- **Guardrail Metrics**: KPI #6 (zero hallucinated citations) -- if this fails, nothing else matters. A single wrong dosage or fabricated paper kills the project.

---

## Measurement Plan

| KPI | Data Source | Collection Method | Frequency | Owner |
|-----|------------|-------------------|-----------|-------|
| 1. Accuracy rating | Questionnaire Part 2 | Structured form, Q19 | Once (demo) | Christian |
| 2. Time to answer | Demo observation | Stopwatch / self-report | Once (demo) | Christian |
| 3. Trust rating | Questionnaire Part 2 | Structured form, Q23 | Once (demo) | Christian |
| 4. Commitment signal | Questionnaire Part 3 | Structured form, Q26-Q28 | Once (demo) | Christian |
| 5. Language quality | Questionnaire Part 2 | Structured form, Q22 | Once (demo) | Christian |
| 6. Citation accuracy | Demo + vet review | Manual verification of DOIs and claims | Once (demo) | Christian + vet team |

---

## Hypothesis

We believe that providing RAG-synthesized, citation-backed answers in Italian for canine lymphoma queries will reduce the time vets spend finding evidence from hours to minutes, and build enough trust through verifiable citations for vets to consider ASIA in clinical decisions.

We will know this is true when at least 1 vet rates 4/5 queries as accurate (KPI #1), trusts the output at 3+/5 (KPI #3), and commits to trying it on their next case (KPI #4).

We will know this is false when vets find factual errors (KPI #6 fails), rate Italian as unacceptable (KPI #5 fails), or decline to use it for a real case (KPI #4 = 0).

---

## Kill Criteria

The project stops if ANY of these occur during the demo:

1. **Hallucinated citations**: Any fabricated paper or DOI found in the 5 critical query responses
2. **Factual error with clinical impact**: Wrong dosage, wrong survival data, wrong protocol recommendation
3. **Universal rejection**: All vets rate trust at 1-2/5 and none commit to trying it
4. **Language failure**: Italian rated "inaccettabile" by any vet

---

## Post-Demo KPIs (if validated)

These apply only after positive demo feedback, for ongoing measurement:

| # | Who | Does What | By How Much | Measured By |
|---|-----|-----------|-------------|-------------|
| 7 | Vet with access | Returns to ASIA within 7 days | >1 return visit per vet | Server access logs |
| 8 | Vet with access | Makes >2 queries per session | Average queries/session > 2 | Server query logs |
| 9 | Vet with access | Refers a colleague | >0 referrals | Self-report or new unique users |
