<!-- markdownlint-disable MD024 -->

# User Stories: ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Total stories**: 7 (Walking Skeleton: 2, Release 1: 3, Release 2: 2)

---

## US-01: Homepage and Medical Disclaimer

### Problem

Dott.ssa Giulia Mancini is a veterinarian in Bologna who manages 3-5 oncology cases per month. When she first opens ASIA, she needs to understand what the tool does and trust that it takes medical responsibility seriously. Without a clear entry point and a persistent disclaimer, she will not engage further.

### Who

- Italian veterinarian | First-time visitor | Needs to understand what ASIA offers and trust it enough to try a query

### Solution

A clean, professional homepage with a search box for clinical queries, navigation to Case Mode and Explain a Paper, and a medical disclaimer that is always visible and never dismissible.

### Domain Examples

#### 1: First Visit -- Dott.ssa Mancini Arrives

Dott.ssa Giulia Mancini (veterinaria generalista, Clinica Veterinaria San Luca, Bologna) opens ASIA on her clinic tablet. She sees the ASIA logo, a search box labeled "Scrivi la tua domanda clinica...", and a disclaimer: "ASIA e un supporto alla decisione clinica basato sulla letteratura scientifica. Non sostituisce il giudizio del veterinario." She also sees the corpus date: "Corpus aggiornato al: marzo 2026." She feels the tool is professional, not a toy.

#### 2: Navigation -- Finding Case Mode

Dott.ssa Mancini sees a "Crea nuovo caso" button below the search area. She also sees "Explain a Paper." Both are clearly labeled and accessible without scrolling on her 10" tablet.

#### 3: Disclaimer Persistence -- Scrolling the Page

After interacting with ASIA for several queries, Dott.ssa Mancini notices the disclaimer is still visible at the bottom of every page. She cannot dismiss it. This is intentional -- in a medical context, the disclaimer must always be visible.

### UAT Scenarios (BDD)

#### Scenario: Homepage renders with core elements

```gherkin
Given Dott.ssa Mancini opens ASIA for the first time on her tablet
When the homepage finishes loading
Then she sees a search box with placeholder text "Scrivi la tua domanda clinica..."
And she sees a "Crea nuovo caso" button
And she sees an "Explain a Paper" button
And the medical disclaimer is visible without scrolling
And the corpus date is displayed
```

#### Scenario: Disclaimer is visible on every page

```gherkin
Given Dott.ssa Mancini navigates from the homepage to a response page
When the response page loads
Then the medical disclaimer is visible
And the disclaimer text matches the homepage disclaimer exactly
```

#### Scenario: Disclaimer cannot be dismissed

```gherkin
Given Dott.ssa Mancini is viewing any page in ASIA
When she looks for a way to hide or dismiss the disclaimer
Then no dismiss button, close icon, or hide mechanism exists
```

#### Scenario: Homepage is usable on tablet

```gherkin
Given Dott.ssa Mancini opens ASIA on a 10-inch tablet in portrait orientation
When the homepage loads
Then the search box, disclaimer, and navigation elements fit without horizontal scrolling
And touch targets are at least 44x44 pixels
```

### Acceptance Criteria

