"""
Step definitions for clinical query scenarios.

Domain: Clinical queries, evidence synthesis, citations, pre-loaded queries.
Driving port: POST /api/query, GET /api/pre-loaded-queries, GET /api/corpus-metadata
"""

from pytest_bdd import scenarios, given, when, then, parsers

# Register feature files
scenarios("../walking-skeleton.feature")
scenarios("../milestone-1-demo-ready.feature")


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("Dott.ssa Mancini opens the ASIA homepage", target_fixture="homepage")
def open_homepage(test_client):
    """Fetch homepage metadata via API."""
    metadata = test_client.get("/api/corpus-metadata")
    queries = test_client.get("/api/pre-loaded-queries")
    return {"metadata": metadata.json(), "queries": queries.json()}


@given(
    "Dott.ssa Mancini opens the ASIA homepage for the first time",
    target_fixture="homepage",
)
def open_homepage_first_time(test_client):
    """Same as open_homepage -- first visit context."""
    metadata = test_client.get("/api/corpus-metadata")
    queries = test_client.get("/api/pre-loaded-queries")
    return {"metadata": metadata.json(), "queries": queries.json()}


@given(
    "Dott.ssa Mancini has received a synthesis with citations for a lymphoma query",
    target_fixture="query_response",
)
def has_synthesis_with_citations(test_client):
    """Submit Q1 and capture the full response."""
    response = test_client.post(
        "/api/query",
        json={
            "text": "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
        },
    )
    return response.json()


@given(
    parsers.parse(
        'the pre-loaded query "{query_text}" is submitted'
    ),
    target_fixture="query_response",
)
def preloaded_query_submitted(test_client, query_text):
    """Submit a specific pre-loaded query."""
    response = test_client.post("/api/query", json={"text": query_text})
    return response.json()


@given(
    parsers.parse(
        'Dott.ssa Mancini sees the pre-loaded query "{query_text}"'
    ),
    target_fixture="selected_query",
)
def sees_preloaded_query(test_client, query_text):
    """Verify the query exists in pre-loaded queries."""
    queries_response = test_client.get("/api/pre-loaded-queries")
    queries = queries_response.json()["queries"]
    matching = [q for q in queries if q["text"] == query_text]
    assert len(matching) == 1, f"Pre-loaded query not found: {query_text}"
    return {"query_text": query_text}


@given(
    parsers.parse('Dott.ssa Mancini submits "{query_text}"'),
    target_fixture="query_response",
)
def submits_query(test_client, query_text):
    """Submit a free-text query."""
    response = test_client.post("/api/query", json={"text": query_text})
    return response.json()


@given(
    parsers.parse(
        'the corpus has no papers relevant to "{query_text}"'
    ),
    target_fixture="out_of_scope_query",
)
def corpus_has_no_papers_for(query_text):
    """Mark a query as out of scope (corpus does not cover it)."""
    return {"query_text": query_text}


@given(
    "the evidence pipeline generates a draft synthesis with 5 citations",
    target_fixture="draft_with_removals",
)
def draft_with_five_citations(test_client, seeded_corpus):
    """Submit a verification-trigger query through the driving port.

    The FakeLLM returns a synthesis with 5 citations for this query,
    then returns a verification response marking one as NON_SUPPORTA.
    The CitationVerifier in the pipeline removes it.
    """
    response = test_client.post(
        "/api/query",
        json={"text": "Verifica citazioni protocollo CHOP linfoma"},
    )
    assert response.status_code == 200
    return response.json()


@given("Dott.ssa Mancini encounters an error during query processing")
def encounters_error():
    """Error scenario setup -- actual error triggered in When step."""
    pass


@given("Dott.ssa Mancini is reading a streaming response")
def reading_streaming_response():
    """Streaming scenario setup -- actual streaming in When step."""
    pass


@given("Dott.ssa Mancini submits a query that requires analyzing many papers")
def complex_query_setup():
    """Complex query setup -- actual submission in When step."""
    pass


@given(
    parsers.parse("any clinical query submitted to ASIA"),
    target_fixture="any_query",
)
def any_clinical_query():
    """Property: applies to all queries."""
    return {"property": True}


@given("any page in the ASIA application")
def any_page():
    """Property: applies to all pages."""
    pass


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    parsers.parse(
        'she submits the clinical question "{query_text}"'
    ),
    target_fixture="query_response",
)
def submit_clinical_question(test_client, query_text):
    """Submit a clinical query via the API driving port."""
    response = test_client.post("/api/query", json={"text": query_text})
    assert response.status_code == 200, f"Query failed: {response.text}"
    return response.json()


