# Lean Canvas -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: 4 -- Market Viability
**Date**: 2026-03-31
**Status**: Draft from market research evidence (viability risks documented)

---

## Lean Canvas

### 1. Problem (Phase 1 Validated -- Conditionally)

**Top 3 problems**:

1. **Scattered evidence**: Veterinary oncology literature is dispersed across hundreds of papers, in English, on platforms designed for researchers not clinicians. No synthesis layer exists.

2. **Time-critical decisions without support**: During chemotherapy, vets face micro-decisions (dose adjustments, side effect management, rescue protocol selection) where they need evidence-based answers in minutes, not hours.

3. **Language and translation burden**: Italian vets must mentally translate English papers into Italian clinical decisions under time pressure, with no tool supporting this.

**Existing alternatives**: PubMed (researcher tool, no synthesis), VIN (forum, unstructured), Plumb's (drug reference, no oncology protocols), colleague consultation (slow, availability-dependent).

---

### 2. Customer Segments (by Job-to-Be-Done)

**Primary JTBD**: "When I have a canine oncology case, help me find the best evidence-based treatment approach quickly, in a language I think in."

| Segment | Size | Urgency | Access |
|---------|------|---------|--------|
| Italian vets managing oncology cases | Subset of ~40,000 Italian vets | High (active cases) | Hard -- no direct channel yet |
| Italian vet oncology specialists | Small (maybe 100-200) | Medium (they know the literature) | Medium -- via conferences, SIONCOV |
| Vet students at Italian faculties | ~5,000/year across faculties | Medium (learning, not treating) | Easier -- via faculty partnerships |
| International vets (non-English speaking) | Large (hundreds of thousands) | Medium | Future -- multilingual expansion |

**Early adopter profile**: Italian veterinarian who has managed at least one complex oncology case in the past year and felt the friction of literature access. Likely works in a general practice (not a specialty referral center with oncologists on staff).

---

### 3. Unique Value Proposition

**Single clear message**:

> ASIA: la letteratura oncologica veterinaria, sintetizzata in italiano, con citazioni verificabili. Il primo "UpToDate" open source per l'oncologia veterinaria.

(ASIA: veterinary oncology literature, synthesized in Italian, with verifiable citations. The first open-source "UpToDate" for veterinary oncology.)

**Key differentiators**:
- Only tool combining literature aggregation + AI synthesis + Italian + open source
- Citation-level transparency (sentence-level, not paper-level)
- Shows disagreement honestly (builds trust through transparency)
- Free and open source (auditable in a clinical context)

---

### 4. Solution (Top 3 Features for Top 3 Problems)

| Problem | Feature | MVP? |
|---------|---------|------|
| Scattered evidence | RAG-powered clinical query with citation-backed synthesis in Italian | Yes |
| Protocol comparison burden | Auto-generated protocol comparison tables | Yes (in response format) |
| Micro-decision urgency | Same RAG handles complication queries; dedicated Complication Advisor post-MVP | Partial |

**MVP is one thing**: A single query interface that returns synthesized, cited answers in Italian for canine lymphoma questions.

---

### 5. Channels (Path to Customers)

| Channel | Viability | Effort | Timeline |
|---------|-----------|--------|----------|
| Asia's vet team (direct) | Validated (Christian has access) | Low | Immediate |
| Italian vet faculties (Bologna, Milan, Turin) | Promising (aligned interest: teaching tool) | Medium | 3-6 months post-MVP |
| SIONCOV (Italian Veterinary Oncology Society) | Unknown | Medium | 6-12 months |
| Italian vet conferences (SCIVAC) | Unknown | Medium | Event-dependent |
| Open source community (GitHub) | Uncertain for vet audience | Low | Passive |
| WhatsApp/Telegram vet groups | Promising (Italian vets use WhatsApp heavily) | Low-Medium | Post-MVP |
| Word of mouth from early users | Highest potential, lowest control | Zero | Depends on product quality |

**Primary channel for validation**: Asia's vet team. Period. Everything else is post-validation.

**Biggest channel risk**: Christian has no broad access to Italian vets. Faculty partnerships are the most promising scalable channel but require credibility (which the MVP + vet team endorsement would provide).

---

### 6. Revenue Streams

**ASIA is free for professionals.** This is a deliberate choice, not a gap. It removes pricing barriers and aligns with the open-source positioning.

**Sustainability options** (not revenue per se):

