"""Unit tests for metadata API endpoints.

Tests enter through the FastAPI driving port (HTTP endpoints) and assert
observable response structure and content.

Test Budget: 2 behaviors (corpus-metadata response, pre-loaded-queries response) x 2 = 4 max
Actual: 2 tests
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from asia.main import app


client = TestClient(app)


def test_corpus_metadata_returns_date_count_and_disclaimer():
    """GET /api/corpus-metadata returns corpus_date, paper_count, and disclaimer_text."""
    response = client.get("/api/corpus-metadata")

    assert response.status_code == 200
    data = response.json()
    assert "corpus_date" in data
    assert "paper_count" in data
    assert isinstance(data["paper_count"], int)
    assert data["paper_count"] > 0
    assert "disclaimer_text" in data
    assert len(data["disclaimer_text"]) > 0


def test_pre_loaded_queries_returns_queries_with_required_fields():
    """GET /api/pre-loaded-queries returns queries with id, text, topic (lymphoma + carcinoma)."""
    response = client.get("/api/pre-loaded-queries")

    assert response.status_code == 200
    data = response.json()
    queries = data["queries"]
    assert len(queries) >= 7, f"Expected >= 7 queries (5 lymphoma + 2+ carcinoma), got {len(queries)}"
    for query in queries:
        assert "id" in query
        assert "text" in query
        assert "topic" in query
        assert len(query["text"]) > 0