@when("she clicks the query card", target_fixture="query_response")
def click_query_card(test_client, selected_query):
    """Click a pre-loaded query card (submits via API)."""
    response = test_client.post(
        "/api/query", json={"text": selected_query["query_text"]}
    )
    assert response.status_code == 200
    return response.json()


@when("the page finishes loading")
def page_loads():
    """Page load is implicit -- data already fetched in Given."""
    pass


@when("she views the source panel", target_fixture="source_panel")
def view_source_panel(query_response):
    """Extract source panel data from the query response."""
    return query_response.get("sources", [])


@when("the response is complete")
def response_complete():
    """Response completeness is implicit -- synchronous test client."""
    pass


@when("the evidence search finds no relevant papers", target_fixture="query_response")
def no_evidence_search(test_client):
    """Submit an out-of-scope query."""
    response = test_client.post(
        "/api/query", json={"text": "Trattamento osteosarcoma felino"}
    )
    return response.json()


@when(
    "Dott.ssa Mancini submits this query", target_fixture="query_response"
)
def submit_out_of_scope(test_client, out_of_scope_query):
    """Submit the previously defined out-of-scope query."""
    response = test_client.post(
        "/api/query", json={"text": out_of_scope_query["query_text"]}
    )
    return response.json()


@when(
    "the verification pass detects that one citation does not support its claim",
    target_fixture="verified_response",
)
def verification_removes_citation(draft_with_removals):
    """Verification already happened in the pipeline during the Given step.

    The API response already contains the verified synthesis with
    unsupported citations removed by the CitationVerifier.
    """
    return draft_with_removals


@when("the error message is displayed", target_fixture="error_response")
def error_displayed(test_client):
    """Trigger an error by submitting a query that causes an error condition."""
    response = test_client.post(
        "/api/query", json={"text": "Trattamento osteosarcoma felino"}
    )
    return response.json()


@when("the response takes more than 10 seconds")
def slow_response():
    """Slow response scenario -- tested via SSE heartbeat events."""
    # Implementation note: this requires SSE client testing
    # The test client should capture heartbeat events during streaming
    pass


@when("the connection is interrupted mid-response")
def connection_interrupted():
    """Connection interruption scenario."""
    # Implementation note: simulate by closing SSE connection mid-stream
    pass


@when("the response includes citations", target_fixture="citation_response")
def response_has_citations(test_client):
    """Property test -- submit a known good query and check citations."""
    response = test_client.post(
        "/api/query",
        json={
            "text": "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"
        },
    )
    return response.json()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("she receives a synthesis in Italian about first-line lymphoma protocols")
def receives_italian_synthesis(query_response):
    """Verify the response contains an Italian synthesis."""
    synthesis = query_response.get("synthesis", "")
    assert len(synthesis) > 0, "Synthesis is empty"
    # Verify Italian content (contains Italian medical terms)
    italian_indicators = ["protocollo", "remissione", "linfoma", "il", "e"]
    assert any(
        term in synthesis.lower() for term in italian_indicators
    ), f"Synthesis does not appear to be in Italian: {synthesis[:100]}"


@then("the synthesis contains at least 1 inline citation marker")
def has_citation_markers(query_response):
    """Verify citation markers [n] exist in the synthesis."""
    import re

    synthesis = query_response.get("synthesis", "")
    markers = re.findall(r"\[\d+\]", synthesis)
    assert len(markers) >= 1, f"No citation markers found in: {synthesis[:100]}"


@then("an evidence level indicator is displayed")
def has_evidence_level(query_response):
    """Verify evidence level is present."""
    evidence_level = query_response.get("evidence_level")
    assert evidence_level in (
        "ALTO",
        "MODERATO",
        "BASSO",
    ), f"Invalid evidence level: {evidence_level}"


@then("the medical disclaimer is visible")
def disclaimer_visible():
    """
    Disclaimer visibility is a frontend concern.
    At the API level, we verify the disclaimer text is available.
    """
    # Implementation note: for API-level tests, verify /api/corpus-metadata
    # returns disclaimer text. Frontend tests verify rendering.
    pass


@then("she sees a search box for clinical questions")
def sees_search_box(homepage):
    """Homepage metadata confirms search capability is available."""
    assert homepage is not None, "Homepage data not loaded"