| Option | Feasibility | Notes |
|--------|-------------|-------|
| EU research grants (Horizon Europe) | Medium | "One Health" and digital health are funded areas |
| Italian digital health grants | Medium | Italy has digitalization funding programs |
| University partnerships (tool hosting) | Medium | Faculties could host and contribute |
| Donations / sponsorships | Low initially | Requires user base |
| Hosted premium tier (e.g., team features, API) | Future | Only viable with significant user base |
| Comparative oncology research grants (NCI) | Speculative | ASIA's data could support One Health research |

**Honest assessment**: Sustainability is a real risk. The project can run on volunteer effort and minimal server costs for MVP and early adoption. Scaling requires external funding. This is typical for open-source medical tools.

---

### 7. Cost Structure

| Cost | MVP Phase | Growth Phase |
|------|-----------|--------------|
| LLM API calls | Low (~$20-50/month for low traffic) | Medium-High (scales with usage) |
| Server hosting | Low (~$20-50/month for small deployment) | Medium |
| Christian's time | High (unpaid, personal project) | Unsustainable without funding |
| Domain + infrastructure | Minimal | Minimal |
| Corpus maintenance (paper ingestion) | Low (automated) | Low (automated) |

**Key insight**: The MVP is financially viable as a personal project. Growth requires either keeping costs ultra-low (local LLMs, efficient RAG) or finding external funding.

---

### 8. Key Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Query accuracy (vet-verified) | Value: are answers correct? | >80% rated accurate |
| Return visits per vet | Adoption: do they come back? | >3 visits per vet in first month |
| Queries per session | Engagement: is it useful beyond first try? | >2 queries per session |
| Time to answer | Usability: is it fast enough? | <30 seconds response time |
| Referral rate | Growth: do vets tell colleagues? | >0 (any referral = strong signal) |
| Error rate (vet-reported) | Trust: how often is ASIA wrong? | <5% of answers have errors |

---

### 9. Unfair Advantage (Not Easily Copied)

| Advantage | Defensibility |
|-----------|---------------|
| Asia's story (authentic origin) | Cannot be replicated -- it's personal |
| First mover in empty niche | Moderate -- niche is small, competitors may not bother |
| Open source (community contributions over time) | Grows with adoption |
| Italian medical language expertise (built into corpus + prompts) | Hard to replicate without domain effort |
| Vet-verified answers accumulating over time | Network effect (weak but real) |

**Honest assessment**: The unfair advantage is thin. The real moat is being first in a niche that is too small for big players to care about, and building community trust over time. If ASIA proves the concept, a well-funded competitor could build something better. The defense is open source: you can't out-compete free.

---

## 4 Big Risks Assessment

| Risk | Status | Evidence | Mitigation |
|------|--------|----------|-----------|
| **Value**: Will vets want this? | Yellow | Market gap is clear; vet demand unconfirmed | Questionnaire + MVP demo with vet team |
| **Usability**: Can vets use this? | Yellow | Interface is simple (one query box); Italian quality untested | Task completion test during demo |
| **Feasibility**: Can we build this? | Green | RAG technology is mature; canine lymphoma corpus is rich; tech stack is standard | Technical spike on critical queries |
| **Viability**: Sustainable model? | Yellow | Free product, no revenue; server costs real but low | EU grants, faculty partnerships, low-cost architecture |

**Overall**: No red risks. Feasibility is the strongest (the technology works). Value is the biggest unknown (will vets actually use it?). Viability is acceptable for a personal open-source project but needs a plan for scale.

---

## G4 Gate Assessment -- Adapted

| Criterion | Standard Target | ASIA Status | Assessment |
|-----------|----------------|-------------|------------|
| Lean Canvas complete | All 9 boxes filled | Complete | PASS |
| 4 big risks addressed | All green/yellow | 1 green, 3 yellow | PASS (no reds) |
| Channel validated | 1+ viable | Asia's vet team (confirmed) | PASS (minimal) |
| Unit economics | LTV > 3x CAC | N/A (free product) | ADAPTED -- costs low enough for personal project |
| Stakeholder sign-off | Required | Solo founder -- Christian decides | PASS (implicit) |

### G4 Decision: PROCEED TO BUILD MVP

With the understanding that:
1. The vet questionnaire MUST go out before or alongside development
2. The MVP demo IS the primary validation event
3. Sustainability planning begins after validation, not before
4. If vet feedback is negative, we stop
