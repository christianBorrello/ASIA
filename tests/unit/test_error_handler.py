"""Unit tests for error handler -- Italian messages, suggestions, no technical codes."""
from __future__ import annotations

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from asia.api.middleware.error_handler import register_error_handlers


def _make_app_with_failing_endpoint() -> FastAPI:
    """Create a minimal app with a route that raises an unhandled exception."""
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/api/fail")
    async def fail_endpoint():
        raise RuntimeError("database connection refused on port 5432")

    return app


class TestErrorHandlerReturnsItalianMessages:

    def test_unhandled_exception_returns_italian_message_with_suggestions(self):
        app = _make_app_with_failing_endpoint()
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/fail")

        body = response.json()
        # Must be Italian -- check for Italian indicators
        message = body.get("message", "") + body.get("detail", "")
        assert any(
            term in message.lower()
            for term in ["errore", "problema", "riprovare", "contattare"]
        ), f"Message not in Italian: {message}"
        # Must have suggestions
        suggestions = body.get("suggestions", [])
        assert len(suggestions) >= 1, "No suggestions provided"
        # Must not expose technical details
        response_text = str(body)
        for term in ["traceback", "exception", "null", "undefined", "database connection refused"]:
            assert term not in response_text.lower(), f"Technical term leaked: {term}"