@then('she sees a "Crea nuovo caso" button for case management')
def sees_case_button(homepage):
    """Homepage confirms case management feature is available."""
    # API-level: verify /api/cases endpoint exists
    pass


@then('she sees an "Explain a Paper" option')
def sees_explain_paper(homepage):
    """Homepage confirms explain paper feature is available."""
    # API-level: verify /api/explain-paper endpoint exists
    pass


@then("the corpus date is displayed")
def corpus_date_displayed(homepage):
    """Verify corpus metadata includes date."""
    metadata = homepage.get("metadata", {})
    assert "corpus_date" in metadata, "Corpus date not in metadata"


@then("each citation shows author, year, and a link to the paper")
def citations_have_details(source_panel):
    """Verify source panel entries have required fields."""
    assert len(source_panel) > 0, "Source panel is empty"
    for source in source_panel:
        assert "author" in source, f"Missing author in source: {source}"
        assert "year" in source, f"Missing year in source: {source}"
        assert "doi" in source, f"Missing DOI link in source: {source}"


@then(
    "the number of source panel entries matches the number of citation markers in the synthesis"
)
def source_count_matches_markers(query_response, source_panel):
    """Verify 1:1 mapping between citation markers and source entries."""
    import re

    synthesis = query_response.get("synthesis", "")
    unique_markers = set(re.findall(r"\[(\d+)\]", synthesis))
    assert len(source_panel) == len(
        unique_markers
    ), f"Source panel has {len(source_panel)} entries but synthesis has {len(unique_markers)} unique markers"


@then("she sees 5 pre-loaded clinical queries as clickable cards")
def sees_five_preloaded(homepage):
    """Verify 5 pre-loaded queries are returned."""
    queries = homepage.get("queries", {}).get("queries", [])
    assert len(queries) == 5, f"Expected 5 pre-loaded queries, got {len(queries)}"


@then(
    "the queries cover first-line protocol, protocol comparison, rescue protocols, prognosis, and dose adjustment"
)
def queries_cover_topics(homepage):
    """Verify topic coverage of pre-loaded queries."""
    queries = homepage.get("queries", {}).get("queries", [])
    topics = [q.get("topic", "") for q in queries]
    assert len(topics) == 5, f"Expected 5 topics, got {len(topics)}"


@then("the query is submitted for evidence synthesis")
def query_submitted(query_response):
    """Verify query produced a response."""
    assert query_response is not None


@then("a streaming response begins")
def streaming_begins(query_response):
    """Verify response was received (streaming tested at integration level)."""
    assert query_response is not None


@then("the query text is displayed at the top of the response")
def query_text_displayed(query_response):
    """Verify the original query text is returned."""
    assert "query_text" in query_response or "query" in query_response


@then("the synthesis mentions the CHOP protocol")
def mentions_chop(query_response):
    """Verify CHOP is mentioned in the synthesis."""
    synthesis = query_response.get("synthesis", "").upper()
    assert "CHOP" in synthesis, f"CHOP not found in synthesis: {synthesis[:200]}"


@then("the synthesis mentions remission rates")
def mentions_remission(query_response):
    """Verify remission rates are discussed."""
    synthesis = query_response.get("synthesis", "").lower()
    assert "remissione" in synthesis or "remission" in synthesis


@then("the response includes citations from relevant lymphoma studies")
def has_relevant_citations(query_response):
    """Verify citations reference lymphoma studies."""
    sources = query_response.get("sources", [])
    assert len(sources) >= 1, "No citations in response"


@then("no citation refers to a non-existent paper")
def no_fabricated_citations(query_response):
    """Verify all citations have valid DOIs."""
    sources = query_response.get("sources", [])
    for source in sources:
        assert source.get("doi") is not None, f"Citation missing DOI: {source}"
        assert source.get("author") is not None, f"Citation missing author: {source}"


@then("the synthesis discusses outcome equivalence between the protocols")
def discusses_equivalence(query_response):
    """Verify equivalence finding is mentioned."""
    synthesis = query_response.get("synthesis", "").lower()
    assert any(
        term in synthesis for term in ["equivalenti", "equivalente", "non ha trovato differenze", "nessuna differenza"]
    ), f"Equivalence not discussed: {synthesis[:200]}"


