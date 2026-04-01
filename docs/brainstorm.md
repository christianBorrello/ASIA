# Brainstorm: ASIA (Aggregated Scientific Intelligence for Animals)

**Date**: 2026-03-31
**Status**: exploring

---

## Problem Statement

Veterinarians managing oncology cases lack a fast, Italian-language tool to access synthesized evidence from scattered English-language literature. The gap is not just linguistic -- it is workflow-level: the existing tools (PubMed, Google Scholar, Plumb's, VetCompanion) are built for researchers, not clinicians under time pressure with an anxious pet owner in front of them. ASIA aims to be a RAG-powered clinical intelligence layer, starting with canine lymphoma.

---

## Research Findings

### Competitive Landscape

- **ImpriMed** -- AI-driven personalized treatment for canine lymphoma using live cell drug sensitivity testing. Claims 3x longer survival in relapsed B-cell lymphoma. Lab-based, not literature-based. Expensive, US-focused.
- **FidoCure** -- Genomic sequencing + AI for personalized canine cancer treatment. Next-gen sequencing approach. US-focused, proprietary.
- **Plumb's Veterinary Drugs** -- Drug dosing reference. Not oncology-specific. Not evidence-synthesis.
- **VetCompanion** -- Clinical decision support. Broad, not deep in oncology.
- **PubMed/Google Scholar** -- Research tools, not clinical tools. No synthesis, no Italian.

**Key gap ASIA fills**: None of the above combines (a) literature aggregation, (b) AI synthesis, (c) Italian language, (d) open source. ASIA occupies an empty quadrant.

### Comparative Oncology is a Massive Opportunity

- NCI's Comparative Oncology Program runs a 20-center consortium studying dog cancers as human cancer models.
- Canine non-Hodgkin lymphoma is a validated model for human NHL.
- Drugs like ibrutinib, acalabrutinib, and selinexor were developed using canine cancer data.
- The "One Health, One Medicine" paradigm is gaining traction in research funding.

### Canine Lymphoma Literature is Rich

- CHOP-19 and CHOP-25 are well-documented standard protocols with 80-90% remission rates.
- Multiple rescue protocols exist (Tanovea, LAP, LOPP, DMAC, dacarbazine, temozolomide).
- Recent European multicenter studies confirm CHOP-19 vs CHOP-25 equivalence.
- B-cell vs T-cell distinction drives prognosis and protocol selection -- a perfect use case for evidence synthesis.

### Italian Market Context

- Italy has ~40,000 veterinarians and a strong pet culture (high emotional attachment to companion animals).
- No Italian-language veterinary oncology decision support tool exists.
- Language barrier to English literature is real and underserved.
- Italy has strong veterinary faculties (Bologna, Milan, Turin, Naples) that could become allies.

---

## Ideas Generated

### Theme 1: Overlooked User Needs -- The Real Clinical Workflow

1. **"Case Mode" not just "Query Mode"** -- A vet doesn't ask one question. They manage a *case* over weeks/months. ASIA could let vets create a persistent case (breed, age, staging, immunophenotype, treatment history) and ask sequential questions in context. "Asia, we started CHOP-19 three weeks ago and the patient relapsed. What rescue protocols show best outcomes for early relapsers?" The system remembers the case context.

2. **Side Effect Decision Trees** -- During chemo, vets face constant micro-decisions: "The dog has grade 2 neutropenia after doxorubicin. Do I delay? Reduce dose? Switch drug?" This is where evidence-based answers have the highest urgency. A dedicated "complication advisor" module, pre-indexed on side effect management literature, could be the most-used feature.

3. **Owner Communication Generator** -- After the vet decides on a protocol, they need to explain it to the owner. Generate a clear, empathetic explanation in Italian: what the treatment involves, expected timeline, side effects, costs, prognosis -- all calibrated to the specific case. This saves 15-20 minutes per case and reduces miscommunication.

4. **Prognostic Context** -- Vets don't just want "what protocol to use." They want: "If I choose CHOP-19 for this Stage IIIa B-cell lymphoma, what's the typical first remission duration? What percentage relapse within 6 months? What's the median survival?" Structured prognostic data extraction from literature would be transformative.

5. **Cost-Effectiveness Lens** -- Italian vet clinics are often small. Owners have budget limits. Being able to filter or compare protocols by cost (drug costs, visit frequency, monitoring requirements) is a real-world need that academic literature almost never addresses but practitioners desperately want.

6. **"What Would You Monitor?" Checklist** -- For each protocol, auto-generate a monitoring schedule: blood work timing, imaging intervals, expected lab values, red flags. This is operational, not just intellectual.

### Theme 2: Killer Features -- From Nice-to-Have to Can't-Live-Without

7. **Protocol Comparison Table (Auto-Generated)** -- Not buried in a paper. A real table: CHOP-19 vs COP vs single-agent doxorubicin. Columns: drugs, doses, schedule, remission rate, median survival, cost tier, evidence level. Generated from literature, not manually curated. This alone could justify ASIA's existence.

8. **"New Evidence Alert" for Active Cases** -- If a vet has an active lymphoma case and a new paper comes out on a relevant protocol or drug, ASIA notifies them. Passive intelligence. This creates stickiness -- the vet keeps ASIA open because it watches the literature for them.

9. **Confidence Scoring with Disagreement Highlighting** -- When papers disagree (and they often do in oncology), don't hide it. Show: "3 studies support Protocol A with median survival 12 months. 2 studies show Protocol B with similar outcomes but lower toxicity. 1 study contradicts with poor outcomes for Protocol A in T-cell subtypes." This builds trust through honesty.

10. **Offline-First Mobile** -- Vets work in places without reliable internet (rural clinics, farm visits). A lightweight offline cache of the most common lymphoma queries/responses could be a differentiator.

11. **"Explain This Paper" Mode** -- A vet finds a paper (from a colleague, a conference, a referral). They paste the DOI or title. ASIA retrieves it and provides a structured clinical summary in Italian: key findings, methodology quality assessment, practical implications, how it fits with other evidence. This bridges the gap between "paper exists" and "paper is useful."

12. **Voice Query** -- In a clinical setting, hands are often occupied. Voice input for queries (Italian speech-to-text into ASIA) could be a practical differentiator.

### Theme 3: Creative Differentiation

13. **Open Source as Trust Engine** -- In a medical/clinical context, "open source" means "auditable." Vets (and vet faculties) can inspect exactly how answers are generated, what papers are included, how evidence is weighted. This is a huge advantage over black-box commercial tools. Market this explicitly: "You can see exactly why ASIA gave this answer."

14. **Italian Veterinary Faculty Partnerships** -- Partner with Bologna, Milan, Turin vet faculties. They get a tool for teaching. Students learn evidence-based oncology through ASIA. Faculty contribute expert annotations. ASIA gets credibility, distribution, and a feedback loop. This is the adoption flywheel.

15. **Comparative Oncology Bridge** -- Unique feature no competitor offers: show relevant human oncology parallels. "This CHOP protocol for canine lymphoma is analogous to R-CHOP in human NHL. Here are the key differences." This attracts a second audience (comparative oncology researchers) and adds depth for curious vets.

16. **Community Annotations** -- Let experienced oncology vets annotate protocols with clinical notes: "In my experience with 40 cases, I reduce doxorubicin by 10% for dogs under 5kg." These are flagged as "clinical experience, not peer-reviewed evidence" but add enormous practical value. Think UpToDate's expert commentary layer.

17. **The "Asia's Story" Brand** -- The project's origin story is powerful. A dog named Asia. A frustrating diagnostic journey. A developer who decided to fix the problem. This is not just branding -- it's authenticity. Every other tool in this space is corporate. ASIA is personal. Lead with the story.

18. **"Veterinarian-Verified" Badge System** -- As vets use ASIA and confirm that a synthesis matches their clinical experience, it builds a verification layer. "This synthesis has been reviewed by 12 practicing oncologists." Crowdsourced trust.

### Theme 4: Risks and Blind Spots

19. **Hallucination Risk is Existential** -- If ASIA generates a synthesis that cites a paper incorrectly, recommends a wrong dose, or misattributes a finding, it could harm an animal and destroy trust permanently. Mitigation: aggressive citation verification, never generate without source, always show confidence level, prominent disclaimers. Consider a "verified corpus" mode where answers only come from manually validated papers.

20. **Regulatory Gray Zone** -- Is ASIA a "medical device" under EU regulations? Likely not if positioned as a literature synthesis tool (like UpToDate for humans, which is not regulated as a device). But the framing matters enormously. Never say "ASIA recommends." Say "The literature suggests." Legal review before launch is essential.

21. **Adoption Chicken-and-Egg** -- Vets won't use it until it's good. It won't get good without vet feedback. Solution: find 5-10 beta vets (possibly through Asia's own veterinary team) who test it with real cases. Their feedback shapes the MVP.

