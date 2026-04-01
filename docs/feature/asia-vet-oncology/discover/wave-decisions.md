# Wave Decisions -- ASIA Vet Oncology Discovery

**Feature ID**: asia-vet-oncology
**Started**: 2026-03-31
**Scout**: Product Discovery Facilitator
**Wave**: DISCOVER (complete, pending vet validation)

---

## Discovery State

```yaml
current_phase: "4"
phase_started: "2026-03-31"
interviews_completed:
  phase_1: 1 (founder as proxy)
  phase_2: 0
  phase_3: 0 (MVP demo pending)
  phase_4: 0
assumptions_tracked: 7
opportunities_identified: 10
decision_gates_evaluated:
  - G1: CONDITIONAL PROCEED (market evidence strong, vet confirmation pending)
  - G2: PROCEED (10 opportunities mapped, top 3 scored >14)
  - G3: TEST PLAN READY (MVP = experiment, 5 critical queries defined)
  - G4: PROCEED TO BUILD (Lean Canvas complete, no red risks)
artifacts_created:
  - docs/feature/asia-vet-oncology/discover/problem-validation.md
  - docs/feature/asia-vet-oncology/discover/opportunity-tree.md
  - docs/feature/asia-vet-oncology/discover/solution-testing.md
  - docs/feature/asia-vet-oncology/discover/lean-canvas.md
  - docs/feature/asia-vet-oncology/discover/interview-log.md
  - docs/feature/asia-vet-oncology/discover/wave-decisions.md
```

---

## Assumption Tracker (Updated)

| # | Assumption | Category | Impact (x3) | Uncertainty (x2) | Ease (x1) | Score | Priority | Status | Validation Method |
|---|-----------|----------|-------------|-------------------|-----------|-------|----------|--------|------------------|
| A1 | Italian vets managing oncology cases lack fast access to synthesized evidence | Value | 3 (9) | 2 (4) | 2 (2) | 15 | Test first | Partially validated | Market research confirms gap; questionnaire Q4-Q9 tests vet perception |
| A2 | Time-pressed vets will actually adopt a new AI tool | Value | 3 (9) | 3 (6) | 2 (2) | 17 | Test first | Untested | Questionnaire Q26-Q28 (commitment test); MVP demo reaction |
| A3 | English-language literature is a real barrier for Italian vets | Value | 2 (6) | 3 (6) | 1 (1) | 13 | Test first | Untested | Questionnaire Q10 |
| A4 | RAG synthesis with citations is the right solution form | Usability | 2 (6) | 2 (4) | 2 (2) | 12 | Test soon | Untested | MVP demo: 5 critical queries accuracy test |
| A5 | Canine lymphoma is the right starting scope | Value | 2 (6) | 1 (2) | 1 (1) | 9 | Test soon | Likely valid | Literature is rich; Asia's case provides motivation; scope is bounded |
| A6 | Open source matters to the target audience | Viability | 1 (3) | 2 (4) | 1 (1) | 8 | Test later | Untested | Not critical for MVP; matters for positioning |
| A7 | Asia's story creates brand resonance | Value | 1 (3) | 2 (4) | 1 (1) | 8 | Test later | Likely valid | Authentic origin; hard to test pre-launch |

### Uncertainty Changes from Market Research

- **A1 uncertainty dropped** from 3 to 2: Market research confirmed no tool serves this need. The gap is structural.
- **A5 uncertainty dropped** from 2 to 1: Literature analysis confirms rich corpus (500-1000 papers, 100-200 high quality). CHOP protocols well-documented. B-cell vs T-cell distinction is a perfect synthesis use case.

### Kill Risks (What Could Make Us Stop)

| Kill Risk | How We Would Detect It | Current Assessment |
|-----------|----------------------|-------------------|
| Hallucination produces wrong dosage | Vet review of 5 critical queries during demo | Unknown -- test during development |
| Italian medical language quality is unacceptable | Questionnaire Q22 + vet review | Unknown -- requires LLM benchmarking |
| Vets have adequate workarounds and feel no pain | Questionnaire Q7-Q8: if <15 min search and "not a problem" | Unlikely based on market evidence, but must verify |
| Zero willingness to change workflow | Questionnaire Q26: "No" from multiple vets | Unknown |
| Corpus completeness bias makes answers unreliable | Pre-verify 5 critical queries against known literature | Manageable -- abstracts are always available, full-text for OA papers |

---

## Key Decisions Made