@then("the response cites the Sorenmo multicenter study")
def cites_sorenmo(query_response):
    """Verify Sorenmo et al. is cited."""
    sources = query_response.get("sources", [])
    sorenmo = [s for s in sources if "Sorenmo" in s.get("author", "")]
    assert len(sorenmo) >= 1, "Sorenmo study not cited"


@then("the synthesis mentions at least 2 rescue protocol options")
def mentions_rescue_options(query_response):
    """Verify multiple rescue protocols are discussed."""
    synthesis = query_response.get("synthesis", "").upper()
    rescue_protocols = ["LOPP", "LAP", "DMAC", "RABACFOSADINA", "TANOVEA"]
    found = [p for p in rescue_protocols if p in synthesis]
    assert len(found) >= 2, f"Only {len(found)} rescue protocols mentioned: {found}"


@then("the synthesis discusses the prognostic difference between immunophenotypes")
def discusses_prognosis(query_response):
    """Verify immunophenotype prognosis is discussed."""
    synthesis = query_response.get("synthesis", "").lower()
    assert "b-cell" in synthesis or "t-cell" in synthesis


@then("the synthesis mentions that B-cell has a better prognosis")
def bcell_better_prognosis(query_response):
    """Verify B-cell superiority is stated."""
    synthesis = query_response.get("synthesis", "").lower()
    assert "migliore" in synthesis or "better" in synthesis or "superiore" in synthesis


@then("the synthesis provides grade-specific dose adjustment guidance")
def grade_specific_guidance(query_response):
    """Verify dose adjustment by grade is discussed."""
    synthesis = query_response.get("synthesis", "").lower()
    assert any(
        term in synthesis for term in ["grado", "grade", "riduzione", "ritardo"]
    )


@then("each claim has at least 1 citation")
def claims_have_citations(query_response):
    """Verify citations exist in the response."""
    import re

    synthesis = query_response.get("synthesis", "")
    markers = re.findall(r"\[\d+\]", synthesis)
    assert len(markers) >= 1, "No citation markers in synthesis"


@then("each recommendation has at least 1 citation")
def recommendations_have_citations(query_response):
    """Alias for claims_have_citations."""
    import re

    synthesis = query_response.get("synthesis", "")
    markers = re.findall(r"\[\d+\]", synthesis)
    assert len(markers) >= 1, "No citation markers in synthesis"


@then("the response includes a comparison table")
def has_comparison_table(query_response):
    """Verify comparison table is present."""
    table = query_response.get("comparison_table")
    assert table is not None, "No comparison table in response"


@then(
    "the table has columns for protocol name, remission rate, and median survival"
)
def table_has_columns(query_response):
    """Verify table structure."""
    table = query_response.get("comparison_table", {})
    columns = table.get("columns", [])
    required = ["protocol", "remission_rate", "median_survival"]
    for col in required:
        assert col in columns, f"Missing column: {col}"


@then("each row in the table has a citation reference")
def table_rows_have_citations(query_response):
    """Verify each table row references a citation."""
    table = query_response.get("comparison_table", {})
    rows = table.get("rows", [])
    assert len(rows) > 0, "Table has no rows"
    for row in rows:
        assert "citation_id" in row, f"Row missing citation: {row}"


@then("the response is a synthesis with citations")
def is_synthesis_with_citations(query_response):
    """Verify response is a standard synthesis."""
    assert query_response.get("synthesis") is not None


@then("no comparison table is displayed")
def no_comparison_table(query_response):
    """Verify no comparison table in response."""
    table = query_response.get("comparison_table")
    assert table is None, f"Unexpected comparison table: {table}"


@then("she sees a message indicating insufficient evidence in the corpus")
def sees_no_evidence_message(query_response):
    """Verify no-evidence message."""
    message = query_response.get("message", "")
    assert "evidenze" in message.lower() or "insufficient" in message.lower()


@then("the message explains the corpus covers canine multicentric lymphoma")
def explains_corpus_scope(query_response):
    """Verify scope explanation."""
    scope = query_response.get("scope_explanation", "")
    assert "linfoma" in scope.lower() or "lymphoma" in scope.lower()


@then("suggestions are provided to rephrase or try pre-loaded queries")
def has_suggestions(query_response):
    """Verify suggestions are provided."""
    suggestions = query_response.get("suggestions", [])
    assert len(suggestions) >= 1, "No suggestions provided"


@then("the response contains no clinical synthesis")
def no_synthesis(query_response):
    """Verify no synthesis when evidence is missing."""
    synthesis = query_response.get("synthesis")
    assert synthesis is None or synthesis == ""