22. **Data Freshness vs. Quality** -- Ingesting preprints creates a speed advantage but a quality risk. A preprint that later gets retracted could lead to a harmful recommendation. MVP should probably exclude preprints entirely and only use peer-reviewed literature.

23. **LLM Provider Lock-in** -- If ASIA depends on OpenAI or Anthropic APIs, it's not truly open source. Users can't run it without paying a third party. Consider supporting local LLMs (Llama, Mistral) as a deployment option. Trade-off: quality vs. independence.

24. **Italian Language Model Quality** -- RAG synthesis in Italian requires a model that handles Italian medical terminology well. Current LLMs are English-dominant. Test Italian output quality rigorously -- a bad translation of a clinical recommendation is worse than no translation at all.

25. **Sustainability Without Revenue** -- Open source is not a business model. Server costs, LLM API costs, maintenance. Options: donations, university grants, freemium hosted version, EU research funding (Horizon Europe), Italian digital health grants. Need a sustainability plan from day one.

26. **Veterinary Malpractice Liability** -- If a vet follows ASIA's synthesis and the outcome is bad, is there liability? The disclaimer helps, but this needs legal consideration. Precedent from UpToDate, DynaMed, etc. in human medicine is reassuring but not guaranteed to transfer.

27. **Corpus Completeness Bias** -- ASIA can only synthesize what it has ingested. If important papers are behind paywalls (not open access), ASIA's answers will be biased toward open-access literature. This is a real problem -- many key veterinary oncology journals are paywalled. Need to be transparent about what's included and what's not.

