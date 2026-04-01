# Problem Validation -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: 1 -- Problem Validation
**Date**: 2026-03-31
**Status**: Conditionally validated (market evidence + founder experience; pending vet team feedback)

---

## Problem Statement (in customer words)

> "Le informazioni scientifiche piu aggiornate su diagnosi e terapie oncologiche veterinarie esistono, ma sono disperse, in inglese, e difficili da raggiungere rapidamente per un veterinario che ha un caso davanti."

Source: Christian's lived experience during Asia's diagnostic journey. The diagnostic phase was "very difficult because the case was complicated." He believes the tool could have made a difference in reaching a diagnosis faster.

---

## Evidence Assessment

### Evidence Source 1: Founder's Direct Experience (Past Behavior)

Christian experienced the problem firsthand as a pet owner navigating Asia's suspected mediastinal lymphoma with hypercalcemia. This is not hypothetical -- it is a completed experience with observable friction points:

- **Multiple visits and exams** over months before a mass was identified near the heart
- **Hypotheses overlapping** without a clear path to resolution
- **Delayed diagnosis** -- a radiograph eventually revealed the mass, but the path was long
- The veterinary team managing Asia's case went through exactly the workflow friction ASIA aims to solve

**Evidence strength**: Moderate. This is a single case from the owner's perspective, not the vet's. However, it confirms the problem exists in at least one real clinical scenario with a complicated case. The diagnostic complexity is consistent with published literature on mediastinal lymphoma (less common than multicentric, harder to diagnose).

### Evidence Source 2: Market Research (37 sources, March 2026)

The market research provides strong structural evidence:

| Finding | Source Count | Confidence |
|---------|-------------|------------|
| No tool combines literature aggregation + AI synthesis + Italian + vet oncology | 6+ tools analyzed | High |
| VIN knowledge trapped in unstructured forum threads | 2 sources | High |
| Plumb's lacks oncology protocol-level support | 3 sources | High |
| ImpriMed/FidoCure are lab-based, not literature-based | 3+ sources | High |
| No "UpToDate for veterinary medicine" exists globally | Cross-referenced | High |
| Italian vets (40,000) have zero Italian-language oncology decision support | Market data | Medium |
| AI in vet oncology scoping review (2025): 69 studies, focus on diagnostics not decision support | BMC Veterinary Research | High |

**Evidence strength**: Strong for "the niche is empty." Moderate for "vets feel this pain" (absence of a tool does not prove demand for one -- but the gap is remarkably clear).

### Evidence Source 3: Brainstorm Analysis (40 ideas)

The brainstorm surfaced specific workflow pain points that map to the problem:

1. **Search friction**: PubMed is designed for researchers, not clinicians under time pressure
2. **Synthesis burden**: Reading dozens of abstracts in English to extract relevant information
3. **Protocol comparison**: Scattered across papers, metrics not directly comparable
4. **Micro-decision urgency**: During chemotherapy (neutropenia management, dose adjustments), vets need evidence-based answers in minutes, not hours
5. **Owner communication**: 15-20 minutes per case explaining protocols, prognosis, side effects
6. **Mental translation**: English literature to Italian clinical decision, under time pressure

**Evidence strength**: These are inferred pain points, not interview-confirmed. But they are specific enough to test with the questionnaire.

### Evidence Source 4: Analogous Domain Evidence

UpToDate in human medicine has become the gold standard (9,400+ GRADE recommendations, used globally). Its success validates the core hypothesis that clinicians need synthesized, graded evidence rather than raw literature. The fact that no veterinary equivalent exists after 30+ years of UpToDate's success is itself a signal -- either the market is too small, or the problem is underserved.

ImpriMed's commercial success (lab-based canine lymphoma AI, 3x survival improvement claims) validates that veterinary oncology decision support has market pull -- just not in the literature synthesis form yet.

**Evidence strength**: Moderate. Analogous markets suggest the pattern works, but veterinary medicine has different economics (smaller market, lower budgets, different workflow patterns).

---

## G1 Gate Assessment -- Adapted

Standard G1 requires 5+ interviews with >60% confirmation. We do not have interviews yet. Instead, we assess readiness using available evidence:

| Criterion | Standard Target | ASIA Status | Assessment |
|-----------|----------------|-------------|------------|
| Problem confirmation | >60% of 5+ interviewees | 0 interviews; strong market evidence | PARTIAL -- market evidence confirms gap exists; vet pain confirmation pending |
| Frequency | Weekly+ | Inferred: every oncology case (vets see multiple per month) | LIKELY -- but unvalidated |
| Current spending on workarounds | >$0 | VIN subscription, PubMed time, colleague consultations | LIKELY |
| Emotional intensity | Frustration evident | Christian's experience: "very difficult" | PARTIAL -- owner perspective, not vet perspective |
| Problem in customer words | 3+ examples | Vision doc captures it; not yet from vet mouths | PENDING |

### G1 Decision: CONDITIONAL PROCEED

**Rationale**: The market evidence is unusually strong for a pre-interview stage. The niche is verifiably empty. The analogous domain (UpToDate) validates the pattern. The founder has direct experience with the problem. However, we have zero direct vet confirmation.

**Condition**: The vet team questionnaire (see interview-log.md) must be deployed before or alongside MVP development. The MVP itself serves as the primary validation instrument. If vet feedback contradicts the problem hypothesis, we pivot or kill before investing further.

**What would make us kill the project at this stage**:
- Vets say: "We have adequate workarounds and don't feel this friction"
- Vets say: "We wouldn't trust an AI tool for clinical decisions, period"
- Zero engagement with the questionnaire (apathy signal)

---

## Validated Problem Dimensions

| Dimension | Evidence Level | Source |
|-----------|---------------|--------|
| Information is scattered across papers | Strong (structural) | Market research: 6 tools analyzed, none aggregate |
| Synthesis is manual and time-consuming | Moderate (inferred) | Brainstorm analysis, UpToDate analogy |
| English is a barrier for Italian vets | Weak (assumed) | No direct vet confirmation yet; questionnaire will test |
| Micro-decisions during chemo need fast answers | Moderate (inferred) | Clinical workflow analysis, brainstorm ideas 2 and 6 |
| No tool exists for this job | Strong (verified) | Market research: comprehensive competitive scan |

---

## Open Questions for Vet Team

These are embedded in the questionnaire (interview-log.md) and will determine whether we have a real problem or a perceived one:

1. When a vet last managed a complex oncology case, what was their information-seeking behavior? (Past behavior, not future intent)
2. How much time do they spend per case on literature review? Is it "annoying but manageable" or "a real bottleneck"?
3. Do they use VIN, Plumb's, or other tools? What do they wish those tools did better?
4. Is English a real barrier, or do most Italian oncology vets read English fluently?
5. Would they trust an AI-synthesized answer enough to influence clinical decisions?

---

## Risk: Building Before Validating

Christian's approach (build MVP, then present to vets) inverts the standard discovery sequence. This is a calculated risk:

**Upside**: A working demo is far more compelling than a pitch. Vets can react to something concrete. The "first five minutes" test is the real validation.

**Downside**: If the problem hypothesis is wrong, development effort is wasted. If the solution form (RAG query) is wrong, the MVP validates nothing.

**Mitigation**: The questionnaire goes out in parallel with development. If early signals are negative, we can stop before the MVP is complete. The MVP scope is deliberately minimal (one interface, one disease, five critical queries) to limit waste.
