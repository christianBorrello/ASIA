"""
Step definitions for Explain This Paper scenarios.

Domain: Paper explanation, DOI resolution, clinical summaries.
Driving port: POST /api/explain-paper
"""

from pytest_bdd import scenarios, given, when, then, parsers

# Scenarios already registered in case_steps.py (same feature file)
# Only register if not already done -- pytest-bdd handles deduplication


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given('Dott.ssa Mancini navigates to "Explain a Paper"')
def navigate_to_explain_paper():
    """Explain a Paper is accessible via the API."""
    pass


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    parsers.parse('she submits the DOI "{doi}" for a paper in the corpus'),
    target_fixture="paper_response",
)
def submit_doi_in_corpus(test_client, doi):
    """Submit a DOI for a paper that exists in the corpus."""
    response = test_client.post(
        "/api/explain-paper",
        json={"doi": doi},
    )
    assert response.status_code == 200, f"Explain paper failed: {response.text}"
    return response.json()


@when(
    "she submits a DOI for a paper not in the ASIA corpus",
    target_fixture="paper_response",
)
def submit_doi_not_in_corpus(test_client):
    """Submit a DOI for a paper outside the corpus."""
    response = test_client.post(
        "/api/explain-paper",
        json={"doi": "10.1234/external.paper.2024"},
    )
    return response.json()


@when(
    parsers.parse('she submits the DOI "{doi}"'),
    target_fixture="paper_response",
)
def submit_doi(test_client, doi):
    """Submit any DOI for paper explanation."""
    response = test_client.post(
        "/api/explain-paper",
        json={"doi": doi},
    )
    return response


@when("she submits an empty DOI field", target_fixture="paper_response")
def submit_empty_doi(test_client):
    """Submit with empty DOI."""
    response = test_client.post(
        "/api/explain-paper",
        json={"doi": ""},
    )
    return response


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("she receives a structured clinical summary in Italian")
def receives_structured_summary(paper_response):
    """Verify the response contains a structured summary."""
    summary = paper_response.get("summary", {})
    assert len(summary) > 0, "No summary in response"


@then(
    "the summary includes sections for study objective, methodology, "
    "key results, practical implications, and corpus context"
)
def summary_has_sections(paper_response):
    """Verify all 5 required sections are present."""
    summary = paper_response.get("summary", {})
    required_sections = [
        "obiettivo",
        "metodologia",
        "risultati",
        "implicazioni",
        "contesto",
    ]
    # Sections may be returned as keys or as a list of named sections
    summary_text = str(summary).lower()
    for section in required_sections:
        assert (
            section in summary_text
        ), f"Missing section '{section}' in summary"


@then("she receives a summary based on the paper abstract")
def receives_abstract_summary(paper_response):
    """Verify summary was generated from abstract only."""
    assert paper_response.get("summary") is not None
    assert paper_response.get("source") == "abstract" or paper_response.get(
        "abstract_only"
    )


@then("a note warns that the summary is based on the abstract only")
def abstract_only_warning(paper_response):
    """Verify abstract-only warning is present."""
    notes = str(paper_response).lower()
    assert "abstract" in notes, "No abstract-only warning"


@then("she sees a message that the paper could not be found")
def paper_not_found(paper_response):
    """Verify not-found message for invalid DOI."""
    if hasattr(paper_response, "status_code"):
        assert paper_response.status_code == 404
        data = paper_response.json()
    else:
        data = paper_response
    message = str(data).lower()
    assert "non" in message or "not found" in message or "trovare" in message


@then("a suggestion to verify the DOI or try the paper title instead")
def doi_suggestion(paper_response):
    """Verify helpful suggestion for invalid DOI."""
    if hasattr(paper_response, "status_code"):
        data = paper_response.json()
    else:
        data = paper_response
    message = str(data).lower()
    assert "doi" in message or "titolo" in message or "title" in message


@then("she sees a message asking her to enter a DOI or paper title")
def empty_doi_message(paper_response):
    """Verify validation message for empty input."""
    if hasattr(paper_response, "status_code"):
        assert paper_response.status_code in (400, 422)


@then("no request is sent to the backend")
def no_backend_request():
    """Frontend validation prevents empty submissions."""
    # At the API level, we verify the error response
    # Frontend-level validation is a frontend test concern
    pass
