# Solution Testing -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: 3 -- Solution Testing
**Date**: 2026-03-31
**Status**: Test plan defined; MVP = the experiment

---

## Core Approach: MVP as Validation Instrument

In standard discovery, solution testing happens with prototypes before building. ASIA inverts this because:

1. Christian's primary validation channel is Asia's vet team -- they need something concrete to react to
2. A static mockup cannot demonstrate RAG quality -- the value IS the AI response quality
3. The MVP scope is deliberately minimal (one disease, one interface, five queries) -- it IS the prototype

**The MVP is the smallest testable thing.** It is not a product launch. It is an experiment.

---

## Hypotheses to Test

### H1: Value -- Vets find ASIA's answers accurate and clinically useful

```
We believe that providing RAG-synthesized answers about canine lymphoma
for Italian veterinarians will be perceived as accurate and clinically useful.

We will know this is TRUE when:
- 4 out of 5 critical queries receive "accurate" or "mostly accurate" ratings from vets
- At least 1 vet says they would use it for a real case
- Vets identify specific answers that would have changed/accelerated a past decision

We will know this is FALSE when:
- Vets find factual errors in the synthesis
- Vets say the answers are too superficial to be clinically useful
- Vets say they could find the same information faster through existing channels
```

**Test method**: Present MVP to Asia's vet team. Walk through the 5 critical queries. Collect structured feedback via questionnaire.

### H2: Usability -- A vet can get a useful answer in under 2 minutes

```
We believe that a veterinarian can type a clinical question and receive
a useful, well-cited answer within 2 minutes of first using ASIA.

We will know this is TRUE when:
- Vets complete the 5 critical query tasks without asking for help
- Time from query to "I have what I need" is under 2 minutes
- No vet asks "how do I use this?"

We will know this is FALSE when:
- Vets struggle to formulate queries
- Response time is too slow (>30 seconds perceived as broken)
- The answer format confuses rather than clarifies
```

**Test method**: Observe (or ask vets to self-report) task completion during MVP demo.

### H3: Trust -- Vets trust the citations and evidence grading enough to act on them

```
We believe that sentence-level citations, evidence grading, and disagreement
highlighting will build sufficient trust for vets to consider ASIA's output
in clinical decisions.

We will know this is TRUE when:
- Vets click through to source papers to verify (engagement signal)
- Vets rate trust at 3+ on a 1-5 scale
- Vets say the transparency (showing disagreement, evidence level) increases trust

We will know this is FALSE when:
- Vets say they would never trust AI for clinical decisions regardless of citations
- Vets find citation errors (wrong paper, wrong claim attribution)
- Vets say they need human expert validation before acting on any ASIA output
```

**Test method**: Questionnaire questions on trust + observation during demo.

### H4: Feasibility -- RAG can produce accurate Italian medical synthesis for vet oncology

```
We believe that a RAG pipeline over canine lymphoma literature can produce
synthesis in Italian that is factually accurate and uses correct medical terminology.

We will know this is TRUE when:
- 0 factual errors in the 5 critical query responses (verified by vet)
- Italian medical terminology is rated "natural" or "acceptable" by native speakers
- Citations map correctly to source claims (no citation hallucination)

We will know this is FALSE when:
- Hallucinated facts appear in responses (wrong dosages, wrong survival data)
- Italian medical language reads as "machine translated" or contains incorrect terms
- Citations reference papers that don't support the stated claim
```

**Test method**: Vet review of 5 critical query responses. This is the most important test -- a single wrong dosage could kill the project.

### H5: Language -- Italian synthesis adds value over reading English directly

```
We believe that Italian-language synthesis is a meaningful value-add,
not just a nice-to-have, for Italian veterinarians.

We will know this is TRUE when:
- Vets rate the Italian synthesis as "significantly easier" than reading English papers
- At least 1 vet says language was a barrier in past case management

We will know this is FALSE when:
- Vets say they read English fluently and the Italian adds no value
- Vets prefer to see the English original rather than the Italian synthesis
```

**Test method**: Questionnaire questions specifically about language value.

---

## The 5 Critical Queries (Acceptance Criteria)

These are the MVP's acceptance test. If ASIA answers these well, the MVP delivers value:

| # | Query (Italian) | Tests | Success Criteria |
|---|----------------|-------|-----------------|
| Q1 | "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?" | Protocol knowledge, evidence synthesis, Italian quality | Mentions CHOP, cites relevant papers, accurate remission rates |
| Q2 | "CHOP-19 vs CHOP-25: differenze negli outcome?" | Comparison, disagreement handling, structured output | Shows equivalence per European multicenter study, table format |
| Q3 | "Protocolli di rescue per recidiva precoce dopo CHOP?" | Depth of knowledge, multiple options | Lists Tanovea, LAP, LOPP, DMAC with evidence levels |
| Q4 | "Prognosi linfoma T-cell vs B-cell?" | Prognostic data extraction, nuance | B-cell better prognosis, specific survival data, staged |
| Q5 | "Aggiustamento dose doxorubicina per neutropenia?" | Micro-decision support, clinical practicality | Grade-specific guidance, delay vs reduce vs switch |

---

## Test Execution Plan

### Phase 3a: Pre-Demo Questionnaire (Before Seeing MVP)

Deploy the vet questionnaire (see interview-log.md) BEFORE the MVP demo. This captures:
- Current pain points (unbiased by seeing the solution)
- Current workflow and tools
- Language barrier reality
- Openness to AI tools

**Timeline**: Send questionnaire as soon as possible. Does not block MVP development.

### Phase 3b: MVP Demo with Asia's Vet Team

**Format**: Christian presents the MVP to Asia's veterinary team during a visit or appointment. He walks through the 5 critical queries and collects reactions.

**What to observe**:
- First reaction to the first answer (the "5-minute test")
- Do they lean in or lean back?
- Do they point out errors? Which kind?
- Do they ask follow-up questions (engagement signal)?
- Do they suggest other queries they would ask (adoption signal)?

**What to ask after**:
- "Was any of this information new to you, or did you already know all of it?"
- "If this had existed when we were diagnosing Asia, would it have changed anything?"
- "What is missing from these answers that you would need?"
- "Would you use this for your next oncology case?"

### Phase 3c: Post-Demo Structured Feedback

A short follow-up form (see interview-log.md, Part 3) that captures:
- Accuracy rating per query (1-5)
- Trust rating (1-5)
- Italian language quality rating (1-5)
- "Would you use this?" with commitment test (would you try it on your next case?)
- Open: what would make this genuinely useful for you?

---

## G3 Gate Assessment -- Adapted

Standard G3 requires 5+ users, >80% task completion. With 1 vet team (likely 2-4 vets), we adapt:

| Criterion | Standard Target | ASIA Adaptation | Minimum to Proceed |
|-----------|----------------|-----------------|-------------------|
| Users tested | 5+ | Asia's vet team (2-4 vets) | At least 2 vets provide feedback |
| Task completion | >80% | 5 critical queries answered correctly | 4 of 5 queries rated "accurate" |
| Value perception | >70% "would use" | At least 1 vet says "I would use this" | 1 genuine commitment signal |
| Usability | No blockers | Vets can use without instruction | No vet says "I don't understand how to use this" |
| Feasibility | Core flow works | RAG produces correct Italian synthesis | 0 factual errors in 5 queries |

### What counts as commitment signals (not just compliments):

- "Can you send me the link when it's ready?" (specific request)
- "I have a case right now where I would try this" (immediate use case)
- "Can I show this to my colleague at [other clinic]?" (referral)
- "Could it also do [X]?" (engagement with the product, not politeness)

### What counts as polite dismissal (not real validation):

- "Very interesting project!" (compliment, not commitment)
- "This could be useful" (future tense, no specificity)
- "Good idea" (opinion, not behavior)

---

## Risk Mitigation During Testing

| Risk | Mitigation |
|------|-----------|
| Hallucinated dosage in demo | Pre-verify all 5 critical query responses against literature before showing to vets |
| Bad Italian medical terminology | Have a native Italian speaker review responses before demo |
| Vet team too polite to give honest feedback | Frame it as "help me find errors" not "tell me if you like it" |
| Only 1-2 vets available | Sufficient for directional signal; plan for broader testing post-MVP |
| Vets don't fill out questionnaire | Keep it short (10-15 minutes). Christian hands it personally, does not email |