- [ ] Homepage displays search box, Case Mode button, Explain a Paper button
- [ ] Medical disclaimer is visible on every page without scrolling
- [ ] Disclaimer cannot be hidden or dismissed
- [ ] Corpus date is displayed and matches actual ingestion date
- [ ] Layout works on tablet (10") and desktop without horizontal scrolling
- [ ] All touch targets are at least 44x44px

### Outcome KPIs

- **Who**: Vet seeing ASIA for the first time
- **Does what**: Understands what ASIA offers within 10 seconds of loading
- **By how much**: 0 vets ask "what is this?" or "how do I use this?"
- **Measured by**: Observation during demo
- **Baseline**: N/A (new product)

### Technical Notes (Optional)

- Next.js + TypeScript + Tailwind CSS
- Tablet-first responsive design (breakpoints: 768px tablet, 1024px+ desktop)
- Disclaimer text sourced from a single constant (shared artifact)
- Corpus date fetched from backend API (ingestion metadata)
- No authentication required for MVP

---

## US-02: Clinical Query with RAG Synthesis

### Problem

Dott.ssa Giulia Mancini has a Golden Retriever with newly diagnosed B-cell lymphoma and needs to know the first-line protocol. Today she would spend 30-60 minutes reading English papers on PubMed. She needs a synthesized, cited answer in Italian in under 2 minutes.

### Who

- Italian veterinarian | Managing an active oncology case | Needs evidence-based answer fast, in Italian, with verifiable citations

### Solution

A RAG-powered clinical query interface that accepts Italian natural language questions and returns a streaming synthesis in Italian with sentence-level citations, evidence level indicator, and an expandable source panel with DOI links.

### Domain Examples

#### 1: Happy Path -- First-Line Protocol Query

Dott.ssa Mancini types "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?" She gets a streaming response: "Il protocollo raccomandato e il CHOP... [1][2]" with evidence level MODERATO, 4 studies cited, and DOI links to Garrett (2002), Simon (2006), Sorenmo (2020), and Vail (2013). She clicks the Sorenmo DOI and it opens the real paper in a new tab.

#### 2: Edge Case -- Ambiguous Query

Dott.ssa Mancini types "linfoma cane cosa fare" -- a vague query. The RAG returns a broader synthesis about canine lymphoma management with a note: "Per una risposta piu specifica, includi lo stadio, l'immunofenotipo e la situazione clinica." Citations are still provided.

#### 3: Error -- Out of Scope Query

Dott.ssa Mancini types "Trattamento osteosarcoma felino." The RAG finds insufficient evidence in the canine lymphoma corpus and returns: "Non sono state trovate evidenze sufficienti nel corpus per rispondere a questa domanda." It suggests rephasing, trying a pre-loaded query, or consulting PubMed directly.

### UAT Scenarios (BDD)

#### Scenario: Successful clinical query with cited synthesis

```gherkin
Given Dott.ssa Mancini is on the ASIA homepage
When she types "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
And submits the query
Then a streaming response begins within 5 seconds
And the response is a synthesis in Italian of 2-3 sentences
And each factual claim has an inline citation marker [1], [2], etc.
And an evidence level indicator shows ALTO, MODERATO, or BASSO
And the number of studies and total sample size are displayed
And an expandable source panel lists each citation with author, year, journal, study type, sample size, and DOI link
```

#### Scenario: DOI link resolves to a real paper

```gherkin
Given Dott.ssa Mancini is reading a response with citation [3] referencing Sorenmo et al. (2020)
When she clicks the DOI link for citation [3]
Then a new browser tab opens showing the paper on the journal website
And her ASIA page is not lost or navigated away from
```

#### Scenario: Citation markers match source panel entries

```gherkin
Given Dott.ssa Mancini reads a response with citations [1] through [4]
When she expands the source panel
Then the source panel contains exactly 4 entries
And entry [1] matches the first citation marker in the text
And entry [4] matches the fourth citation marker in the text
```

#### Scenario: Streaming response for perceived responsiveness

```gherkin
Given Dott.ssa Mancini submits a clinical query
When the backend begins generating the response
Then text appears incrementally on screen via SSE
And she does not have to wait for the complete response before reading
```

#### Scenario: Insufficient evidence response

```gherkin
Given Dott.ssa Mancini submits "Trattamento osteosarcoma felino"
When the RAG pipeline finds insufficient evidence in the corpus
Then she sees "Non sono state trovate evidenze sufficienti nel corpus"
And the message explains the current corpus scope
And suggestions are provided to rephrase, try pre-loaded queries, or consult PubMed
```

### Acceptance Criteria

- [ ] Free-text Italian queries accepted and processed by RAG pipeline
- [ ] Response streams via SSE, beginning within 5 seconds
- [ ] Synthesis is in Italian with correct veterinary medical terminology
- [ ] Every factual claim has a sentence-level citation marker
- [ ] Citation markers match source panel entries 1:1
- [ ] Source panel shows author, year, journal, study type, sample size, DOI
- [ ] DOI links open in new tab and resolve to real papers
- [ ] Evidence level indicator (ALTO/MODERATO/BASSO) displayed
- [ ] Out-of-scope queries receive honest "no evidence" response with suggestions
- [ ] Complete response delivered within 30 seconds for typical queries
- [ ] Disclaimer visible on response page

### Outcome KPIs

- **Who**: Vet asking a clinical question
- **Does what**: Gets an accurate, cited answer in Italian
- **By how much**: 4/5 critical queries rated >= 4/5 accuracy by vet team
- **Measured by**: Questionnaire Part 2, Q19
- **Baseline**: 0 (no tool exists)

### Technical Notes (Optional)

- FastAPI backend with SSE streaming endpoint
- RAG pipeline: query embedding -> pgvector retrieval -> LLM synthesis -> self-reflective citation verification
- Groq free tier (Llama 3.3 70B) with LLM adapter pattern for future provider swap
- Self-reflective RAG: generate, verify citations, refine (max 2 iterations)
- Confidence threshold: below threshold, return "no evidence" response
- Dependency: US-01 (homepage provides entry point), ingestion pipeline (corpus must be populated)

---

## US-03: Pre-loaded Clinical Queries

### Problem

Dott.ssa Mancini is seeing ASIA for the first time during the demo. If her first query produces a poor result, trust is permanently damaged. Pre-loaded queries guarantee a high-quality first impression with tested, validated responses.

### Who

- Italian veterinarian | First-time user during demo | Needs a safe, high-quality first experience to build trust

### Solution

Five pre-loaded clinical queries displayed as clickable cards on the homepage. Clicking a card submits the query to the RAG pipeline (not hardcoded responses). The queries have been pre-tested and validated for accuracy.

### Domain Examples

#### 1: Happy Path -- Clicking the First Query

Dott.ssa Mancini clicks "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?" She gets the same RAG-generated response as if she had typed it, but the query was guaranteed to work well.

#### 2: Demo Safety -- All 5 Queries Produce Quality Answers

Dr. Marco Rossi (oncologo veterinario, Clinica Universitaria Bologna) clicks through all 5 pre-loaded queries during the demo. Each produces an accurate, well-cited response. He recognizes the papers cited and the clinical recommendations align with his practice.

#### 3: Transition -- Moving from Pre-loaded to Free Query

After trying 2 pre-loaded queries, Dott.ssa Mancini types her own question: "Tossicita epatica della lomustina nel cane?" She gets a response from the RAG, transitioning naturally from guided to free exploration.

### UAT Scenarios (BDD)

#### Scenario: Pre-loaded queries displayed as clickable cards

```gherkin
Given Dott.ssa Mancini is on the ASIA homepage
When the page loads
Then she sees 5 pre-loaded clinical queries as clickable cards:
  | Query |
  | Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III? |
  | CHOP-19 vs CHOP-25: differenze negli outcome? |
  | Protocolli di rescue per recidiva precoce dopo CHOP? |
  | Prognosi linfoma T-cell vs B-cell? |
  | Aggiustamento dose doxorubicina per neutropenia? |
```

#### Scenario: Clicking a pre-loaded query submits to RAG

```gherkin
Given Dott.ssa Mancini sees the pre-loaded query "CHOP-19 vs CHOP-25: differenze negli outcome?"
When she clicks the query card
Then the query is submitted to the RAG pipeline (not a hardcoded response)
And a streaming response begins within 5 seconds
And the response page shows the query text at the top
```

#### Scenario: All 5 critical queries produce accurate responses

```gherkin
Given each of the 5 pre-loaded queries is submitted to ASIA
When the responses are reviewed by Dr. Marco Rossi (oncologo veterinario)
Then at least 4 of 5 responses are rated >= 4/5 for accuracy
And 0 responses contain factual errors with clinical impact
And all citation DOIs resolve to real, relevant papers
```

### Acceptance Criteria

- [ ] 5 pre-loaded queries displayed as clickable cards on homepage
- [ ] Clicking a card submits to RAG (not hardcoded responses)
- [ ] Query text displayed on response page matches the card text
- [ ] All 5 queries produce responses with citations and evidence levels
- [ ] Pre-tested: 0 factual errors, 0 hallucinated citations across all 5 queries

### Outcome KPIs

- **Who**: Vet team during demo
- **Does what**: Click pre-loaded queries and rate responses as accurate
- **By how much**: 4/5 queries rated >= 4/5 accuracy
- **Measured by**: Questionnaire Part 2, Q19
- **Baseline**: 0 (no prior demo)

### Technical Notes (Optional)

- Pre-loaded query texts stored in backend config (single source of truth)
- Responses are live RAG, not cached -- but should be pre-tested before demo
- Consider pre-warming the RAG cache for these 5 queries for faster demo response
- Dependency: US-02 (RAG query must work)

---

## US-04: Protocol Comparison Table

### Problem

When Dott.ssa Mancini needs to compare CHOP-19 vs CHOP-25 vs COP, today she reads 5-10 papers and mentally assembles the comparison. A structured table with remission rates, survival data, and evidence level side-by-side would save her 30+ minutes and reduce comparison errors.

### Who

- Italian veterinarian | Choosing between treatment protocols | Needs structured side-by-side data with citations

### Solution

When a clinical query involves comparing protocols, the RAG response includes an auto-generated comparison table with columns for protocol name, drugs, remission rate, median survival, study type, sample size, and citation reference.

### Domain Examples

#### 1: Happy Path -- CHOP-19 vs CHOP-25

Dott.ssa Mancini asks "CHOP-19 vs CHOP-25: differenze negli outcome?" The response includes a synthesis paragraph plus a table showing CHOP-19 and CHOP-25 side by side: same drugs, same remission (80-90%), same survival (10-12 months B-cell), n=408, citing Sorenmo et al. (2020). Below the table: COP as alternative with 60-70% remission, 6-8 months survival.

#### 2: Three-Way Comparison -- Including COP

Dr. Marco Rossi asks "Confronto CHOP, COP e monochemioterapia doxorubicina per linfoma B-cell." The table shows all three protocols with their respective data and citations. The synthesis notes that CHOP-based protocols are superior but COP is an option for cost-sensitive owners.

#### 3: No Comparison Applicable

Dott.ssa Mancini asks "Qual e la prognosi per linfoma T-cell stadio V?" This is not a comparison query. The response is a standard synthesis without a comparison table.

### UAT Scenarios (BDD)

#### Scenario: Comparison query generates a structured table

```gherkin
Given Dott.ssa Mancini submits "CHOP-19 vs CHOP-25: differenze negli outcome?"
When the response finishes streaming
Then the response includes a comparison table
And the table has columns for: protocol, drugs, remission rate, median survival, sample size
And each row has a citation reference
And the table data is consistent with the cited papers
```

#### Scenario: Non-comparison query does not show a table

```gherkin
Given Dott.ssa Mancini submits "Prognosi linfoma T-cell vs B-cell?"
When the response finishes streaming
Then the response is a synthesis with citations
And no comparison table is displayed (this is a prognosis query, not a protocol comparison)
```

#### Scenario: Table data matches cited sources

```gherkin
Given the comparison table shows CHOP-19 with 80-90% remission rate citing Sorenmo et al. (2020)
When Dr. Marco Rossi verifies the claim against the cited paper
Then the remission rate in the table matches the paper's reported data
```

### Acceptance Criteria

- [ ] Comparison queries trigger auto-generated comparison table in response
- [ ] Table includes protocol name, drugs, remission rate, median survival, sample size, citation
- [ ] Non-comparison queries do not display a table
- [ ] Table data is consistent with cited sources
- [ ] Table renders correctly on tablet and desktop

### Outcome KPIs

- **Who**: Vet comparing treatment protocols
- **Does what**: Gets a structured side-by-side comparison from literature
- **By how much**: Comparison table generated for at least 1 of the 5 critical queries (Q2)
- **Measured by**: Demo observation
- **Baseline**: 0 (no tool generates comparison tables from vet oncology literature)

### Technical Notes (Optional)

- Table generation is part of the RAG synthesis prompt, not a separate module
- LLM extracts structured data from retrieved papers and formats as table
- Detection of "comparison query" can be prompt-based (LLM decides) or keyword-based
- Dependency: US-02 (RAG response format must support structured output)

---

## US-05: Graceful Error Handling

### Problem

Dott.ssa Mancini asks a question outside the corpus scope or encounters a slow response. If ASIA fails silently, shows a raw error, or fabricates an answer, her trust is destroyed. She needs honest, helpful error handling that respects her intelligence and time.

### Who

- Italian veterinarian | Encountering an error or edge case | Needs clear guidance, not blame or silence

### Solution

Three error handling patterns: (1) no evidence found -- honest message with scope explanation and suggestions, (2) slow response -- progress indicator with paper count, (3) citation quality issue -- transparent note about self-correction.

### Domain Examples

#### 1: Out of Scope -- Feline Osteosarcoma

Dott.ssa Mancini types "Trattamento osteosarcoma felino." ASIA responds: "Non sono state trovate evidenze sufficienti nel corpus per rispondere a questa domanda. Il corpus attuale copre il linfoma multicentrico canino." Suggestions: rephrase with canine lymphoma terms, try a pre-loaded query, or search PubMed directly (with a link).

#### 2: Slow Response -- Complex Multi-Paper Analysis

Dott.ssa Mancini asks a complex question requiring analysis of 15 papers. After 10 seconds without a response, she sees: "Analisi della letteratura in corso... Sto analizzando 15 paper rilevanti. Tempo stimato: ~20 secondi" with a progress bar.

#### 3: Self-Correction -- Citation Removed

The RAG pipeline initially identifies 5 citations but the self-reflective pass detects that citation [4] does not support the stated claim. The final response includes 4 citations and a note: "Una citazione inizialmente identificata e stata rimossa perche non supportava adeguatamente l'affermazione."

### UAT Scenarios (BDD)

#### Scenario: Out-of-scope query returns honest no-evidence message

```gherkin
Given Dott.ssa Mancini submits "Trattamento osteosarcoma felino"
When the RAG pipeline finds insufficient evidence
Then she sees "Non sono state trovate evidenze sufficienti nel corpus"
And the corpus scope is explained (linfoma multicentrico canino)
And she sees suggestions: rephrase, try pre-loaded queries, consult PubMed
And a direct PubMed search link is provided
```

#### Scenario: Slow response shows progress indicator

```gherkin
Given Dott.ssa Mancini submits a complex query
When the response takes more than 10 seconds
Then a progress indicator appears showing the number of papers being analyzed
And an estimated completion time is displayed
And the indicator updates as analysis progresses
```

#### Scenario: Self-reflective RAG removes unverified citation

```gherkin
Given the RAG pipeline generates a response with 5 citations
When the self-reflective verification detects citation [4] does not support the claim
Then citation [4] is removed from the final response
And the synthesis is adjusted to remove the unsupported claim
And a transparency note explains that a citation was removed for quality assurance
```

#### Scenario: ASIA never fabricates an answer when evidence is insufficient

```gherkin
Given the corpus has no papers relevant to the submitted query
When Dott.ssa Mancini reads the response
Then the response does not contain any synthesis or clinical recommendations
And no citations are fabricated
And the response honestly states that insufficient evidence was found
```

### Acceptance Criteria

- [ ] Out-of-scope queries return "no evidence" message with scope explanation and suggestions
- [ ] Slow responses (>10s) show progress indicator with paper count
- [ ] Self-reflective RAG can remove unverified citations and show transparency note
- [ ] ASIA never fabricates answers or citations when evidence is insufficient
- [ ] Error messages are in Italian, empathetic, and suggest concrete next steps
- [ ] No raw error codes or stack traces shown to the user

### Outcome KPIs

- **Who**: Vet encountering an edge case
- **Does what**: Receives helpful guidance instead of a broken experience
- **By how much**: 0 instances of raw errors, blank screens, or fabricated answers during demo
- **Measured by**: Observation during demo
- **Baseline**: N/A

### Technical Notes (Optional)

- Confidence threshold in RAG pipeline determines when to show "no evidence" vs synthesis
- Self-reflective RAG: max 2 verification iterations per response
- Progress indicator requires SSE heartbeat messages during processing
- PubMed search link can be constructed from the query text programmatically
- Dependency: US-02 (RAG pipeline must support confidence scoring and self-reflection)

---

## US-06: Basic Case Mode

### Problem

Dott.ssa Mancini manages the case of Luna (Golden Retriever, 7 anni, linfoma B-cell stadio IIIa) over several weeks. Each time she queries ASIA, she has to re-type the patient context. She needs a persistent case that stores patient info, tracks query history, and automatically injects clinical context into RAG queries.

### Who

- Italian veterinarian | Managing an ongoing oncology case over weeks | Needs persistent context and query history per patient

### Solution

A case creation form (patient name, breed, age, diagnosis, stage, immunophenotype, notes), a case page with query history, and automatic context injection: when a vet queries within a case, the patient data is included in the RAG prompt for more specific answers.

### Domain Examples

#### 1: Happy Path -- Creating a Case for Luna

Dott.ssa Mancini clicks "Crea nuovo caso" and fills in: Nome: Luna, Razza: Golden Retriever, Eta: 7 anni, Diagnosi: Linfoma multicentrico, Stadio: III, Immunofenotipo: B-cell, Note: "Substadio a, buone condizioni generali." She creates the case and is redirected to Luna's case page.

#### 2: Context Injection -- Query Within a Case

Inside Luna's case, Dott.ssa Mancini types "Qual e il protocollo migliore?" The RAG receives: "Contesto: Golden Retriever, 7 anni, linfoma multicentrico B-cell, stadio IIIa, substadio a, buone condizioni generali. Domanda: Qual e il protocollo migliore?" The response is more specific than a context-free query -- it mentions age and breed-specific considerations.

#### 3: Case History -- Reviewing Past Queries

After 3 weeks and 5 queries, Dott.ssa Mancini opens Luna's case page. She sees all 5 queries listed chronologically: "[14:32 - 15 Mar] Qual e il protocollo migliore?", "[09:15 - 22 Mar] Neutropenia grado 2 dopo prima dose doxorubicina?", etc. She clicks any query to re-read the full response.

### UAT Scenarios (BDD)

#### Scenario: Create a new case with patient information

```gherkin
Given Dott.ssa Mancini clicks "Crea nuovo caso"
When she fills in: Nome "Luna", Razza "Golden Retriever", Eta "7 anni", Diagnosi "Linfoma multicentrico", Stadio "III", Immunofenotipo "B-cell", Note "Substadio a, buone condizioni generali"
And clicks "Crea caso"
Then the case "Luna" is created and stored
And she is redirected to the case page showing all entered details
```

#### Scenario: Query within a case auto-injects patient context

```gherkin
Given Dott.ssa Mancini is on the case page for "Luna" (Golden Retriever, 7 anni, B-cell, stadio IIIa)
When she types "Qual e il protocollo migliore?" and submits
Then the RAG query includes Luna's case data as context
And the response references breed, age, or stage-specific considerations
And the query and response are saved in Luna's case history
```

#### Scenario: Case history displays all queries chronologically

```gherkin
Given Dott.ssa Mancini has made 3 queries within the case "Luna"
When she views Luna's case page
Then she sees all 3 queries listed with timestamps
And she can click any query to view its full response
And the most recent query appears at the top
```

#### Scenario: Case can be created with minimal fields

```gherkin
Given Dott.ssa Mancini clicks "Crea nuovo caso"
When she fills in only Nome "Rex" and Diagnosi "Linfoma multicentrico"
And clicks "Crea caso"
Then the case "Rex" is created with the available information
And optional fields (Razza, Eta, Stadio, Immunofenotipo, Note) are stored as empty
```

### Acceptance Criteria

- [ ] Case creation form with fields: nome, razza, eta, diagnosi, stadio, immunofenotipo, note
- [ ] Only nome and diagnosi are required; other fields are optional
- [ ] Case page displays all entered patient details
- [ ] Queries within a case auto-inject patient data into RAG prompt
- [ ] Query history is stored and displayed chronologically per case
- [ ] Clicking a past query shows the full response
- [ ] Case data persists across browser sessions (stored in PostgreSQL)

### Outcome KPIs

- **Who**: Vet managing an ongoing case
- **Does what**: Creates a case and makes context-aware queries
- **By how much**: At least 1 vet creates a case during or after demo
- **Measured by**: Database records + demo observation
- **Baseline**: 0 (no case management tool exists for vet oncology evidence)

### Technical Notes (Optional)

- PostgreSQL table: cases (id, patient_name, breed, age, diagnosis, stage, immunophenotype, notes, created_at)
- PostgreSQL table: case_queries (id, case_id, query_text, response_text, created_at)
- Context injection: prepend case data to RAG prompt before LLM call
- No case sharing, export, or deletion in MVP
- Dependency: US-01 (homepage CTA), US-02 (RAG query pipeline)

---

## US-07: Explain This Paper

### Problem

Dott.ssa Mancini found a paper cited in ASIA's response (Sorenmo et al. 2020) and wants to understand it in depth. Reading the full paper in English would take 45 minutes. She needs a structured clinical summary in Italian: what was studied, how, what they found, and what it means for her practice.

### Who

- Italian veterinarian | Found a paper through ASIA or has a DOI from a colleague | Needs a quick clinical summary in Italian

### Solution

An "Explain This Paper" interface where the vet pastes a DOI or paper title. ASIA retrieves the paper from its corpus (or searches PubMed/Semantic Scholar) and generates a structured clinical summary in Italian with sections for objective, methodology, key results, practical implications, and positioning within the ASIA corpus.

### Domain Examples

#### 1: Happy Path -- Paper in Corpus

Dott.ssa Mancini pastes "10.1111/vco.12345" (Sorenmo et al. 2020, CHOP-19 vs CHOP-25). ASIA finds it in the corpus and generates: Obiettivo: Confrontare CHOP-19 e CHOP-25 per efficacia e tossicita. Metodologia: Prospettico multicentrico randomizzato, n=408, 12 centri europei. Quality: ALTA. Risultati: Nessuna differenza significativa. Implicazioni: CHOP-19 preferibile per durata minore. Contesto: Conferma e aggiorna Garrett (2002) e Simon (2006).

#### 2: Edge Case -- Paper Not in Corpus

Dott.ssa Mancini pastes a DOI for a recent paper not yet in the ASIA corpus. ASIA retrieves the abstract from PubMed and generates a summary based on the abstract only, with a note: "Riassunto basato solo sull'abstract. Il paper completo non e nel corpus ASIA."

#### 3: Error -- Invalid DOI

Dott.ssa Mancini pastes "10.9999/nonexistent" -- an invalid DOI. ASIA responds: "Non e stato possibile trovare un paper con questo DOI. Verifica che il DOI sia corretto, oppure prova con il titolo del paper."

### UAT Scenarios (BDD)

#### Scenario: Explain a paper in the corpus

```gherkin
Given Dott.ssa Mancini navigates to "Explain a Paper"
When she pastes the DOI "10.1111/vco.12345" and clicks "Analizza"
Then ASIA retrieves the paper from its corpus
And displays a structured clinical summary in Italian with sections:
  | Section                    |
  | Obiettivo dello studio     |
  | Metodologia e qualita      |
  | Risultati chiave           |
  | Implicazioni pratiche      |
  | Contesto nel corpus ASIA   |
```

#### Scenario: Explain a paper not in the corpus

```gherkin
Given Dott.ssa Mancini pastes a DOI for a paper not in the ASIA corpus
When she clicks "Analizza"
Then ASIA retrieves the abstract from PubMed or Semantic Scholar
And generates a summary based on the abstract
And a note warns: "Riassunto basato solo sull'abstract"
```

#### Scenario: Invalid DOI returns helpful error

```gherkin
Given Dott.ssa Mancini pastes "10.9999/nonexistent"
When she clicks "Analizza"
Then she sees "Non e stato possibile trovare un paper con questo DOI"
And a suggestion to verify the DOI or try the paper title instead
```

### Acceptance Criteria

- [ ] DOI input field with "Analizza" button
- [ ] Papers in corpus: full structured summary with 5 sections
- [ ] Papers not in corpus: abstract-based summary with warning note
- [ ] Invalid DOI: helpful error message with suggestion
- [ ] Summary is in Italian with correct medical terminology
- [ ] Paper title input accepted as alternative to DOI

### Outcome KPIs

- **Who**: Vet wanting to understand a specific paper
- **Does what**: Gets a structured clinical summary in Italian from a DOI
- **By how much**: Summary generated for at least 1 paper during demo
- **Measured by**: Demo observation
- **Baseline**: 0 (no tool generates Italian clinical summaries of vet oncology papers)

### Technical Notes (Optional)

- DOI resolution: first check local corpus (pgvector metadata), then PubMed E-utilities, then Semantic Scholar API
- Summary generated by LLM with structured prompt (5-section template)
- For corpus papers: full metadata + abstract available. For external: abstract only.
- Dependency: US-01 (homepage CTA), ingestion pipeline (corpus metadata with DOIs)

---

## Definition of Ready Validation

### Summary

| Story | Problem | Persona | Examples (3+) | UAT (3-7) | AC from UAT | Right-sized | Tech Notes | Dependencies | KPIs | Status |
|-------|---------|---------|---------------|-----------|-------------|-------------|------------|--------------|------|--------|
| US-01 | PASS | PASS | 3 | 4 | PASS | 1 day | PASS | None | PASS | READY |
| US-02 | PASS | PASS | 3 | 5 | PASS | 2-3 days | PASS | US-01, ingestion | PASS | READY |
| US-03 | PASS | PASS | 3 | 3 | PASS | 1 day | PASS | US-02 | PASS | READY |
| US-04 | PASS | PASS | 3 | 3 | PASS | 1-2 days | PASS | US-02 | PASS | READY |
| US-05 | PASS | PASS | 3 | 4 | PASS | 1-2 days | PASS | US-02 | PASS | READY |
| US-06 | PASS | PASS | 4 | 4 | PASS | 2-3 days | PASS | US-01, US-02 | PASS | READY |
| US-07 | PASS | PASS | 3 | 3 | PASS | 1-2 days | PASS | US-01, ingestion | PASS | READY |

### DoR Status: ALL PASSED

All 7 stories pass the 9-item Definition of Ready checklist (problem + persona + examples + UAT + AC + right-sized + tech notes + dependencies + KPIs).