### Theme 5: Unconventional Angles

28. **Pet Owner Companion Mode** -- A simplified, non-technical interface for owners. After the vet consultation, the owner can ask ASIA: "My dog has B-cell lymphoma. The vet suggested CHOP. What does that mean in simple terms? What should I expect?" This is emotional support backed by evidence. It could drive massive adoption (owners tell vets about ASIA, not the other way around).

29. **Veterinary Journal Club Tool** -- A feature where a vet group (clinic, study group, faculty) can do structured journal clubs through ASIA: select a paper, ASIA provides structured analysis, the group discusses and annotates. Turns ASIA from a solo tool into a collaborative learning platform.

30. **Integration with WhatsApp/Telegram** -- Italian vets (like many professionals) live in WhatsApp. A bot that answers clinical queries in a chat interface could have higher adoption than a web app. Lower friction, familiar interface.

31. **Case Report Contribution Pipeline** -- Let vets contribute anonymized case outcomes back to ASIA. "I used CHOP-19 on a Stage IV T-cell lymphoma. Here's what happened." Over time, this creates a real-world evidence dataset that complements the published literature. This is the long-term moat.

32. **Gamified Literature Review** -- "Help ASIA get smarter." Present vets with a paper abstract and ask: "Is this clinically relevant for canine lymphoma? Rate evidence quality 1-5." Rewards: contributor badge, name in credits. This crowdsources quality curation while engaging users.

33. **Multilingual Expansion Path** -- Start Italian, but the architecture should support any language. Spanish, Portuguese, German, French veterinary markets have the same problem. ASIA-ES, ASIA-DE, etc. The open-source community could drive translations.

34. **Conference Integration** -- At veterinary oncology conferences (ESVONC, VCOG), provide real-time synthesis of presented abstracts. "ASIA at ESVONC 2027" -- live coverage. This creates buzz and demonstrates value in a high-visibility context.

35. **Necropsy/Outcome Feedback Loop** -- One of the biggest gaps in veterinary oncology is outcome tracking. If vets could record outcomes (remission duration, survival, cause of death) linked to the protocols they chose, ASIA becomes not just a literature tool but a registry. This is enormously valuable for research.

### Theme 6: MVP Scope Assessment

36. **Canine Lymphoma is the RIGHT Starting Point** -- The assessment in the vision is sound. High prevalence, rich literature, well-defined subtypes, concrete decision points. It's narrow enough to build well and broad enough to deliver real value. Don't change it.

37. **But Define "Lymphoma" Precisely for MVP** -- Multicentric lymphoma (the most common presentation) should be the core. Alimentary, mediastinal, extranodal, and cutaneous lymphoma have different literature bases and clinical pathways. MVP should explicitly state: "multicentric canine lymphoma, B-cell and T-cell" and note that other anatomic forms are coming.

38. **Minimum Viable Corpus** -- Estimate: there are probably 500-1000 relevant papers on canine multicentric lymphoma. Of these, maybe 100-200 are high-quality (prospective studies, meta-analyses, large retrospectives). The MVP should index at least the top 200 papers to provide meaningful synthesis. Define a "core corpus" first.

39. **Five Critical Queries the MVP Must Nail** -- Define acceptance criteria through use cases:
    - "What first-line protocol for Stage III B-cell multicentric lymphoma?"
    - "CHOP-19 vs CHOP-25: differences in outcomes?"
    - "Rescue protocols for early relapse after CHOP?"
    - "Prognosis for T-cell vs B-cell lymphoma?"
    - "Doxorubicin dose adjustment for neutropenia?"
    If ASIA answers these five questions well (accurate, well-cited, clear Italian), the MVP delivers value.

40. **The "First Five Minutes" Test** -- A vet opens ASIA for the first time. They type a question. If the answer is impressive, they come back. If it's mediocre, they never return. The entire MVP should be optimized for that first impression. This means: curate the core corpus aggressively, tune the RAG pipeline on those 5 critical queries, and polish the answer formatting.

