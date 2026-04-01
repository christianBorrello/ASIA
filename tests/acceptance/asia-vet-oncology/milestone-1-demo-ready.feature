# language: en
Feature: Milestone 1 -- Demo Ready
  As a veterinarian evaluating ASIA during a demo
  I need pre-loaded queries that produce accurate responses,
  a protocol comparison table, and graceful error handling
  So I can trust ASIA as a reliable clinical decision support tool

  Stories: US-03, US-04, US-05

  Background:
    Given the ASIA application is running
    And the corpus contains papers about canine multicentric lymphoma

  # ===== US-03: Pre-loaded Clinical Queries =====

  @US-03
  Scenario: Homepage displays five pre-loaded clinical queries as clickable cards
    Given Dott.ssa Mancini opens the ASIA homepage
    When the page finishes loading
    Then she sees 5 pre-loaded clinical queries as clickable cards
    And the queries cover first-line protocol, protocol comparison, rescue protocols, prognosis, and dose adjustment

  @US-03
  Scenario: Clicking a pre-loaded query submits it to the evidence pipeline
    Given Dott.ssa Mancini sees the pre-loaded query "CHOP-19 vs CHOP-25: differenze negli outcome?"
    When she clicks the query card
    Then the query is submitted for evidence synthesis
    And a streaming response begins
    And the query text is displayed at the top of the response

  @US-03
  Scenario: First-line protocol query produces an accurate cited response
    Given the pre-loaded query "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?" is submitted
    When the response is complete
    Then the synthesis mentions the CHOP protocol
    And the synthesis mentions remission rates
    And the response includes citations from relevant lymphoma studies
    And no citation refers to a non-existent paper

  @US-03
  Scenario: Protocol comparison query produces an accurate cited response
    Given the pre-loaded query "CHOP-19 vs CHOP-25: differenze negli outcome?" is submitted
    When the response is complete
    Then the synthesis discusses outcome equivalence between the protocols
    And the response cites the Sorenmo multicenter study
    And no citation refers to a non-existent paper

  @US-03
  Scenario: Rescue protocol query produces an accurate cited response
    Given the pre-loaded query "Protocolli di rescue per recidiva precoce dopo CHOP?" is submitted
    When the response is complete
    Then the synthesis mentions at least 2 rescue protocol options
    And each recommendation has at least 1 citation
    And no citation refers to a non-existent paper

  @US-03 @skip
  Scenario: Prognosis query produces an accurate cited response
    Given the pre-loaded query "Prognosi linfoma T-cell vs B-cell?" is submitted
    When the response is complete
    Then the synthesis discusses the prognostic difference between immunophenotypes
    And the synthesis mentions that B-cell has a better prognosis
    And each claim has at least 1 citation
    And no citation refers to a non-existent paper

  @US-03 @skip
  Scenario: Dose adjustment query produces an accurate cited response
    Given the pre-loaded query "Aggiustamento dose doxorubicina per neutropenia?" is submitted
    When the response is complete
    Then the synthesis provides grade-specific dose adjustment guidance
    And each recommendation has at least 1 citation
    And no citation refers to a non-existent paper

  # ===== US-04: Protocol Comparison Table =====

  @US-04
  Scenario: Comparison query generates a structured protocol table
    Given Dott.ssa Mancini submits "CHOP-19 vs CHOP-25: differenze negli outcome?"
    When the response is complete
    Then the response includes a comparison table
    And the table has columns for protocol name, remission rate, and median survival
    And each row in the table has a citation reference

  @US-04
  Scenario: Non-comparison query does not generate a table
    Given Dott.ssa Mancini submits "Prognosi linfoma T-cell vs B-cell?"
    When the response is complete
    Then the response is a synthesis with citations
    And no comparison table is displayed

  # ===== US-05: Graceful Error Handling =====

  @US-05
  Scenario: Out-of-scope query returns an honest no-evidence message
    Given Dott.ssa Mancini submits "Trattamento osteosarcoma felino"
    When the evidence search finds no relevant papers
    Then she sees a message indicating insufficient evidence in the corpus
    And the message explains the corpus covers canine multicentric lymphoma
    And suggestions are provided to rephrase or try pre-loaded queries

  @US-05
  Scenario: ASIA never fabricates an answer when evidence is missing
    Given the corpus has no papers relevant to "Chemioterapia per carcinoma polmonare nel gatto"
    When Dott.ssa Mancini submits this query
    Then the response contains no clinical synthesis
    And no citations are included
    And the response honestly states that insufficient evidence was found

  @US-05 @skip
  Scenario: Slow response shows progress feedback
    Given Dott.ssa Mancini submits a query that requires analyzing many papers
    When the response takes more than 10 seconds
    Then a progress indicator appears showing papers being analyzed
    And an estimated completion time is displayed

  @US-05
  Scenario: Self-reflective verification removes an unsupported citation
    Given the evidence pipeline generates a draft synthesis with 5 citations
    When the verification pass detects that one citation does not support its claim
    Then that citation is removed from the final response
    And a transparency note explains that a citation was removed for quality assurance
    And the final response contains only verified citations

  @US-05 @skip
  Scenario: Error messages are in Italian and suggest next steps
    Given Dott.ssa Mancini encounters an error during query processing
    When the error message is displayed
    Then the message is in Italian
    And the message suggests concrete next steps
    And no technical error codes or raw system messages are shown

  @US-05 @skip
  Scenario: Streaming connection lost preserves partial content
    Given Dott.ssa Mancini is reading a streaming response
    When the connection is interrupted mid-response
    Then the partial response already received is preserved on screen
    And a message explains the connection was interrupted
    And a retry option is available

  # ===== Property-Shaped Scenarios =====

  @property @US-02 @US-05 @skip
  Scenario: No response ever contains fabricated citations
    Given any clinical query submitted to ASIA
    When the response includes citations
    Then every cited paper exists in the corpus or in PubMed
    And every citation marker in the synthesis corresponds to a source panel entry

  @property @US-01 @skip
  Scenario: Medical disclaimer is visible on every page
    Given any page in the ASIA application
    Then the medical disclaimer is visible
    And the disclaimer cannot be hidden or dismissed