| # | Decision | Rationale | Reversible? |
|---|----------|-----------|-------------|
| D1 | Build MVP before completing traditional 5-interview validation | Only 1 vet team accessible; MVP IS the validation instrument; scope is minimal | Yes -- stop if vet feedback is negative |
| D2 | Free for professionals, no pricing | Removes adoption barrier; aligns with open-source positioning; sustainability addressed separately | Yes -- could add premium tier later |
| D3 | Start with canine multicentric lymphoma only | Rich literature, high prevalence, concrete decision points, personal motivation (Asia's case) | Yes -- expand to other tumors post-validation |
| D4 | Approach A: Literature Intelligence (not Clinical Workflow Hub or Community Platform) | Fastest to build, sharpest value prop, validates core hypothesis with minimum complexity | Yes -- layer in Approach B features post-validation |
| D5 | Questionnaire instead of live interviews | Vets are time-pressed; form is lower friction; Christian prefers this approach | Partially -- live conversation captures more, but form is realistic |
| D6 | Italian questionnaire, English artifacts | Questionnaire in Italian for vet team; discovery artifacts in English for potential contributors | Yes |
| D7 | 5 critical queries as acceptance criteria | Concrete, testable, cover the key clinical scenarios for canine lymphoma | No -- these ARE the test |

---

## Validated / Invalidated Assumptions Summary

| Assumption | Status | Evidence |
|-----------|--------|----------|
| The niche is empty (no tool combines lit aggregation + AI + Italian + vet oncology) | **VALIDATED** | Market research: 6+ tools analyzed, none cover this quadrant |
| Canine lymphoma literature is rich enough for RAG | **VALIDATED** | 500-1000 papers estimated, 100-200 high quality, protocols well-documented |
| Regulatory risk is low | **VALIDATED** | Vet CDS software falls outside FDA/EU MDR scope (market research) |
| Technology stack is viable | **VALIDATED** | Python + FastAPI + pgvector + LangChain/LlamaIndex = standard RAG stack; Medical Graph RAG as reference |
| Vets feel the evidence access pain | **UNVALIDATED** | Inferred from market gap + founder experience; needs vet confirmation |
| Vets will adopt an AI tool | **UNVALIDATED** | No data; highest-risk assumption |
| English is a real barrier for Italian vets | **UNVALIDATED** | Assumed; questionnaire Q10 will test |
| RAG synthesis quality is sufficient for clinical use | **UNVALIDATED** | Requires MVP + vet review of 5 critical queries |
| Italian medical language from LLMs is acceptable | **UNVALIDATED** | Requires LLM benchmarking + vet review |

---

## Constraints Acknowledged

1. **Single validation channel**: Asia's vet team is the only accessible vet group. This means sample size of 2-4, not the standard 5-8. Discovery methodology adapted accordingly -- market research carries more weight than usual.

2. **MVP-as-experiment**: The build happens before traditional validation is complete. Risk is accepted because MVP scope is minimal and serves as the validation instrument.

3. **Solo founder**: No cross-functional team (PM + Designer + Engineer together). Christian is all three. Discovery is adapted for solo execution.

4. **No direct revenue model**: The project is free and open source. Viability is assessed differently -- sustainability through grants, partnerships, and low-cost architecture rather than traditional unit economics.

---

## Gate Summary

| Gate | Status | Key Condition |
|------|--------|---------------|
| G1: Problem Validation | CONDITIONAL PROCEED | Market evidence strong; vet confirmation pending via questionnaire |
| G2: Opportunity Mapping | PROCEED | 10 opportunities mapped; top 3 scored 14-16; job map covers 87.5% of steps |
| G3: Solution Testing | TEST PLAN READY | MVP = experiment; 5 critical queries defined; vet demo is the test |
| G4: Market Viability | PROCEED TO BUILD | Lean Canvas complete; no red risks; sustainability plan outlined |

---

## Phase Log

| Date | Phase | Action | Outcome |
|------|-------|--------|---------|
| 2026-03-31 | 1 | Discovery initiated, context loaded | Assumptions scored, ready for interviews |
| 2026-03-31 | 1 | Market research analyzed as Phase 1 evidence | Problem conditionally validated; niche confirmed empty |
| 2026-03-31 | 2 | Opportunity mapping from brainstorm + market research | 10 opportunities, top 3 scored 14-16, OST complete |
| 2026-03-31 | 3 | Solution test plan designed | MVP = experiment; 5 critical queries; vet demo plan |
| 2026-03-31 | 4 | Lean Canvas completed | All 9 boxes filled; 4 risks assessed; no reds |
| 2026-03-31 | ALL | Questionnaire designed (Italian, Mom Test principles) | Ready for Christian to deploy to vet team |
| 2026-03-31 | ALL | All discovery artifacts produced | 6 files in discover/ directory |

---

## Next Actions

1. **Immediate**: Christian deploys Part 1 of the questionnaire to Asia's vet team (before MVP development if possible)
2. **In parallel**: Begin MVP development (Approach A: Literature Intelligence)
3. **When MVP ready**: Demo to vet team, deploy Parts 2 and 3 of questionnaire
4. **After feedback**: Update all discovery artifacts with real vet evidence; re-evaluate gates
5. **If positive**: Proceed to DISCUSS wave -- hand off to product-owner with validated discovery package

---

## Handoff Requirements (When Ready)

Before handing off to product-owner in DISCUSS wave, the following must be true:

- [ ] Questionnaire Part 1 responses collected (at least 2 vets)
- [ ] MVP demo completed with vet team
- [ ] Questionnaire Parts 2+3 responses collected
- [ ] Problem validation updated with real vet evidence
- [ ] Assumption tracker updated with validation results
- [ ] Go/no-go decision documented based on vet feedback
- [ ] Peer review completed (if proceeding)

**Current status**: Discovery artifacts are complete and ready. Vet validation is the next critical step. The handoff is blocked on real customer evidence.
