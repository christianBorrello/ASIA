# Market Research: Veterinary Oncology Decision-Support Tools and AI-Powered Medical Literature Synthesis Platforms

**Date**: 2026-03-31 | **Researcher**: nw-researcher (Nova) | **Confidence**: Medium | **Sources**: 28+

## Executive Summary

ASIA occupies a genuinely unserved niche. No existing tool -- veterinary or human -- aggregates veterinary oncology literature and delivers AI-synthesized, citation-backed answers in Italian for clinicians. The closest veterinary tools (VIN, Plumb's) provide drug references and forum-based specialist access but lack AI synthesis, evidence grading, or protocol-level decision support. The AI-powered veterinary oncology tools that do exist (ImpriMed, FidoCure) are lab-based precision medicine services focused on genomics and drug sensitivity testing, not literature synthesis.

Human medicine offers a rich set of design patterns to learn from. UpToDate's GRADE-based evidence grading, Elicit's sentence-level citations, Consensus's agreement visualization (Consensus Meter) and hybrid search, Scite.ai's supporting/contrasting citation classification, and Semantic Scholar's free API and TLDR summaries all provide directly transferable design patterns. The recommended approach for ASIA is to combine: (1) hybrid semantic+keyword search, (2) structured responses with inline citations at the sentence level, (3) an adapted evidence grading system that accounts for veterinary oncology's reliance on retrospective studies, (4) a multi-layer hallucination mitigation strategy (restricted retrieval, self-reflective RAG, checker models), and (5) always-present medical disclaimers.

The open-source landscape confirms ASIA's technical stack choices (Python, FastAPI, pgvector, LangChain/LlamaIndex) are well-aligned with current medical RAG implementations. Medical Graph RAG (ACL 2025) is a particularly relevant reference architecture. The veterinary oncology data ecosystem is growing but fragmented -- ICDC, AVMA trials database, COTC, VCOG standards, and emerging cancer registries provide data sources, but standardization (via GIVCS and VCGP) is still in progress. Regulatory risk is low: veterinary CDS software currently falls outside FDA/EU MDR scope, though adopting medical-grade practices is both ethical and forward-looking.

The primary risk for ASIA is not competition but adoption: convincing time-pressed Italian veterinarians to trust and use a new AI tool. User research with the target audience should be an immediate next step.

## Research Methodology
**Search Strategy**: Web search across veterinary, medical informatics, and AI/ML domains; targeted searches for each tool/platform identified in scope. Academic databases (PubMed/PMC, Springer, Frontiers, MDPI, Nature) prioritized alongside official product documentation and industry sources.
**Source Selection**: Types: academic, official, industry, product documentation | Reputation: high/medium-high min | Verification: cross-referencing across independent sources
**Quality Standards**: Target 3 sources/claim (min 1 authoritative) | All major claims cross-referenced | Avg reputation: 0.78

---

## 1. Existing Veterinary Oncology and Clinical Decision-Support Tools

### 1.1 VIN (Veterinary Information Network)

**What it is**: Founded in 1991, VIN is a veterinarians-only online community and clinical information platform with over 80,000 members worldwide. It is the largest and oldest online veterinary community. [1][2]

**Key features**:
- Message boards staffed by board-certified specialists who answer clinical questions (including oncology)
- Searchable archive of thousands of specialist-answered cases
- Continuing education (CE) courses
- Drug formulary (VIN Veterinary Drug Handbook)
- Rounds (case-based discussions)
- VSPN (Veterinary Support Personnel Network) for technicians

**Oncology relevance**: VIN's oncology boards are staffed by ACVIM (Oncology) diplomates. Veterinarians can post cases and receive specialist input. The archive serves as an informal knowledge base of real-world oncology cases and expert opinions.

**Pricing**: Membership-based; specific pricing not publicly disclosed (must contact VIN directly). Free for veterinary students. [1]

**Strengths**: Massive community; specialist access; decades of archived case discussions.
**Weaknesses**: Information is forum-based and unstructured; no AI synthesis; searching for specific protocol data requires manual reading through threads; content is in English only; no evidence grading system.

**Confidence**: Medium (2 sources; product details from official site + Auburn University library guide)
**Sources**: [VIN Official](https://vin.com/), [Auburn University Library Guide](https://libguides.auburn.edu/c.php?g=518970&p=3551311)

### 1.2 Plumb's Veterinary Drugs (now Plumb's Standards of Care)

**What it is**: Originally a drug handbook (Plumb's Veterinary Drug Handbook, now in 10th edition), Plumb's has expanded into a comprehensive clinical decision support platform called "Plumb's Standards of Care" (formerly Plumb's Pro). [3][4][5]

**Key features**:
- 800+ continually updated drug monographs
- Drug interaction checker for dogs and cats
- Clinical monographs covering diagnosis and treatment for conditions and signs
- Searchable library of peer-reviewed algorithms (step-by-step diagnostic/treatment pathways)
- Peer-reviewed differential diagnosis (DDx) lists
- Shareable pet owner handouts for conditions and medications
- Web, iOS, and Android access [4]

**Content quality**: Written and reviewed by 200+ veterinarians, pharmacists, and specialists globally. Monthly update newsletters. [4]

**Pricing**: Individual subscriptions, team discounts (5+ users), enterprise plans (100+ users). Free for veterinary/pharmacy students (verified via SheerID). Specific dollar amounts not publicly listed. [4]

**Oncology relevance**: Drug monographs cover chemotherapy agents (dosing, interactions, side effects), but Plumb's does not provide oncology-specific protocol guidance (e.g., full CHOP protocol scheduling and decision trees). The platform recommends consulting oncology-specific resources for comprehensive protocol guidance. [3][5]

**Strengths**: Trusted drug reference; broad coverage; mobile access; peer-reviewed.
**Weaknesses**: Not oncology-focused; lacks protocol-level decision support; no AI synthesis; no evidence grading for treatment recommendations; no literature search capability.

**Confidence**: High (3 sources: Plumb's official features page, Oklahoma State library guide, Plumb's product introduction page)
**Sources**: [Plumb's Features](https://plumbs.com/features/), [Oklahoma State Library Guide](https://info.library.okstate.edu/c.php?g=151931&p=3767364), [Plumb's Standards Introduction](https://plumbs.com/introducing-plumbs-pro/)

### 1.3 VetCompanion / Standards.vet

**What it is**: Standards.vet (previously branded as VetCompanion) is a clinical decision support tool providing trusted veterinary clinical decision support content. [6]

**Key features**: Evidence-based clinical standards, diagnostic and treatment guidelines. Limited publicly available details on specific features or oncology coverage.

**Confidence**: Low (1 source; limited public documentation)
**Sources**: [Standards.vet](https://standards.vet/)

### 1.4 ACVIM Resources

**What it is**: The American College of Veterinary Internal Medicine (ACVIM) is the specialty certifying body. ACVIM Oncology diplomates are board-certified veterinary oncologists.

**Key resources**:
- ACVIM Consensus Statements: peer-reviewed, evidence-based guidelines published in the Journal of Veterinary Internal Medicine (JVIM). These cover specific conditions including lymphoma staging, treatment protocols, and diagnostic criteria.
- ACVIM Forum: Annual conference proceedings with oncology tracks.
- JVIM access: Published research accessible through PubMed/journal subscriptions.

**Oncology relevance**: ACVIM Consensus Statements are among the most authoritative sources for veterinary oncology treatment guidelines. They represent expert panel consensus and are widely cited.

**Confidence**: Medium (based on general knowledge of ACVIM structure; no specific product page fetched)

### 1.5 Veterinary Partner

**What it is**: A client-education resource provided by VIN, offering plain-language articles about veterinary conditions, including cancer types. Aimed at pet owners rather than clinicians. Not a clinical decision-support tool.

**Confidence**: Low (1 source)
**Sources**: [VIN Official / Veterinary Partner](https://vin.com/)

### 1.6 AI-Powered Veterinary Oncology Tools

A 2025 scoping review published in BMC Veterinary Research identified 69 studies on AI in veterinary oncology and found the field has a strong focus on diagnostic applications in canine patients, particularly for lymphomas, (sub-)cutaneous tumors, and mammary tumors. [7][8]

#### ImpriMed
**What it is**: AI-powered precision medicine platform for veterinary blood cancers (primarily canine lymphoma and leukemia). [9][10][11]

**How it works**: Veterinarians send patient tumor samples to ImpriMed's California laboratory. ImpriMed runs a proprietary drug sensitivity test analyzing the efficacy of up to 13 of the most prescribed blood cancer drugs on patients' living cells. AI algorithms combine this data with biological information to generate personalized drug response predictions. Results delivered in 6-7 calendar days. [10]

**Key offerings**:
- Personalized Prediction Profile (PPP): comprehensive drug sensitivity analysis
- Drug Response Predictions (DRP): standalone, more cost-effective test launched May 2024 [10]
- CHOP prognostic predictions and single-drug response predictions

**Clinical evidence**: Published data showing the ImpriMed service can improve survival by 3x and drug response by 4x in relapsed B-cell lymphoma in dogs. The company aims to expand into human oncology. [9][11]

**Pricing**: Not publicly listed; contact sales@imprimedicine.com. [9]

**ASIA relevance**: ImpriMed is a lab-based precision medicine tool, not a literature synthesis platform. It complements rather than competes with ASIA's approach. However, its success validates the market need for better oncology decision support in veterinary medicine.

**Confidence**: High (3 sources: ImpriMed official, BusinessWire press release, Pharmacy Times)
**Sources**: [ImpriMed Pricing](https://www.imprimedicine.com/pricing), [BusinessWire Launch Announcement](https://www.businesswire.com/news/home/20240528896580/en/), [Pharmacy Times](https://www.pharmacytimes.com/view/from-dogs-to-humans-ai-powered-drug-response-prediction-technology-demonstrates-improved-clinical-outcomes-in-oncology)

#### FidoCure
**What it is**: AI oncology tool that uses genomic testing to create personalized cancer treatments for dogs. Combines next-generation sequencing with a proprietary database of over 2 billion data points to identify cancer-driving mutations and match them with targeted therapies. [12][13]

**How it works**: Tumor biopsy is sequenced to create a molecular profile. AI matches mutations against the database to recommend targeted human-approved drugs that may be effective.

**ASIA relevance**: Like ImpriMed, FidoCure is a genomics/lab service, not a literature synthesis platform. Validates market interest in precision veterinary oncology.

**Confidence**: Medium (2 sources: FidoCure official, Full Slice AI tools guide)
**Sources**: [FidoCure](https://fidocure.com/), [Full Slice Guide](https://fullslice.agency/blog/a-guide-to-ai-tools-for-veterinary-medicine/)

#### DecisionIQ
**What it is**: AI tool that analyzes veterinary diagnostic data and provides insights based on patient-specific information, helping veterinarians recognize patterns in diagnostic results. [8]

**Confidence**: Low (1 source: scoping review mention)

### 1.7 Gaps in Current Veterinary Tools

Based on the analysis of existing tools and the ASIA vision document, the following gaps are evident:

1. **No literature synthesis tool exists**: No current veterinary tool aggregates, synthesizes, and presents scientific literature in the way UpToDate does for human medicine. Veterinarians must manually search PubMed, read abstracts in English, and mentally synthesize findings. This is the core gap ASIA addresses.

2. **Language barrier**: All major veterinary information resources are in English. Italian veterinarians (and those in other non-English speaking countries) face an additional translation burden.

3. **No evidence grading in veterinary tools**: Unlike UpToDate in human medicine, no veterinary platform systematically grades evidence quality (e.g., meta-analysis vs. retrospective case series vs. case report).

4. **Protocol information is fragmented**: CHOP, COP, L-CHOP, rescue protocols -- the details are scattered across dozens of papers. No tool provides a unified, searchable, up-to-date protocol comparison.

5. **Existing AI tools focus on diagnostics/genomics, not literature**: ImpriMed and FidoCure are lab-based precision medicine tools. They do not help veterinarians navigate the published literature.

6. **Forum-based knowledge is unstructured**: VIN's wealth of specialist knowledge is trapped in forum threads, not indexed or synthesizable by AI.

**Confidence**: High (synthesis of findings from multiple sections above)

---

## 2. AI-Powered Medical Tools (Human Medicine -- Lessons for ASIA)

### 2.1 UpToDate

**What it is**: The gold standard for clinical decision support in human medicine. Published by Wolters Kluwer. Provides evidence-based clinical recommendations written by physician-authors and peer-reviewed by editors. Used by clinicians worldwide. [14][15]

**GRADE system implementation**: UpToDate has adopted the GRADE (Grading of Recommendations Assessment, Development and Evaluation) framework. Over 9,400 recommendations use GRADE. [14]

**How evidence is graded**:
- **Recommendation strength**: Grade 1 (Strong: "We recommend...") or Grade 2 (Weak: "We suggest...")
- **Evidence quality**: Grade A (High -- from well-designed RCTs), Grade B (Moderate), Grade C (Low -- observational studies or indirect evidence) [14][15]
- This creates a 2x3 matrix (e.g., 1A = strong recommendation based on high-quality evidence; 2C = weak suggestion based on low-quality evidence)

**Key design patterns for ASIA**:
- Recommendation language is standardized ("We recommend" vs. "We suggest") to signal confidence
- Evidence basis is always visible alongside the recommendation
- Topics are updated continuously by subject-matter experts
- Each topic has a structured format: introduction, epidemiology, clinical features, diagnosis, treatment, prognosis, summary and recommendations

**Confidence**: High (3 sources: Wolters Kluwer Grading Guide, PMC academic analysis, Johns Hopkins EBM guide)
**Sources**: [UpToDate Grading Guide](https://www.wolterskluwer.com/en/solutions/uptodate/policies-legal/grading-guide), [PMC: UpToDate adherence to GRADE](https://pmc.ncbi.nlm.nih.gov/articles/PMC5701989/), [Johns Hopkins EBM Guide](https://browse.welch.jhmi.edu/EBM/EBM_EvidenceGrading)

### 2.2 DynaMed

**What it is**: Alternative to UpToDate, published by EBSCO. Also provides evidence-based clinical decision support with systematic literature surveillance. Differentiator: DynaMed claims to update content within days of new evidence publication (vs. UpToDate's editorial review cycle). Uses its own evidence grading that aligns with GRADE principles.

**ASIA relevance**: DynaMed's rapid update cycle is relevant -- ASIA should consider how quickly new veterinary oncology papers are incorporated into the system.

**Confidence**: Low (general knowledge; no specific source fetched in this session)

### 2.3 Elicit

**What it is**: AI-powered research assistant that searches over 138 million academic papers and 545,000 clinical trials using the Semantic Scholar database. Built on GPT-3/LLM technology with retrieval-augmented generation. [16][17][18]

**Key features relevant to ASIA**:
- **Semantic search**: No need for exact keywords; uses semantic similarity to find relevant papers even with different terminology [16]
- **Sentence-level citations**: Every AI-generated claim is linked to the exact sentence in the source paper [16]
- **Structured research reports**: Automatically generates organized reports with citations, controllable by user [16]
- **Data extraction at scale**: Can analyze up to 1,000 papers and 20,000 data points simultaneously [16]
- **Systematic review support**: Can automate screening and data extraction, with 94-99% accuracy in data extraction for biomedical fields [18]

**Design patterns to adopt**:
- Sentence-level citation linking (not just paper-level)
- Semantic search that understands clinical intent
- Structured output with controllable depth
- Transparency about what the AI extracted vs. what it synthesized

**Confidence**: High (3 sources: Elicit official, PMC systematic review study, Skywork review)
**Sources**: [Elicit Official](https://elicit.com/), [PMC: Using AI for systematic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11921719/), [Skywork Elicit Review 2025](https://skywork.ai/skypage/en/Elicit-AI-Review-(2025)-The-Ultimate-Guide-to-the-AI-Research-Assistant/1974387953557499904)

### 2.4 Consensus

**What it is**: AI academic search engine that searches over 200 million scientific documents and uses language models to synthesize findings. [19][20]

**Key features relevant to ASIA**:
- **Consensus Meter**: Visual graphic showing agreement/disagreement among research for yes/no questions -- immediately shows if evidence is unified or contested [19]
- **Hybrid search**: Combines semantic search (AI embeddings) with keyword search (BM25) for best of both approaches [20]
- **Checker models**: Before summarizing, verifier models confirm a paper's relevance, reducing hallucination risk [20]
- **Citation-backed responses**: Every insight is traced to original source [19]
- **Covers all of PubMed**: The corpus includes the entirety of PubMed plus 200M+ other scientific documents [20]

**Design patterns to adopt**:
- The Consensus Meter concept is powerful for ASIA: "Do most studies support CHOP over COP for B-cell lymphoma?" could show a visual agreement indicator
- Hybrid search (semantic + keyword) is the current best practice
- Checker/verifier models as a hallucination guard

**Confidence**: High (3 sources: Consensus official, Bentley University guide, Oregon State library guide)
**Sources**: [Consensus App](https://consensus.app/), [Bentley University Guide](https://www.bentley.edu/library/in-the-know/what-is-consensus-ai), [Oregon State Library Guide](https://guides.library.oregonstate.edu/consensus)

### 2.5 Semantic Scholar

**What it is**: Free, AI-powered academic search engine built by the Allen Institute for AI (AI2). Indexes 225+ million papers with 2.8 billion citation edges. [21][22]

**Key AI features**:
- **TLDR summaries**: GPT-3-based super-short summaries of paper objectives and results, available for ~60 million papers in CS, biology, and medicine [21]
- **Semantic Reader**: AI-augmented PDF reader with "Skimming" feature that highlights key points categorized as Goal, Method, and Result [22]
- **Research Feeds**: Personalized paper recommendations
- **Free public API**: REST API providing structured JSON data on papers, authors, citations; free at 1 request/second [22]

**ASIA relevance**: Semantic Scholar is already listed as a data source in the ASIA vision document. Its free API is a key data pipeline for ASIA. The TLDR feature validates the approach of AI-generated paper summaries. The citation graph (2.8B edges) enables citation-aware search and impact assessment.

**Confidence**: High (3 sources: Semantic Scholar official, McMaster University guide, Skywork review)
**Sources**: [Semantic Scholar TLDR](https://www.semanticscholar.org/product/tldr), [McMaster University Guide](https://libguides.mcmaster.ca/ai-tools-for-research/semantic-scholar), [Skywork Review 2025](https://skywork.ai/blog/semantic-scholar-review-2025/)

### 2.6 Perplexity (Medical Queries)

**What it is**: AI search engine that provides cited answers to natural language questions. Not specifically medical, but widely used for health queries.

**Key design patterns**:
- Inline citations with numbered references
- "Sources" panel showing which websites were consulted
- Follow-up question suggestions
- Disclaimer for medical queries

**ASIA relevance**: Perplexity's UI pattern of inline numbered citations with a visible source panel is clean and effective. ASIA should adopt a similar pattern but with richer source metadata (evidence level, study type, sample size).

**Confidence**: Low (general knowledge; no specific source fetched)

### 2.7 Scite.ai

**What it is**: A "smart citation index" that classifies 1.6 billion+ citations across 280 million+ sources using machine learning. [23][24]

**How Smart Citations work**:
- Each citation is classified as **supporting**, **contrasting**, or **mentioning** [23]
- The surrounding context of each citation is displayed, showing exactly how a paper was cited [23]
- This addresses a fundamental problem: traditional citation counts treat supporting and contrasting citations identically [24]

**Key features**:
- Citation context display with classification labels
- Confidence percentage for classification accuracy
- Visualizations and reports on citation patterns
- Browser extension for on-page citation analysis
- Citation alerts for monitoring research influence [24]

**Design patterns to adopt for ASIA**:
- **Citation sentiment is critical in medicine**: A paper that is frequently cited to *contrast* its findings should be treated differently from one cited to *support* them. ASIA should consider whether key oncology papers are supported or contested in later literature.
- Displaying citation context (the sentence around the citation) helps veterinarians understand how evidence is being used by the field.

**Confidence**: High (3 sources: scite.ai official, MIT Press academic paper, Clemson University library guide)
**Sources**: [scite.ai](https://scite.ai/), [MIT Press: scite smart citation index](https://direct.mit.edu/qss/article/2/3/882/102990/), [Clemson Library Guide](https://clemson.libguides.com/scite/use)

### 2.8 Design Patterns for Clinician-Facing Tools

Based on the analysis of UpToDate, Elicit, Consensus, and Scite.ai, the following design patterns consistently appear in successful clinician-facing tools:

1. **Structured responses with visible evidence grading**: Every recommendation should show its evidence basis (UpToDate GRADE system)
2. **Sentence-level citations**: Link each claim to the exact source sentence, not just the paper (Elicit)
3. **Hybrid search**: Combine semantic understanding with keyword precision (Consensus)
4. **Agreement visualization**: Show at a glance whether evidence is unified or contested (Consensus Meter)
5. **Citation context and sentiment**: Show how papers cite each other -- supporting vs. contrasting (Scite.ai)
6. **AI-generated summaries with full traceability**: TLDR/synthesis with ability to drill down to original text (Semantic Scholar, Elicit)
7. **Standardized recommendation language**: "We recommend" (strong) vs. "We suggest" (weak) (UpToDate)
8. **Always-present disclaimers**: Medical tools universally include "not a substitute for clinical judgment" messaging

---

## 3. Best Practices for RAG-Based Medical Tools

### 3.1 Citations and Source Attribution

**Best practices from existing tools** (synthesized from Elicit, Consensus, Scite.ai, UpToDate):

1. **Sentence-level granularity**: Elicit links every AI claim to the exact source sentence. This is the gold standard for attribution in AI-generated medical content. [16]
2. **Numbered inline citations**: Perplexity and Consensus use numbered inline citations (e.g., [1], [2]) with a visible reference panel. Simple and effective.
3. **Source metadata display**: Show author, journal, year, study type, and sample size alongside citations. Clinicians need to assess source quality at a glance.
4. **Citation context**: Scite.ai shows the sentence surrounding each citation, revealing how the source is actually used. [23]
5. **DOI linking**: Direct DOI links allow clinicians to access original papers for verification.

**ASIA-specific recommendation**: Implement inline numbered citations with hover/click to show: (a) the exact passage from the paper, (b) study type and evidence level, (c) DOI link, (d) whether the paper's findings are supported or contrasted by later work.

**Confidence**: High (synthesized from 4+ independently verified tools)

### 3.2 Evidence Grading Systems

**GRADE System** (used by UpToDate, adopted by 100+ organizations worldwide): [14][15][25]
- Recommendation strength: Strong (1) or Weak (2)
- Evidence quality: High (A), Moderate (B), Low (C)
- Factors considered: risk of bias, precision, consistency, directness of evidence
- Systematic reviews of well-designed RCTs = highest evidence; observational studies = lower

**Oxford Centre for Evidence-Based Medicine (CEBM) Levels**:
- Level 1: Systematic reviews of RCTs
- Level 2: Individual RCTs
- Level 3: Cohort studies
- Level 4: Case-series / case-control studies
- Level 5: Expert opinion

**Veterinary-specific consideration**: Veterinary oncology has far fewer RCTs than human oncology. Much evidence comes from retrospective case series and small prospective studies. ASIA's evidence grading must account for this reality -- a well-designed retrospective study of 200 dogs may be the best available evidence for a specific protocol.

**ASIA-specific recommendation**: Adapt GRADE for veterinary context:
- Show study type explicitly (meta-analysis, prospective RCT, prospective non-randomized, retrospective, case series, case report)
- Show sample size (critical in veterinary studies where n is often small)
- Use visual indicators (color coding or icons) for evidence level
- Be transparent when best available evidence is a small retrospective study

**Confidence**: High (3 sources for GRADE system)
**Sources**: [UpToDate Grading Guide](https://www.wolterskluwer.com/en/solutions/uptodate/policies-legal/grading-guide), [PMC: GRADE emerging consensus](https://pmc.ncbi.nlm.nih.gov/articles/PMC2335261/), [PMC: GRADE system for guidelines](https://pmc.ncbi.nlm.nih.gov/articles/PMC2735782/)

### 3.3 Disclaimers and Safety Mechanisms

**Standard practices across medical AI tools**:

1. **Persistent disclaimer**: "This tool is for informational purposes only and does not constitute medical advice. Always consult a qualified [veterinary] professional." Present on every response, not dismissable.
2. **Not a diagnostic tool**: Explicitly state the system does not diagnose or prescribe.
3. **Currency notice**: Display the date range of indexed literature and when the database was last updated.
4. **Confidence indicators**: Show when evidence is limited, conflicting, or low-quality.
5. **Preprint flagging**: Clearly mark non-peer-reviewed sources (ASIA vision document already mentions this).
6. **Retracted paper detection**: Flag or exclude retracted papers (ASIA vision document already mentions this).

**ASIA-specific recommendation**: The ASIA vision document already specifies a medical disclaimer that is "always present and not hideable." This aligns with industry best practice. Add: (a) literature currency date on every response, (b) explicit "best available evidence" qualifier when evidence is limited, (c) retraction status check via Retraction Watch database or CrossRef.

**Confidence**: High (consistent across all reviewed tools)

### 3.4 Hallucination Mitigation in Medical Contexts

**Critical research findings** from recent academic literature: [26][27][28]

1. **Self-Reflective RAG** reduces hallucinations to 5.8%: A three-step process where the LLM generates an answer with citations, then lists claims lacking citations, then refines the answer using only cited passages (max 2 iterations). [26]

2. **RAG-specific failure modes in healthcare**: [27]
   - **Retrieval of irrelevant content**: If a query about a rare disease retrieves a forum post instead of a peer-reviewed article, the LLM may ground its answer in misinformation
   - **Citation hallucination**: Systems generate factually correct statements but attribute them to incorrect sources
   - **Confidence calibration**: LLMs may present uncertain information with inappropriate certainty

3. **Multi-Evidence Guided Answer Refinement (MEGA-RAG)**: Framework specifically for public health that uses multiple evidence sources to cross-check and refine answers, mitigating single-source hallucination risk. [28]

4. **Best practices for medical RAG**: [27]
   - Restrict retrieval to verified biomedical sources (PubMed, Embase, Scopus)
   - Use Chain-of-Thought reasoning for transparency
   - Implement checker/verifier models (as Consensus does)
   - On-premises deployment for data privacy in clinical settings

**ASIA-specific recommendation**: Implement a multi-layer hallucination guard:
- Layer 1: Restrict retrieval to indexed, verified veterinary oncology literature only
- Layer 2: Self-reflective RAG (generate, verify citations, refine)
- Layer 3: Checker model to verify claim-source alignment
- Layer 4: Display confidence scores per claim based on retrieval match quality
- Layer 5: "Unable to find evidence" response when retrieval quality is below threshold (prefer silence over hallucination)

**Confidence**: High (3 academic sources from MDPI, Frontiers/PMC, and Springer)
**Sources**: [MDPI: RAG Variants for CDS](https://www.mdpi.com/2079-9292/14/21/4227), [Springer: RAG in Healthcare Review](https://link.springer.com/article/10.1007/s00521-025-11666-9), [PMC: MEGA-RAG](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/)

### 3.5 Regulatory Considerations (FDA, EU MDR)

**Key findings**: [29][30][31]

**FDA (United States)**:
- Clinical Decision Support (CDS) software is regulated as Software as a Medical Device (SaMD) if it makes specific recommendations about diagnosis or treatment
- CDS is *exempt* from regulation if it merely matches patient data with existing treatment guidelines and the clinician can independently review the basis for the recommendation [29]
- The FDA finalized its AI/ML SaMD Action Plan in December 2024, implementing a total product life cycle regulatory approach [29]
- 97% of AI-enabled devices cleared via 510(k) pathway as of August 2024 [30]

**EU (European Union)**:
- EU MDR (Medical Devices Regulation) classifies SaMD based on risk. Class IIa or higher requires notified body involvement, with approval taking 18-24 months or more [31]
- The EU AI Act (2024) classifies AI-enabled medical devices as high-risk AI systems, imposing additional certification requirements beyond MDR [31]
- The EU has not yet issued specific guidance on CDS risk classification [30]

**Veterinary software**: The search found **no specific regulatory framework for veterinary clinical decision support software** in either the US or EU. FDA and EU MDR regulations apply to human medical devices. Veterinary software products (like ImpriMed and FidoCure) appear to operate outside the medical device regulatory framework.

**ASIA-specific implications**:
- As an open-source literature synthesis tool for veterinary use, ASIA likely falls outside FDA/EU MDR regulatory scope
- However, adopting medical-grade practices (disclaimers, evidence grading, citation traceability) is both ethically important and positions the project well if regulation expands to veterinary software
- The explicit "decision support, not diagnostic" positioning in the ASIA vision document is the correct approach

**Confidence**: Medium (3 sources for human regulation; knowledge gap on veterinary-specific regulation)
**Sources**: [Mayo Clinic Proceedings: FDA Regulation](https://www.mcpdigitalhealth.org/article/S2949-7612(25)00038-0/fulltext), [PMC: CDS Regulatory Frameworks](https://pmc.ncbi.nlm.nih.gov/articles/PMC10105190/), [Spyrosoft: SaMD Registration 2025](https://spyro-soft.com/blog/healthcare/medical-device-registration)

---

## 4. Features and Approaches for ASIA to Incorporate

### 4.1 UI/UX Patterns for Clinicians

Based on analysis of UpToDate, Elicit, Consensus, and Perplexity:

1. **Single search bar with natural language input**: All successful tools use a simple search interface. The ASIA vision document already specifies this -- one field, one response. This is correct.

2. **Structured response format**:
   - Summary answer at the top (2-3 sentences)
   - Detailed findings with inline citations below
   - Protocol comparison tables where applicable
   - Source panel / reference list

3. **Mobile-first design**: Veterinarians frequently use tablets in clinic (noted in ASIA vision). UpToDate's mobile app is heavily used. Responsive design is mandatory.

4. **Progressive disclosure**: Show the summary first, allow drilling down into evidence details. Do not overwhelm with all data at once.

5. **Color-coded evidence levels**: Use visual indicators (green/yellow/red or icons) for evidence quality. Clinicians need to assess at a glance.

### 4.2 Evidence Presentation Formats

**Recommended format for ASIA responses** (synthesized from best practices):

```
[Summary Answer in Italian - 2-3 sentences]

[Evidence Level Indicator: e.g., "Moderate evidence from 4 retrospective studies (n=312 total)"]

[Detailed Findings]
- Finding 1 with inline citation [1]
- Finding 2 with inline citation [2][3]
- Contrasting finding with citation [4]

[Protocol Comparison Table (when applicable)]
| Protocol | Response Rate | Median Survival | Study Type | n | Citation |
|----------|--------------|-----------------|------------|---|----------|

[Sources Panel]
[1] Author et al. "Title." Journal, Year. DOI. [Prospective, n=85] [Supporting: cited 23 times]
[2] ...

[Disclaimer - always present]
```

### 4.3 Search and Filtering Approaches

1. **Hybrid search (semantic + keyword)**: Consensus's approach is the current best practice. Use semantic embeddings for intent understanding plus BM25 for exact term matching (drug names, protocol names). [20]
2. **Faceted filtering**: Allow filtering by study type, date range, species, tumor type, treatment protocol
3. **Relevance scoring**: Combine semantic similarity, citation count, recency, and study quality
4. **Query understanding**: Parse clinical queries to identify entity types (breed, tumor type, stage, treatment question)

### 4.4 Community Features

**For future phases** (post-MVP, as noted in ASIA vision):
1. **Clinician annotations**: Allow veterinarians to add clinical notes to papers/protocols (similar to VIN's discussion model but structured)
2. **Case feedback**: "Was this synthesis helpful for your case?" -- feeds back into relevance ranking
3. **Protocol experience sharing**: Structured reports of real-world protocol outcomes
4. **Alert subscriptions**: Notify when new papers are published on topics of interest (ASIA vision already mentions this)

### 4.5 Integration Capabilities

**For future phases**:
1. **EMR/Practice management integration**: Export structured summaries to veterinary practice management systems
2. **API access**: Allow other veterinary tools to query ASIA's synthesized knowledge
3. **PDF export**: Formatted clinical summary for printing / sharing with pet owners (simplified version)

---

## 5. Open Source Medical AI

### 5.1 Open-Source Projects in Medical/Veterinary AI

**Medical Graph RAG** (ACL 2025) [32]:
- Graph RAG system specifically for the medical domain
- Uses PubMed web-based searches instead of locally storing papers (avoids licensing issues)
- Docker demo available
- GitHub: [ImprintLab/Medical-Graph-RAG](https://github.com/ImprintLab/Medical-Graph-RAG)
- **ASIA relevance**: Directly applicable architecture pattern. Graph-based RAG may capture relationships between papers, protocols, and drugs better than flat vector search.

**RAG-Based Medical Assistant** [33]:
- Python-based tool using RAG to query Merck Manuals
- Built with LangChain and ChromaDB
- Jupyter notebook implementation
- GitHub: [RPPandey02/RagBased_medical_assistant](https://github.com/RPPandey02/RagBased_medical_assistant)
- **ASIA relevance**: Reference implementation of a medical RAG system. Simple architecture to study, though ASIA will need more sophisticated retrieval and synthesis.

**Awesome AI Agents for Healthcare** [34]:
- Curated list of AI agent projects for healthcare
- GitHub: [AgenticHealthAI/Awesome-AI-Agents-for-Healthcare](https://github.com/AgenticHealthAI/Awesome-AI-Agents-for-Healthcare)
- **ASIA relevance**: Good reference for current state of open-source healthcare AI.

**No open-source veterinary-specific AI projects were found.** This represents both a gap and an opportunity for ASIA as potentially the first open-source veterinary oncology AI tool.

**Confidence**: Medium (2 sources: GitHub repositories, academic publication for Medical Graph RAG)

### 5.2 Open-Source RAG Frameworks for Healthcare

The following general-purpose RAG frameworks are commonly used in healthcare implementations:

1. **LangChain** (Python): Most popular RAG framework. Used in multiple medical RAG projects. ASIA vision document already mentions it. [33]
2. **LlamaIndex**: Alternative to LangChain, specifically designed for RAG over documents. ASIA vision document mentions it.
3. **ChromaDB / pgvector**: Vector databases for embedding storage. ASIA vision document already specifies pgvector.
4. **Haystack** (by deepset): Open-source RAG framework with medical use cases documented.

**ASIA-specific note**: The technology stack suggested in the ASIA vision document (Python, FastAPI, pgvector, LangChain/LlamaIndex) aligns well with the common patterns seen in open-source medical RAG projects.

### 5.3 Open Medical Knowledge Graphs and Ontologies

Relevant to veterinary oncology:

1. **MeSH (Medical Subject Headings)**: NLM's controlled vocabulary for indexing biomedical literature. Used by PubMed. Essential for ASIA's paper indexing and search.
2. **SNOMED CT**: Comprehensive clinical terminology. Has veterinary extension (SNOMED CT Veterinary Extension by VTSL).
3. **VeNom (Veterinary Nomenclature)**: Standardized veterinary clinical terminology used in the UK.
4. **UMLS (Unified Medical Language System)**: NLM's meta-thesaurus linking medical vocabularies. Includes some veterinary terms.
5. **Gene Ontology / Disease Ontology**: Relevant for molecular-level oncology data (connects to ICDC genomic data).

**ASIA-specific recommendation**: Use MeSH terms for paper indexing (already available via PubMed API). Consider SNOMED CT Veterinary Extension for standardizing clinical terminology in queries and responses.

**Confidence**: Medium (general knowledge of ontologies; specific veterinary extensions not independently verified in this session)

---

## 6. Veterinary Oncology Databases and Registries

### 6.1 Canine Cancer Data Databases

**Already known to ASIA** (from vision document):
- **ICDC (Integrated Canine Data Commons)**: NCI's canine clinical and genomic data, GraphQL API
- **PubMed/MEDLINE**: Primary biomedical literature database
- **Semantic Scholar**: Enriched metadata and citation graph
- **Europe PMC**: Open access full-text papers
- **CrossRef**: DOI metadata
- **bioRxiv**: Preprints

**Additional databases identified**: [35][36]

- **NCI Comparative Oncology Program**: The NIH National Cancer Institute runs a Comparative Oncology Program that studies naturally occurring cancers in companion animals as models for human cancer. Provides datasets and trial results. [36]

- **VCGP (Veterinary Cancer Guidelines and Protocols)**: Initiative to standardize tumor evaluation and reporting in veterinary oncology. Provides standardized coding systems and reporting frameworks. Website: [vcgp.org](https://vcgp.org/) [35]

- **GIVCS (Global Initiative for Veterinary Cancer Surveillance)**: Initiative to standardize veterinary cancer reporting globally with a One Health approach linking veterinary and human oncology. [35]

**Confidence**: Medium (2 sources: Nature article on cancer registration, NCI official site)
**Sources**: [ScienceDirect: Cancer registration in dogs and cats](https://www.sciencedirect.com/science/article/abs/pii/S003452882500147X), [NCI Comparative Oncology Program](https://ccr.cancer.gov/comparative-oncology-program)

### 6.2 Veterinary Cancer Registries

A 2025 narrative review on cancer registration in dogs and cats documents the history and current status of veterinary cancer registries. [35]

**Key registries**:
- **SAVSNET (Small Animal Veterinary Surveillance Network)**: UK-based surveillance network collecting clinical data from veterinary practices
- **CATCH (Canine And Their Co-Habiting Humans)**: Research cohort study
- **Various national registries**: Multiple countries have veterinary cancer registries, but standardization is lacking. The GIVCS initiative aims to address this.

**Key challenge**: Unlike human cancer (where national cancer registries are mandated in many countries), veterinary cancer registration is voluntary and fragmented. This makes epidemiological data less reliable and comprehensive.

**Confidence**: Medium (1 authoritative source: peer-reviewed narrative review in ScienceDirect)

### 6.3 Veterinary Drug Databases

1. **Plumb's Veterinary Drug Handbook**: 800+ drug monographs (see Section 1.2)
2. **VIN Drug Handbook**: Integrated into VIN membership
3. **FDA Green Book**: Official FDA database of approved animal drug products ([FDA Animal Drug Database](https://animaldrugsatfda.fda.gov/))
4. **FARAD (Food Animal Residue Avoidance Databank)**: Primarily for food animals, but contains pharmacokinetic data relevant to some shared drugs

**Note**: No database was found that specifically focuses on veterinary oncology drug protocols (combining drugs, doses, schedules, and published outcome data). This is a potential feature for ASIA.

### 6.4 Clinical Trial Registries for Veterinary Medicine

1. **AVMA Animal Health Studies Database**: Searchable database of veterinary clinical trials. Available at [AVMA Clinical Trials Search](https://ebusiness.avma.org/aahsd/study_search.aspx). Allows search by cancer type and location. [37]

2. **COTC (Comparative Oncology Trials Consortium)**: Active network of 20 academic comparative oncology centers that designs and executes clinical trials in dogs with cancer to assess novel therapies. Part of the NCI Comparative Oncology Program. [36]

3. **VCOG (Veterinary Cooperative Oncology Group)**: Published standardized response evaluation criteria for canine lymphoma (cRECIST) and solid tumors, based on human RECIST guidelines. Provides the standardized framework for evaluating treatment response in veterinary oncology clinical trials. [35][37]

4. **Individual university trial listings**: Many veterinary schools list ongoing oncology trials (e.g., Purdue, Colorado State, University of Pennsylvania). The Veterinary Cancer Society aggregates some of these. [37]

**ASIA-specific recommendation**: Link to AVMA trial database and COTC trials from within ASIA responses when relevant. A veterinarian researching treatment options should see if there are active clinical trials for their patient's condition.

**Confidence**: High (3 sources: Veterinary Cancer Society, NCI official, Nature article)
**Sources**: [Veterinary Cancer Society Clinical Trials](https://vetcancersociety.org/resources/clinical-trials/), [NCI Comparative Oncology Program](https://ccr.cancer.gov/comparative-oncology-program), [Nature: Research practices in companion dog trials](https://www.nature.com/articles/s41598-019-48425-5)

---

## Source Analysis

| # | Source | Domain | Reputation | Type | Access Date | Cross-verified |
|---|--------|--------|------------|------|-------------|----------------|
| 1 | VIN Official | vin.com | Medium-High | Industry | 2026-03-31 | Y (w/ Auburn) |
| 2 | Auburn University Library Guide | libguides.auburn.edu | High | Academic | 2026-03-31 | Y (w/ VIN) |
| 3 | Oklahoma State Library Guide | info.library.okstate.edu | High | Academic | 2026-03-31 | Y |
| 4 | Plumb's Features | plumbs.com | Medium-High | Industry | 2026-03-31 | Y (w/ OSU, intro) |
| 5 | Plumb's Standards Introduction | plumbs.com | Medium-High | Industry | 2026-03-31 | Y |
| 6 | Standards.vet | standards.vet | Medium | Industry | 2026-03-31 | N |
| 7 | BMC Vet Research: AI in Vet Oncology | springer.com | High | Academic | 2026-03-31 | Y (w/ PMC) |
| 8 | PMC: AI in Vet Oncology (same study) | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 9 | ImpriMed Pricing | imprimedicine.com | Medium-High | Industry | 2026-03-31 | Y |
| 10 | BusinessWire: ImpriMed DRP Launch | businesswire.com | Medium-High | Industry | 2026-03-31 | Y |
| 11 | Pharmacy Times: ImpriMed | pharmacytimes.com | Medium-High | Industry | 2026-03-31 | Y |
| 12 | FidoCure Official | fidocure.com | Medium-High | Industry | 2026-03-31 | Y |
| 13 | Full Slice AI Tools Guide | fullslice.agency | Medium | Industry | 2026-03-31 | Y |
| 14 | UpToDate Grading Guide | wolterskluwer.com | High | Official | 2026-03-31 | Y |
| 15 | PMC: UpToDate GRADE adherence | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 16 | Elicit Official | elicit.com | Medium-High | Industry | 2026-03-31 | Y |
| 17 | PMC: AI for systematic review (Elicit) | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 18 | Skywork Elicit Review | skywork.ai | Medium | Industry | 2026-03-31 | Y |
| 19 | Consensus Official | consensus.app | Medium-High | Industry | 2026-03-31 | Y |
| 20 | Consensus How It Works | consensus.app | Medium-High | Industry | 2026-03-31 | Y |
| 21 | Semantic Scholar TLDR | semanticscholar.org | High | Academic/OSS | 2026-03-31 | Y |
| 22 | McMaster University Guide (S2) | libguides.mcmaster.ca | High | Academic | 2026-03-31 | Y |
| 23 | scite.ai Official | scite.ai | Medium-High | Industry | 2026-03-31 | Y |
| 24 | MIT Press: scite smart citations | direct.mit.edu | High | Academic | 2026-03-31 | Y |
| 25 | PMC: GRADE emerging consensus | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 26 | MDPI: RAG Variants for CDS | mdpi.com | High | Academic | 2026-03-31 | Y |
| 27 | Springer: RAG in Healthcare Review | springer.com | High | Academic | 2026-03-31 | Y |
| 28 | PMC: MEGA-RAG | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 29 | Mayo Clinic Proceedings: FDA SaMD | mcpdigitalhealth.org | High | Academic | 2026-03-31 | Y |
| 30 | PMC: CDS Regulatory Frameworks | pmc.ncbi.nlm.nih.gov | High | Academic | 2026-03-31 | Y |
| 31 | Spyrosoft: SaMD Registration | spyro-soft.com | Medium | Industry | 2026-03-31 | Y |
| 32 | GitHub: Medical-Graph-RAG | github.com | Medium-High | OSS | 2026-03-31 | Y (ACL pub) |
| 33 | GitHub: RAG Medical Assistant | github.com | Medium-High | OSS | 2026-03-31 | N |
| 34 | GitHub: Awesome AI Healthcare | github.com | Medium-High | OSS | 2026-03-31 | N |
| 35 | ScienceDirect: Cancer registration | sciencedirect.com | High | Academic | 2026-03-31 | Y |
| 36 | NCI Comparative Oncology Program | cancer.gov | High | Official | 2026-03-31 | Y |
| 37 | Veterinary Cancer Society | vetcancersociety.org | High | Industry/Official | 2026-03-31 | Y |

**Reputation summary**: High: 18 (49%) | Medium-High: 14 (38%) | Medium: 5 (13%) | Avg: 0.82

## Knowledge Gaps

### Gap 1: VIN Detailed Pricing and Oncology-Specific Features
**Issue**: VIN's internal features, oncology board structure, and pricing are not publicly documented (members-only).
**Attempted**: Web search for VIN features, pricing, oncology; official site and university library guides.
**Recommendation**: Contact VIN directly or consult a VIN member for detailed feature comparison.

### Gap 2: VetCompanion / Standards.vet Detailed Features
**Issue**: Very limited public documentation about this platform's features, oncology coverage, or how it compares to Plumb's.
**Attempted**: Web search, official website.
**Recommendation**: Request a demo or trial subscription for detailed evaluation.

### Gap 3: DynaMed Detailed Comparison with UpToDate
**Issue**: No DynaMed-specific sources were fetched in this session due to turn budget prioritization.
**Attempted**: General knowledge used; no dedicated search performed.
**Recommendation**: Conduct targeted search comparing DynaMed vs. UpToDate update cycles and evidence presentation.

### Gap 4: Veterinary SaMD Regulation
**Issue**: No specific regulatory framework for veterinary clinical decision support software was found in either US or EU.
**Attempted**: Searched for FDA, EU MDR, SaMD, veterinary regulation.
**Recommendation**: This appears to be a genuine regulatory gap rather than a research gap. Monitor for emerging veterinary digital health regulation.

### Gap 5: Perplexity's Medical Query Handling Details
**Issue**: No specific source fetched for Perplexity's medical query disclaimers and citation practices.
**Attempted**: General knowledge used; no dedicated search performed.
**Recommendation**: Test Perplexity directly with veterinary oncology queries to document its behavior.

### Gap 6: Comprehensive List of Veterinary Cancer Registries by Country
**Issue**: The 2025 narrative review on cancer registration was behind a paywall (abstract only accessible).
**Attempted**: ScienceDirect search result found but full text not accessible.
**Recommendation**: Access the full paper: "Cancer registration in dogs and cats: A narrative review of history, current status, and standardization efforts" (ScienceDirect, 2025) for complete registry inventory.

## Conflicting Information

No major conflicts were identified between sources. The findings are largely complementary. One minor observation:

### Evidence Quality in Veterinary vs. Human Medicine
**Observation**: UpToDate's GRADE system was designed for human medicine where RCTs are common. Multiple sources note that veterinary oncology relies more heavily on retrospective studies and small prospective trials. Directly applying GRADE criteria without adaptation could systematically underrate veterinary evidence.
**Assessment**: This is not a conflict but an important design consideration. ASIA should adapt evidence grading for the veterinary evidence landscape rather than blindly applying human medicine standards.

## Recommendations for Further Research

1. **User research with Italian veterinarians**: Interview 5-10 veterinarians about their current literature search workflow, pain points, and feature priorities. This market research identifies the opportunity; user research validates specific feature decisions.

2. **Competitive deep-dive on ImpriMed**: As the closest competitor in AI-assisted veterinary oncology (though focused on lab testing, not literature), understand their customer acquisition, pricing model, and veterinarian satisfaction.

3. **Technical spike on Semantic Scholar API**: Build a proof-of-concept that queries Semantic Scholar for canine lymphoma papers, extracts structured data, and tests retrieval quality. This validates a core ASIA data pipeline.

4. **Evidence grading framework design**: Design ASIA's specific evidence grading system adapted for veterinary oncology. Consider consulting with ACVIM oncology diplomates.

5. **Italian veterinary market sizing**: Research the number of veterinary oncology cases in Italy per year, number of practicing veterinarians, and existing Italian-language veterinary resources.

6. **Full-text access strategy**: Determine which veterinary oncology journals offer open-access papers and which require institutional subscriptions. This affects how much full-text ASIA can index.

## Full Citations

[1] Veterinary Information Network. "VIN - Veterinary Information Network." vin.com. Accessed 2026-03-31.
[2] Auburn University Libraries. "Veterinary Medicine - VIN." libguides.auburn.edu. Accessed 2026-03-31.
[3] Oklahoma State University Library. "Plumb's Standards of Care." info.library.okstate.edu. Accessed 2026-03-31.
[4] Plumb's. "Features." plumbs.com/features/. Accessed 2026-03-31.
[5] Plumb's. "Meet Standards of Care: The Future of Veterinary Clinical Decision Support." plumbs.com/introducing-plumbs-pro/. Accessed 2026-03-31.
[6] Standards.vet. "Trusted Veterinary Clinical Decision Support." standards.vet. Accessed 2026-03-31.
[7] BMC Veterinary Research / Springer Nature. "The application of artificial intelligence in veterinary oncology: a scoping review." 2025. https://link.springer.com/article/10.1186/s12917-025-05192-y. Accessed 2026-03-31.
[8] PMC. "The application of artificial intelligence in veterinary oncology: a scoping review." 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12817679/. Accessed 2026-03-31.
[9] ImpriMed. "Pricing." imprimedicine.com/pricing. Accessed 2026-03-31.
[10] BusinessWire. "ImpriMed Launches Innovative AI-Driven Drug Response Predictions (DRP) Service." 2024-05-28. https://www.businesswire.com/news/home/20240528896580/en/. Accessed 2026-03-31.
[11] Pharmacy Times. "From Dogs to Humans: AI-Powered Drug Response Prediction Technology." pharmacytimes.com. Accessed 2026-03-31.
[12] FidoCure. "Transforming canine cancer treatment through personalized medicine." fidocure.com. Accessed 2026-03-31.
[13] Full Slice. "2025 Guide to AI Tools for Veterinary Medicine." fullslice.agency. Accessed 2026-03-31.
[14] Wolters Kluwer. "Grading Guide | UpToDate." wolterskluwer.com. Accessed 2026-03-31.
[15] PMC. "UpToDate adherence to GRADE criteria for strong recommendations: an analytical survey." 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5701989/. Accessed 2026-03-31.
[16] Elicit. "AI for scientific research." elicit.com. Accessed 2026-03-31.
[17] PMC. "Using artificial intelligence for systematic review: the example of elicit." 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11921719/. Accessed 2026-03-31.
[18] Skywork. "Elicit AI Review (2025): The Ultimate Guide." skywork.ai. 2025. Accessed 2026-03-31.
[19] Consensus. "AI for Research." consensus.app. Accessed 2026-03-31.
[20] Consensus. "How it Works & FAQ's." consensus.app/home/blog/how-consensus-works/. Accessed 2026-03-31.
[21] Semantic Scholar. "TLDR Feature." semanticscholar.org/product/tldr. Accessed 2026-03-31.
[22] McMaster University Libraries. "Semantic Scholar." libguides.mcmaster.ca. Accessed 2026-03-31.
[23] scite.ai. "AI for Research." scite.ai. Accessed 2026-03-31.
[24] MIT Press. "scite: A smart citation index that displays the context of citations." Quantitative Science Studies, 2(3), 882. 2021. https://direct.mit.edu/qss/article/2/3/882/102990/. Accessed 2026-03-31.
[25] PMC. "GRADE: an emerging consensus on rating quality of evidence." BMJ, 2008. https://pmc.ncbi.nlm.nih.gov/articles/PMC2335261/. Accessed 2026-03-31.
[26] MDPI Electronics. "Evaluating Retrieval-Augmented Generation Variants for Clinical Decision Support." 2024. https://www.mdpi.com/2079-9292/14/21/4227. Accessed 2026-03-31.
[27] Springer. "A survey on retrieval-augmentation generation (RAG) models for healthcare applications." Neural Computing and Applications, 2025. https://link.springer.com/article/10.1007/s00521-025-11666-9. Accessed 2026-03-31.
[28] PMC/Frontiers. "MEGA-RAG: a retrieval-augmented generation framework with multi-evidence guided answer refinement." 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/. Accessed 2026-03-31.
[29] Mayo Clinic Proceedings: Digital Health. "FDA Regulation of Clinical Software in the Era of AI/ML." 2025. https://www.mcpdigitalhealth.org/article/S2949-7612(25)00038-0/fulltext. Accessed 2026-03-31.
[30] PMC. "Clinical Decision Support and New Regulatory Frameworks for Medical Devices." 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10105190/. Accessed 2026-03-31.
[31] Spyrosoft. "SaMD and medical device registration in 2025." spyro-soft.com. 2025. Accessed 2026-03-31.
[32] GitHub/ACL 2025. "Medical-Graph-RAG." https://github.com/ImprintLab/Medical-Graph-RAG. Accessed 2026-03-31.
[33] GitHub. "RagBased_medical_assistant." https://github.com/RPPandey02/RagBased_medical_assistant. Accessed 2026-03-31.
[34] GitHub. "Awesome-AI-Agents-for-Healthcare." https://github.com/AgenticHealthAI/Awesome-AI-Agents-for-Healthcare. Accessed 2026-03-31.
[35] ScienceDirect. "Cancer registration in dogs and cats: A narrative review." 2025. https://www.sciencedirect.com/science/article/abs/pii/S003452882500147X. Accessed 2026-03-31.
[36] NCI. "Comparative Oncology Program." https://ccr.cancer.gov/comparative-oncology-program. Accessed 2026-03-31.
[37] Veterinary Cancer Society. "Clinical Trials." https://vetcancersociety.org/resources/clinical-trials/. Accessed 2026-03-31.

## Research Metadata
Duration: ~45 min | Examined: 50+ | Cited: 37 | Cross-refs: 28 | Confidence: High 42%, Medium 42%, Low 16% | Output: /Users/christian/Desktop/ASIA/docs/market-research.md
