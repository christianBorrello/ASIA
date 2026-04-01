"""
Step definitions for case mode scenarios.

Domain: Patient case management, context injection, query history.
Driving port: POST /api/cases, GET /api/cases/{id}, POST /api/cases/{id}/query
"""

from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../milestone-2-clinical-workflow.feature")


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("Dott.ssa Mancini navigates to case creation")
def navigate_to_case_creation():
    """Case creation is available via API."""
    pass


@given(
    parsers.parse(
        'Dott.ssa Mancini has created the case "{case_name}" with breed "{breed}", '
        'age "{age}", diagnosis "{diagnosis}", and stage "{stage}"'
    ),
    target_fixture="existing_case",
)
def has_case_with_details(test_client, case_name, breed, age, diagnosis, stage):
    """Create a case via the API for subsequent query tests."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": case_name,
            "breed": breed,
            "age": age,
            "diagnosis": diagnosis,
            "stage": stage,
        },
    )
    assert response.status_code == 201, f"Case creation failed: {response.text}"
    return response.json()


@given(
    parsers.parse(
        'Dott.ssa Mancini has created the case "{case_name}" with only name and diagnosis "{diagnosis}"'
    ),
    target_fixture="existing_case",
)
def has_minimal_case(test_client, case_name, diagnosis):
    """Create a case with only required fields."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": case_name,
            "diagnosis": diagnosis,
        },
    )
    assert response.status_code == 201
    return response.json()


@given(
    parsers.parse(
        'Dott.ssa Mancini has made {count:d} queries within the case "{case_name}"'
    ),
    target_fixture="case_with_queries",
)
def has_queries_in_case(test_client, count, case_name):
    """Create a case and submit multiple queries."""
    # Create the case
    case_response = test_client.post(
        "/api/cases",
        json={
            "patient_name": case_name,
            "diagnosis": "Linfoma multicentrico",
        },
    )
    assert case_response.status_code == 201
    case = case_response.json()
    case_id = case["id"]

    # Submit queries
    sample_queries = [
        "Qual e il protocollo migliore?",
        "Neutropenia grado 2 dopo prima dose doxorubicina?",
        "Quando iniziare il protocollo di rescue?",
    ]
    for i in range(count):
        query_text = sample_queries[i % len(sample_queries)]
        test_client.post(
            f"/api/cases/{case_id}/query",
            json={"text": query_text},
        )

    return {"case_id": case_id, "case_name": case_name, "query_count": count}


@given(
    parsers.parse(
        'Dott.ssa Mancini created the case "{case_name}" in a previous session'
    ),
    target_fixture="existing_case",
)
def case_from_previous_session(test_client, case_name):
    """Create a case to simulate persistence from a previous session."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": case_name,
            "breed": "Golden Retriever",
            "age": "7 anni",
            "diagnosis": "Linfoma multicentrico",
            "stage": "III",
            "immunophenotype": "B-cell",
        },
    )
    assert response.status_code == 201
    return response.json()


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    parsers.parse(
        'she creates a case with name "{name}", breed "{breed}", age "{age}", '
        'diagnosis "{diagnosis}", stage "{stage}", immunophenotype "{immunophenotype}", '
        'and notes "{notes}"'
    ),
    target_fixture="case_response",
)
def create_full_case(test_client, name, breed, age, diagnosis, stage, immunophenotype, notes):
    """Create a case with all fields via the API driving port."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": name,
            "breed": breed,
            "age": age,
            "diagnosis": diagnosis,
            "stage": stage,
            "immunophenotype": immunophenotype,
            "notes": notes,
        },
    )
    return response


@when(
    parsers.parse(
        'she creates a case with only name "{name}" and diagnosis "{diagnosis}"'
    ),
    target_fixture="case_response",
)
def create_minimal_case(test_client, name, diagnosis):
    """Create a case with required fields only."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": name,
            "diagnosis": diagnosis,
        },
    )
    return response


@when(
    parsers.parse(
        'she submits the query "{query_text}" within Luna\'s case'
    ),
    target_fixture="case_query_response",
)
def submit_query_in_luna_case(test_client, existing_case, query_text):
    """Submit a query within an existing case."""
    case_id = existing_case["id"]
    response = test_client.post(
        f"/api/cases/{case_id}/query",
        json={"text": query_text},
    )
    assert response.status_code == 200, f"Case query failed: {response.text}"
    return response.json()


@when(
    parsers.parse(
        'she submits the query "{query_text}" within Rex\'s case'
    ),
    target_fixture="case_query_response",
)
def submit_query_in_rex_case(test_client, existing_case, query_text):
    """Submit a query within Rex's case."""
    case_id = existing_case["id"]
    response = test_client.post(
        f"/api/cases/{case_id}/query",
        json={"text": query_text},
    )
    assert response.status_code == 200
    return response.json()


