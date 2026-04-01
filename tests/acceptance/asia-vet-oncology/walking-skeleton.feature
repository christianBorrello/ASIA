# language: en
Feature: Walking Skeleton -- One Question, One Answer
  As a veterinarian managing a canine lymphoma case
  I need to ask a clinical question and receive a cited synthesis in Italian
  So I can make an informed treatment decision quickly

  The walking skeleton proves the core value proposition:
  a vet types a question, gets an Italian synthesis with verifiable citations.
  This is the thinnest slice that delivers observable user value end-to-end.

  Stories: US-01, US-02

  Background:
    Given the ASIA application is running
    And the corpus contains papers about canine multicentric lymphoma

  # --- Walking Skeleton 1: Core Query Flow ---

  @walking_skeleton @US-01 @US-02
  Scenario: Veterinarian asks a clinical question and receives a cited synthesis in Italian
    Given Dott.ssa Mancini opens the ASIA homepage
    When she submits the clinical question "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
    Then she receives a synthesis in Italian about first-line lymphoma protocols
    And the synthesis contains at least 1 inline citation marker
    And an evidence level indicator is displayed
    And the medical disclaimer is visible

  # --- Walking Skeleton 2: Citation Verification ---

  @walking_skeleton @US-02
  Scenario: Veterinarian verifies a citation from the synthesis
    Given Dott.ssa Mancini has received a synthesis with citations for a lymphoma query
    When she views the source panel
    Then each citation shows author, year, and a link to the paper
    And the number of source panel entries matches the number of citation markers in the synthesis

  # --- Walking Skeleton 3: Homepage Discovery ---

  @walking_skeleton @US-01
  Scenario: Veterinarian discovers ASIA and understands its purpose
    Given Dott.ssa Mancini opens the ASIA homepage for the first time
    When the page finishes loading
    Then she sees a search box for clinical questions
    And she sees a "Crea nuovo caso" button for case management
    And she sees an "Explain a Paper" option
    And the medical disclaimer is visible
    And the corpus date is displayed
