# language: en
# Feature: Veterinary Clinical Query Journey
# Persona: Dott.ssa Giulia Mancini, Italian vet, 8 years experience
# Domain: Canine multicentric lymphoma (B-cell, T-cell)

Feature: Clinical Query -- RAG Synthesis in Italian
  As a veterinarian managing a canine lymphoma case
  I need evidence-based answers in Italian with verifiable citations
  So I can make informed treatment decisions quickly

  # ===== STEP 1: ARRIVE =====

  Scenario: Homepage displays pre-loaded queries and search box
    Given Dott.ssa Mancini opens ASIA for the first time
    When the homepage loads
    Then she sees a search box for free-text clinical queries
    And she sees 5 pre-loaded clinical queries as clickable cards
    And she sees a "Crea nuovo caso" button
    And she sees an "Explain a Paper" button
    And a medical disclaimer is visible without scrolling
    And the corpus date is displayed

  Scenario: Disclaimer is always visible and not dismissible
    Given Dott.ssa Mancini is on any page of ASIA
    When she looks for the disclaimer
    Then the text "ASIA e un supporto alla decisione clinica. Non sostituisce il giudizio del veterinario." is visible
    And there is no way to hide or dismiss the disclaimer

  # ===== STEP 2: QUERY =====

  Scenario: Vet clicks a pre-loaded query
    Given Dott.ssa Mancini is on the homepage
    When she clicks the pre-loaded query "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
    Then a streaming response begins within 5 seconds
    And the query text is displayed at the top of the response page
    And a loading indicator is visible immediately

  Scenario: Vet types a free-text query in Italian
    Given Dott.ssa Mancini is on the homepage
    When she types "Effetti collaterali della vincristina nel cane" in the search box
    And she submits the query
    Then a streaming response begins within 5 seconds
    And the query text is displayed at the top of the response page

  # ===== STEP 3: READ =====

  Scenario: Response includes Italian synthesis with sentence-level citations
    Given Dott.ssa Mancini has submitted the query "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
    When the response finishes streaming
    Then she sees a synthesis in Italian of 2-3 sentences
    And each factual claim has an inline citation marker like [1] or [2]
    And she sees an evidence level indicator (ALTO, MODERATO, or BASSO)
    And she sees the number of studies, study types, and total sample size
    And the disclaimer is visible at the bottom

  Scenario: Source panel shows citation details with DOI links
    Given Dott.ssa Mancini is reading a response with citations [1] through [4]
    When she expands the source panel
    Then she sees for each citation: author, year, journal, study type, sample size, and a clickable DOI link
    And the number of source panel entries matches the number of citation markers in the synthesis

  Scenario: Protocol comparison query generates a structured table
    Given Dott.ssa Mancini submits "CHOP-19 vs CHOP-25: differenze negli outcome?"
    When the response finishes streaming
    Then she sees a comparison table with columns for protocol name, drugs, remission rate, median survival, and sample size
    And each row in the table has a citation reference

  Scenario: Response streams via SSE for perceived responsiveness
    Given Dott.ssa Mancini submits a clinical query
    When the backend begins generating the response
    Then text appears word-by-word or sentence-by-sentence on screen
    And the full response does not require waiting for complete generation

  # ===== STEP 4: VERIFY =====

  Scenario: DOI link opens the source paper in a new tab
    Given Dott.ssa Mancini is reading a response with citation [3] referencing Sorenmo et al. (2020)
    When she clicks the DOI link for citation [3]
    Then a new browser tab opens with the paper on the journal website
    And she does not lose her place in ASIA

  Scenario: Citation claim matches the source paper
    Given Dott.ssa Mancini reads that "CHOP-19 e CHOP-25 hanno outcome equivalenti [3]"
    When she verifies citation [3] against the source paper
    Then the claim in the synthesis accurately reflects the paper's findings

  # ===== STEP 5: DECIDE =====

  Scenario: Vet asks a follow-up question from the response page
    Given Dott.ssa Mancini has read a response about CHOP protocols
    When she types "Aggiustamento dose doxorubicina per neutropenia?" in the search box
    Then a new streaming response begins
    And the previous response remains accessible

  # ===== EXPLAIN THIS PAPER =====

  Scenario: Vet gets a clinical summary from a DOI
    Given Dott.ssa Mancini navigates to "Explain a Paper"
    When she pastes the DOI "10.1111/vco.12345"
    And clicks "Analizza"
    Then she sees a structured clinical summary in Italian with sections for:
      | Section                    |
      | Obiettivo dello studio     |
      | Metodologia e qualita      |
      | Risultati chiave           |
      | Implicazioni pratiche      |
      | Contesto nel corpus ASIA   |

  # ===== CASE MODE =====

  Scenario: Vet creates a new case
    Given Dott.ssa Mancini clicks "Crea nuovo caso" on the homepage
    When she fills in the case form:
      | Campo          | Valore                      |
      | Nome paziente  | Luna                        |
      | Razza          | Golden Retriever            |
      | Eta            | 7 anni                      |
      | Diagnosi       | Linfoma multicentrico       |
      | Stadio         | III                         |
      | Immunofenotipo | B-cell                      |
      | Note           | Substadio a, buone condizioni generali |
    And she clicks "Crea caso"
    Then the case "Luna" is created
    And she is redirected to the case page showing the case details

  Scenario: Query within a case injects patient context automatically
    Given Dott.ssa Mancini has created the case "Luna" (Golden Retriever, 7 anni, linfoma multicentrico B-cell stadio IIIa)
    When she types "Qual e il protocollo migliore?" within the case
    Then the RAG query includes the case context (breed, age, diagnosis, stage, immunophenotype)
    And the response is more specific than a context-free query
    And the query appears in the case history with a timestamp

  Scenario: Case history shows chronological query list
    Given Dott.ssa Mancini has made 3 queries within the case "Luna"
    When she views the case page
    Then she sees all 3 queries listed chronologically with timestamps
    And she can click any query to see its full response

  # ===== ERROR PATHS =====

  Scenario: No evidence found for out-of-scope query
    Given Dott.ssa Mancini submits "Trattamento osteosarcoma felino"
    When the RAG pipeline finds insufficient evidence
    Then she sees a message: "Non sono state trovate evidenze sufficienti nel corpus"
    And the message explains the current corpus scope (linfoma multicentrico canino)
    And suggestions are provided: rephrase, try pre-loaded queries, or consult PubMed

  Scenario: Slow response shows progress indicator
    Given Dott.ssa Mancini submits a complex query
    When the response takes more than 10 seconds
    Then she sees a progress indicator showing the number of papers being analyzed
    And an estimated time is displayed

  Scenario: Self-reflective RAG removes an unverified citation
    Given the RAG pipeline initially identifies 5 citations for a query
    When the verification pass detects that citation [4] does not support the stated claim
    Then citation [4] is removed from the synthesis
    And a note explains that a citation was removed for quality assurance
    And the final response contains only verified citations

  # ===== NON-FUNCTIONAL (as @property) =====

  @property
  Scenario: Response time under normal load
    Given ASIA is running on the demo infrastructure
    Then streaming response begins within 5 seconds of query submission
    And complete response is delivered within 30 seconds for typical queries

  @property
  Scenario: Italian medical terminology quality
    Given any clinical query about canine multicentric lymphoma
    Then the Italian synthesis uses correct veterinary medical terminology
    And the language reads naturally to a native Italian speaker

  @property
  Scenario: Citation accuracy
    Given any response with inline citations
    Then every citation marker [n] corresponds to a real, published paper
    And every cited claim accurately reflects the source paper's findings
    And no hallucinated papers or fabricated DOIs appear in responses

  @property
  Scenario: Disclaimer persistence
    Given any page in the ASIA application
    Then the medical disclaimer is visible
    And it cannot be hidden or dismissed by the user