---

## Convergence: Three Strategic Approaches

| Dimension | Approach A: Literature Intelligence | Approach B: Clinical Workflow Hub | Approach C: Community Platform |
|-----------|-------------------------------------|----------------------------------|-------------------------------|
| **Core idea** | Excel at one thing: the best evidence synthesis for canine lymphoma. Perfect RAG, perfect citations, perfect Italian. A "better PubMed" for one niche. | Go beyond search. Case management, protocol comparison tables, monitoring checklists, owner communication. A clinical workspace. | Build around community: vet annotations, case contributions, journal clubs, crowdsourced verification. ASIA as a collaborative intelligence. |
| **Pros** | Fastest to build. Clear value proposition. Easiest to validate quality. Sharpest differentiation. | Highest stickiness (vets integrate it into daily workflow). Harder to replicate. Solves multiple pain points. | Strongest long-term moat (network effects). Real-world data accumulation. Community drives adoption. |
| **Cons** | Single-use tool (search and leave). Limited stickiness. Easy for competitors to replicate once concept is proven. | Much larger MVP scope. Risk of building features nobody uses. Higher complexity = more bugs in clinical context. | Chicken-and-egg problem: empty community is useless. Requires critical mass. Slower to show value. Content moderation challenges. |
| **Best for** | Validating the core concept fast. Proving that RAG + Italian + oncology works. Getting to market in months, not years. | A team with bandwidth to build a multi-feature product. Post-validation expansion. | Post-MVP growth phase when you have a user base. Can layer onto Approach A later. |
| **Risk** | Becomes a demo, not a product. Users try it once and forget. | Over-engineering before validation. Building a Swiss Army knife when users wanted a scalpel. | Community never reaches critical mass. Becomes a ghost town with stale annotations. |

**Recommendation**: Start with Approach A (Literature Intelligence) as the MVP. It validates the core hypothesis with minimum complexity. Then layer in select elements from Approach B (protocol comparison tables and side effect advisor are the highest-value additions). Approach C is a Phase 2 play after you have 50+ active users.

---

## Provocative "What If..." Questions for Further Exploration

- What if the killer app isn't for vets, but for pet owners? (Idea #28)
- What if ASIA's real value isn't answers but confidence? (Reducing decision anxiety)
- What if the open-source community becomes the distribution channel? (Vet school forks)
- What if the comparative oncology angle attracts human oncology researchers -- and with them, funding?
- What if the biggest barrier isn't building ASIA but getting 10 vets to try it?
- What if a WhatsApp bot outperforms a web app for Italian vet adoption?

---

## Next Steps

1. **Validate MVP scope**: Confirm "multicentric canine lymphoma" as the precise boundary. Define the 5 critical queries (see #39).
2. **Identify beta vets**: Find 3-5 veterinarians (start with Asia's own vet team) willing to test early prototypes and provide feedback.
3. **Corpus analysis**: Search PubMed for canine multicentric lymphoma papers, estimate total count and open-access availability. Define the "core 200" papers.
4. **Legal review**: Clarify EU regulatory position. Is ASIA a "clinical decision support" tool or a "literature search" tool? The answer determines compliance requirements.
5. **LLM Italian quality benchmark**: Test 3-4 LLMs (GPT-4o, Claude, Llama 3, Mistral) on Italian veterinary oncology synthesis quality. Choose the best one, and verify a local model is viable for the open-source deployment story.
6. **Architecture design**: Proceed to design phase with the Architecture agent.

---

## Sources

- [AI in Veterinary Oncology: Scoping Review (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12817679/)
- [NCI Comparative Oncology Program](https://ccr.cancer.gov/comparative-oncology-program)
- [One Health, One Medicine: Canine Cancer Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12191360/)
- [ImpriMed: CHOP Protocol Guide](https://www.imprimedicine.com/blog/chop-protocol)
- [CHOP-19 vs CHOP-25 European Multicenter Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11586558/)
- [UW Veterinary Care: Chemotherapy Protocols](https://uwveterinarycare.wisc.edu/small-animal/cats-and-dogs/oncology/chemotherapy-protocols/)
- [Veterinary Oncology Market Analysis 2025-2030](https://www.globenewswire.com/news-release/2025/09/03/3143360/0/en/Veterinary-Oncology-Market-Shares-Competition-and-Trends-Analysis-2025-2030-Discover-the-Impact-of-Advanced-Therapies-and-Digital-Tools.html)
- [Ethical Considerations of AI in Veterinary Decision-Making (2026)](https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2026.1780868/full)
- [Colorado State: One Health, One Cancer, One Cure](https://www.csuanimalcancercenter.org/2020/01/23/one-health-one-cancer-one-cure/)
- [FidoCure: Personalized Canine Cancer Treatment](https://fidocure.com/)
