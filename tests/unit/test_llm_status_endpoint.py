"""Unit tests for GET /api/llm-status endpoint.

Tests enter through the FastAPI HTTP driving port and assert observable
JSON response structure.

Test Budget: 1 behavior x 2 = 2 max
  1. /api/llm-status returns JSON with primary_available and model fields
Actual: 1 test
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


def test_llm_status_returns_availability_and_model():
    """GET /api/llm-status returns {primary_available: bool, model: str}."""
    from asia.main import app

    # We need to set up app.state with a rag_pipeline that has an _llm
    # with check_availability method
    mock_llm = AsyncMock()
    mock_llm.check_availability = AsyncMock(return_value=True)
    mock_llm._model = "llama-3.3-70b-versatile"

    mock_pipeline = MagicMock()
    mock_pipeline._llm = mock_llm

    app.state.rag_pipeline = mock_pipeline

    client = TestClient(app)
    response = client.get("/api/llm-status")

    assert response.status_code == 200
    data = response.json()
    assert "primary_available" in data
    assert data["primary_available"] is True
    assert "model" in data
    assert data["model"] == "llama-3.3-70b-versatile"
