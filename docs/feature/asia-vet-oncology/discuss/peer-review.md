# Peer Review -- ASIA Vet Oncology Requirements

**Review ID**: req_rev_20260401_001
**Reviewer**: product-owner (review mode)
**Artifact**: docs/feature/asia-vet-oncology/discuss/user-stories.md
**Iteration**: 1

---

## Strengths

1. **Strong problem grounding**: Every story traces to validated discovery artifacts (problem-validation.md, opportunity-tree.md). The persona is specific and consistent across all stories.

2. **Excellent domain examples**: All stories use real clinical data (CHOP-19, Sorenmo et al. 2020, Golden Retriever Luna, Dott.ssa Giulia Mancini). No generic data (user123 etc.).

3. **Emotional arc integration**: The journey from skeptical to satisfied is coherent and the error paths are well-designed to prevent trust damage.

4. **Citation accuracy as hard gate**: The emphasis on zero hallucinated citations as a kill criterion is appropriate for a medical context.

5. **Right-sized stories**: All 7 stories fit the 1-3 day / 3-5 scenario range. The walking skeleton is genuinely thin.

6. **Solution-neutral requirements**: Stories describe observable outcomes, not implementation details. Technical notes are clearly separated.

---

## Issues Identified

### Confirmation Bias

- **Issue**: All UAT scenarios assume Italian-language responses will be high quality. No scenario tests what happens if the LLM produces poor Italian medical terminology.
  - **Severity**: medium
  - **Location**: US-02, US-07
  - **Recommendation**: Add explicit UAT scenario: "Given the response uses a medical term incorrectly, When Dott.ssa Mancini reports it, Then..." -- or accept this as a @property test (already present in .feature file). Resolved: the @property scenario "Italian medical terminology quality" in the Gherkin file covers this. No action needed.

### Completeness Gaps

- **Issue**: No explicit NFR for response time threshold. The UAT says "within 5 seconds" for streaming start but no max time for complete response.
  - **Severity**: medium
  - **Location**: US-02
  - **Recommendation**: Add to AC: "Complete response delivered within 30 seconds for typical queries." Already present as @property in .feature file. Add to US-02 AC for completeness.

- **Issue**: Accessibility (WCAG) is mentioned in US-01 (touch targets) but not systematically across all stories.
  - **Severity**: low
  - **Location**: All stories
  - **Recommendation**: Acceptable for a demo to 1-3 vets. Flag for post-MVP if expanding to broader audience. Not blocking.

- **Issue**: No explicit data retention/privacy consideration for case data (patient names stored in PostgreSQL).
  - **Severity**: low
  - **Location**: US-06
  - **Recommendation**: For MVP demo, this is acceptable (no real patient data, demo context). Note for post-MVP: consider data protection for real clinical data. Not blocking.

### Clarity Issues

- **Issue**: Evidence level scoring algorithm (ALTO/MODERATO/BASSO) criteria not specified. How many studies / what study types qualify for each level?
  - **Severity**: medium
  - **Location**: US-02
  - **Recommendation**: This is a DESIGN wave decision (implementation detail). Requirements correctly stay solution-neutral by specifying that the level must be displayed. The algorithm belongs in architecture. Acceptable.

### Testability

- **Issue**: US-03 scenario "All 5 critical queries produce accurate responses" depends on vet verification -- not automatable.
  - **Severity**: low
  - **Location**: US-03
  - **Recommendation**: Acceptable. This is a human-verified acceptance test by design. The 5 critical queries ARE the acceptance criteria for the MVP. Not every scenario needs to be automatable.

### Priority Validation

- **Q1: Is this the largest bottleneck?** YES -- discovery artifacts confirm "fast access to synthesized evidence" is the #1 opportunity (score 16/20).
- **Q2: Were simpler alternatives considered?** YES -- opportunity tree shows S1b (static summaries) and S1c (FAQ) as alternatives; RAG was chosen because quality must be demonstrated live, not pre-computed.
- **Q3: Is constraint prioritization correct?** YES -- zero-cost constraint drives Groq free tier choice; demo-first constraint drives pre-loaded queries.
- **Q4: Is the approach data-justified?** YES -- market research (37 sources) confirms the niche is empty; opportunity scoring places top 3 at 14-16.

---

## Resolution Summary

| Issue | Severity | Resolution |
|-------|----------|------------|
| Italian quality scenario | Medium | Already covered by @property in .feature file. No action. |
| Response time NFR | Medium | Add "Complete response within 30 seconds" to US-02 AC. Minor edit. |
| Accessibility | Low | Acceptable for demo. Flag post-MVP. Not blocking. |
| Data retention | Low | Acceptable for demo. Flag post-MVP. Not blocking. |
| Evidence level algorithm | Medium | DESIGN wave decision. Requirements are correctly solution-neutral. |
| Non-automatable test | Low | By design -- human verification for medical accuracy. |

---

## Approval Status: APPROVED

- **Critical issues**: 0
- **High issues**: 0
- **Medium issues**: 3 (all resolved or acceptable)
- **Low issues**: 3 (all non-blocking)

The requirements package is approved for handoff to DESIGN wave. One minor edit recommended: add response time threshold to US-02 acceptance criteria.