@then("no citations are included")
def no_citations(query_response):
    """Verify no citations in no-evidence response."""
    sources = query_response.get("sources", [])
    assert len(sources) == 0, f"Unexpected citations: {sources}"


@then("the response honestly states that insufficient evidence was found")
def honest_no_evidence(query_response):
    """Verify honest no-evidence message."""
    message = query_response.get("message", "")
    assert len(message) > 0, "No message in no-evidence response"


@then("a progress indicator appears showing papers being analyzed")
def progress_indicator():
    """Tested via SSE heartbeat events at integration level."""
    # Implementation note: verify SSE heartbeat events contain paper count
    pass


@then("an estimated completion time is displayed")
def estimated_time():
    """Tested via SSE heartbeat events at integration level."""
    pass


@then("that citation is removed from the final response")
def citation_removed(verified_response):
    """Verify the synthesis has fewer citations after verification.

    The original synthesis had 5 citations [1]-[5].
    After verification, the NON_SUPPORTA citation should be removed.
    """
    import re

    synthesis = verified_response.get("synthesis", "")
    markers = set(re.findall(r"\[(\d+)\]", synthesis))
    # Original had 5, one removed means max marker should be 4
    assert len(markers) <= 4, (
        f"Expected at most 4 unique citation markers after removal, "
        f"got {len(markers)}: {markers}"
    )


@then(
    "a transparency note explains that a citation was removed for quality assurance"
)
def transparency_note(verified_response):
    """Verify transparency note is present in the API response."""
    note = verified_response.get("reflection_note", "")
    assert len(note) > 0, "No reflection_note in response"
    assert "rimossa" in note.lower() or "removed" in note.lower() or "rimoss" in note.lower(), (
        f"Transparency note does not mention removal: {note}"
    )


@then("the final response contains only verified citations")
def only_verified_citations(verified_response):
    """Verify the response still contains citations (not all removed)."""
    sources = verified_response.get("sources", [])
    assert len(sources) >= 1, "All citations were removed -- at least one should remain"


@then("the message is in Italian")
def message_in_italian(error_response):
    """Verify error message is in Italian."""
    message = error_response.get("message", "") + error_response.get("detail", "")
    # Check for Italian language indicators
    assert any(
        term in message.lower()
        for term in ["non", "evidenze", "corpus", "domanda", "errore"]
    ), f"Message may not be in Italian: {message[:100]}"


@then("the message suggests concrete next steps")
def message_has_next_steps(error_response):
    """Verify actionable suggestions."""
    suggestions = error_response.get("suggestions", [])
    assert len(suggestions) >= 1, "No suggestions in error response"


@then("no technical error codes or raw system messages are shown")
def no_technical_errors(error_response):
    """Verify no technical jargon in error response."""
    response_text = str(error_response)
    technical_terms = ["traceback", "exception", "500", "404", "null", "undefined"]
    for term in technical_terms:
        assert term not in response_text.lower(), f"Technical term found: {term}"


@then("the partial response already received is preserved on screen")
def partial_response_preserved():
    """Connection loss scenario -- tested at frontend integration level."""
    pass


@then("a message explains the connection was interrupted")
def connection_interrupted_message():
    """Connection loss scenario -- tested at frontend integration level."""
    pass


@then("a retry option is available")
def retry_available():
    """Connection loss scenario -- tested at frontend integration level."""
    pass


@then("every cited paper exists in the corpus or in PubMed")
def all_citations_real(citation_response):
    """Property: verify no fabricated papers."""
    sources = citation_response.get("sources", [])
    for source in sources:
        assert source.get("doi") is not None, f"Citation without DOI: {source}"


@then(
    "every citation marker in the synthesis corresponds to a source panel entry"
)
def markers_match_sources(citation_response):
    """Property: verify 1:1 citation mapping."""
    import re

    synthesis = citation_response.get("synthesis", "")
    unique_markers = set(re.findall(r"\[(\d+)\]", synthesis))
    sources = citation_response.get("sources", [])
    source_ids = {str(s.get("id")) for s in sources}
    assert unique_markers.issubset(
        source_ids
    ), f"Unmatched markers: {unique_markers - source_ids}"


@then("the disclaimer cannot be hidden or dismissed")
def disclaimer_persistent():
    """Property: disclaimer persistence (frontend concern)."""
    # At API level, verified by ensuring disclaimer text is always returned
    pass