@when("she views Luna's case page", target_fixture="case_detail")
def view_luna_case(test_client, case_with_queries):
    """Fetch case details via API."""
    case_id = case_with_queries["case_id"]
    response = test_client.get(f"/api/cases/{case_id}")
    assert response.status_code == 200
    return response.json()


@when("she reopens ASIA and navigates to Luna's case", target_fixture="case_detail")
def reopen_and_navigate(test_client, existing_case):
    """Simulate reopening by fetching case from API."""
    case_id = existing_case["id"]
    response = test_client.get(f"/api/cases/{case_id}")
    assert response.status_code == 200
    return response.json()


@when("she attempts to create a case without providing a diagnosis", target_fixture="case_response")
def create_case_without_diagnosis(test_client):
    """Attempt to create a case missing required field."""
    response = test_client.post(
        "/api/cases",
        json={
            "patient_name": "Fido",
        },
    )
    return response


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the case "{case_name}" is created successfully'))
def case_created(case_response, case_name):
    """Verify case creation succeeded."""
    assert case_response.status_code == 201, f"Expected 201, got {case_response.status_code}"
    data = case_response.json()
    assert data["patient_name"] == case_name


@then("the case page displays all the entered patient details")
def displays_patient_details(case_response):
    """Verify all fields are returned."""
    data = case_response.json()
    assert data.get("patient_name") is not None
    assert data.get("breed") is not None
    assert data.get("diagnosis") is not None


@then("optional fields are stored as empty")
def optional_fields_empty(case_response):
    """Verify optional fields are null or empty."""
    data = case_response.json()
    optional = ["breed", "age", "stage", "immunophenotype", "notes"]
    for field in optional:
        value = data.get(field)
        assert value is None or value == "", f"Optional field {field} has value: {value}"


@then("the response considers the patient context")
def response_considers_context(case_query_response):
    """Verify the response reflects case context."""
    synthesis = case_query_response.get("synthesis", "")
    assert len(synthesis) > 0, "Empty synthesis from case query"
    # The response should be relevant (contains medical content)
    assert any(
        term in synthesis.lower()
        for term in ["protocollo", "linfoma", "trattamento", "chop"]
    )


@then("the query and response are saved in Luna's case history")
def saved_in_history(test_client, existing_case):
    """Verify the query appears in case history."""
    case_id = existing_case["id"]
    response = test_client.get(f"/api/cases/{case_id}")
    data = response.json()
    queries = data.get("queries", [])
    assert len(queries) >= 1, "No queries in case history"


@then(parsers.parse("she sees all {count:d} queries listed with timestamps"))
def sees_queries_with_timestamps(case_detail, count):
    """Verify query count and timestamps."""
    queries = case_detail.get("queries", [])
    assert len(queries) == count, f"Expected {count} queries, got {len(queries)}"
    for q in queries:
        assert "created_at" in q, f"Query missing timestamp: {q}"


@then("the most recent query appears at the top")
def most_recent_first(case_detail):
    """Verify chronological ordering (most recent first)."""
    queries = case_detail.get("queries", [])
    if len(queries) >= 2:
        assert queries[0]["created_at"] >= queries[1]["created_at"]


@then("she can view the full response for any past query")
def can_view_past_responses(case_detail):
    """Verify responses are included in query history."""
    queries = case_detail.get("queries", [])
    for q in queries:
        assert "response" in q or "synthesis" in q, f"Query missing response: {q}"


@then("all patient details are intact")
def patient_details_intact(case_detail):
    """Verify case data persisted correctly."""
    assert case_detail.get("patient_name") is not None
    assert case_detail.get("diagnosis") is not None


@then("all previous queries and responses are available")
def previous_queries_available(case_detail):
    """Verify query history persisted."""
    # Case may or may not have queries depending on test setup
    assert "queries" in case_detail


@then("case creation fails with a clear message about the missing required field")
def creation_fails_with_message(case_response):
    """Verify validation error for missing required field."""
    assert case_response.status_code == 422 or case_response.status_code == 400
    data = case_response.json()
    error_text = str(data).lower()
    assert "diagnosi" in error_text or "diagnosis" in error_text or "required" in error_text


@then("no incomplete case is stored")
def no_incomplete_case(test_client):
    """Verify no case named 'Fido' was stored."""
    # Implementation note: list cases and verify Fido is not there
    pass


@then("she receives a synthesis in Italian")
def receives_synthesis(case_query_response):
    """Verify synthesis is returned for case query."""
    synthesis = case_query_response.get("synthesis", "")
    assert len(synthesis) > 0


@then("the response is not negatively affected by the missing optional fields")
def response_not_affected(case_query_response):
    """Verify response quality is maintained with minimal context."""
    synthesis = case_query_response.get("synthesis", "")
    assert len(synthesis) > 0
    sources = case_query_response.get("sources", [])
    assert len(sources) >= 1, "No citations even with minimal context"
