# language: en
Feature: Milestone 2 -- Clinical Workflow
  As a veterinarian managing ongoing oncology cases
  I need persistent case context and the ability to understand individual papers
  So I can track patient-specific evidence and deepen my understanding of cited studies

  Stories: US-06, US-07

  Background:
    Given the ASIA application is running
    And the corpus contains papers about canine multicentric lymphoma

  # ===== US-06: Basic Case Mode =====

  @US-06
  Scenario: Veterinarian creates a new case with full patient information
    Given Dott.ssa Mancini navigates to case creation
    When she creates a case with name "Luna", breed "Golden Retriever", age "7 anni", diagnosis "Linfoma multicentrico", stage "III", immunophenotype "B-cell", and notes "Substadio a, buone condizioni generali"
    Then the case "Luna" is created successfully
    And the case page displays all the entered patient details

  @US-06
  Scenario: Veterinarian creates a case with only required fields
    Given Dott.ssa Mancini navigates to case creation
    When she creates a case with only name "Rex" and diagnosis "Linfoma multicentrico"
    Then the case "Rex" is created successfully
    And optional fields are stored as empty

  @US-06
  Scenario: Query within a case automatically includes patient context
    Given Dott.ssa Mancini has created the case "Luna" with breed "Golden Retriever", age "7 anni", diagnosis "Linfoma multicentrico B-cell", and stage "IIIa"
    When she submits the query "Qual e il protocollo migliore?" within Luna's case
    Then the response considers the patient context
    And the query and response are saved in Luna's case history

  @US-06
  Scenario: Case history shows all queries in chronological order
    Given Dott.ssa Mancini has made 3 queries within the case "Luna"
    When she views Luna's case page
    Then she sees all 3 queries listed with timestamps
    And the most recent query appears at the top
    And she can view the full response for any past query

  @US-06
  Scenario: Case data persists across sessions
    Given Dott.ssa Mancini created the case "Luna" in a previous session
    When she reopens ASIA and navigates to Luna's case
    Then all patient details are intact
    And all previous queries and responses are available

  @US-06 @skip
  Scenario: Case creation fails when required fields are missing
    Given Dott.ssa Mancini navigates to case creation
    When she attempts to create a case without providing a diagnosis
    Then case creation fails with a clear message about the missing required field
    And no incomplete case is stored

  # ===== US-07: Explain This Paper =====

  @US-07 @skip
  Scenario: Veterinarian gets a structured summary of a paper in the corpus
    Given Dott.ssa Mancini navigates to "Explain a Paper"
    When she submits the DOI "10.1111/vco.12345" for a paper in the corpus
    Then she receives a structured clinical summary in Italian
    And the summary includes sections for study objective, methodology, key results, practical implications, and corpus context

  @US-07 @skip
  Scenario: Paper not in the corpus produces an abstract-based summary
    Given Dott.ssa Mancini navigates to "Explain a Paper"
    When she submits a DOI for a paper not in the ASIA corpus
    Then she receives a summary based on the paper abstract
    And a note warns that the summary is based on the abstract only

  @US-07 @skip
  Scenario: Invalid DOI returns a helpful error message
    Given Dott.ssa Mancini navigates to "Explain a Paper"
    When she submits the DOI "10.9999/nonexistent"
    Then she sees a message that the paper could not be found
    And a suggestion to verify the DOI or try the paper title instead

  # ===== Error Paths =====

  @US-06 @skip
  Scenario: Query within a case with minimal context still produces a response
    Given Dott.ssa Mancini has created the case "Rex" with only name and diagnosis "Linfoma multicentrico"
    When she submits the query "Qual e il protocollo raccomandato?" within Rex's case
    Then she receives a synthesis in Italian
    And the response is not negatively affected by the missing optional fields

  @US-07 @skip
  Scenario: Empty DOI input shows a validation message
    Given Dott.ssa Mancini navigates to "Explain a Paper"
    When she submits an empty DOI field
    Then she sees a message asking her to enter a DOI or paper title
    And no request is sent to the backend
