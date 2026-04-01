"""Unit tests for GroqProvider retry, fallback, and availability.

Tests enter through the GroqProvider driving port (generate, check_availability)
and assert observable outcomes. The Groq SDK client is mocked at the external
boundary (infrastructure port).

Test Budget: 6 behaviors x 2 = 12 max
  1. generate() succeeds on first try -> last_used_fallback is False
  2. generate() retries on 503 then succeeds -> last_used_fallback is False
  3. generate() retries exhausted, falls back to smaller model -> last_used_fallback is True
  4. check_availability() returns True when primary model responds
  5. check_availability() returns False when primary model raises 503
  6. Settings includes GROQ_FALLBACK_MODEL_NAME and GROQ_MAX_RETRIES
Actual: 6 tests
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers to simulate Groq SDK responses and errors
# ---------------------------------------------------------------------------

def _make_completion_response(content: str) -> MagicMock:
    """Build a mock ChatCompletion response matching Groq SDK structure."""
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


def _make_internal_server_error():
    """Build an exception that mimics Groq 503 InternalServerError."""
    # We create a custom exception to avoid importing groq SDK in tests.
    # The production code catches groq.InternalServerError; we'll patch it.
    error = Exception("503 Service Unavailable")
    error.status_code = 503
    return error


# ---------------------------------------------------------------------------
# Test: generate() succeeds on first attempt
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_generate_succeeds_first_try_no_fallback():
    """generate() returns text and last_used_fallback is False when no error."""
    from asia.adapters.groq_provider import GroqProvider

    provider = GroqProvider(api_key="test-key", model_name="llama-3.3-70b-versatile")

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=_make_completion_response("synthesis result")
    )
    provider._client = mock_client

    result = await provider.generate("test prompt")

    assert result == "synthesis result"
    assert provider.last_used_fallback is False


# ---------------------------------------------------------------------------
# Test: generate() retries on 503, then succeeds on primary model
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_generate_retries_on_503_then_succeeds():
    """generate() retries on 503 and succeeds on retry; last_used_fallback is False."""
    from asia.adapters.groq_provider import GroqProvider
    from groq import InternalServerError

    provider = GroqProvider(
        api_key="test-key",
        model_name="llama-3.3-70b-versatile",
        max_retries=2,
    )

    # First call raises 503, second succeeds
    error_response = MagicMock()
    error_response.status_code = 503
    error_response.headers = {}

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[
            InternalServerError(
                message="Service Unavailable",
                response=error_response,
                body=None,
            ),
            _make_completion_response("retry success"),
        ]
    )
    provider._client = mock_client

    result = await provider.generate("test prompt")

    assert result == "retry success"
    assert provider.last_used_fallback is False


# ---------------------------------------------------------------------------
# Test: generate() retries exhausted -> fallback model used
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_generate_falls_back_after_retries_exhausted():
    """generate() falls back to smaller model after all retries fail; last_used_fallback is True."""
    from asia.adapters.groq_provider import GroqProvider
    from groq import InternalServerError

    provider = GroqProvider(
        api_key="test-key",
        model_name="llama-3.3-70b-versatile",
        fallback_model_name="llama-3.1-8b-instant",
        max_retries=2,
    )

    error_response = MagicMock()
    error_response.status_code = 503
    error_response.headers = {}

    internal_error = InternalServerError(
        message="Service Unavailable",
        response=error_response,
        body=None,
    )

    # All primary attempts fail (initial + 2 retries = 3 calls), then fallback succeeds
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[
            internal_error,
            internal_error,
            internal_error,
            _make_completion_response("fallback result"),
        ]
    )
    provider._client = mock_client

    result = await provider.generate("test prompt")

    assert result == "fallback result"
    assert provider.last_used_fallback is True
    # Verify the fallback call used the smaller model
    last_call = mock_client.chat.completions.create.call_args_list[-1]
    assert last_call.kwargs.get("model") == "llama-3.1-8b-instant" or \
        last_call[1].get("model") == "llama-3.1-8b-instant"


# ---------------------------------------------------------------------------
# Test: check_availability() returns True
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_check_availability_returns_true_when_model_responds():
    """check_availability() returns True when primary model can respond."""
    from asia.adapters.groq_provider import GroqProvider

    provider = GroqProvider(api_key="test-key", model_name="llama-3.3-70b-versatile")

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=_make_completion_response("ok")
    )
    provider._client = mock_client

    result = await provider.check_availability()

    assert result is True


# ---------------------------------------------------------------------------
# Test: check_availability() returns False on 503
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_check_availability_returns_false_on_503():
    """check_availability() returns False when primary model raises 503."""
    from asia.adapters.groq_provider import GroqProvider
    from groq import InternalServerError

    provider = GroqProvider(api_key="test-key", model_name="llama-3.3-70b-versatile")

    error_response = MagicMock()
    error_response.status_code = 503
    error_response.headers = {}

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=InternalServerError(
            message="Service Unavailable",
            response=error_response,
            body=None,
        )
    )
    provider._client = mock_client

    result = await provider.check_availability()

    assert result is False


# ---------------------------------------------------------------------------
# Test: Settings includes fallback configuration
# ---------------------------------------------------------------------------

def test_settings_includes_fallback_configuration():
    """Settings has GROQ_FALLBACK_MODEL_NAME and GROQ_MAX_RETRIES with defaults."""
    from asia.config.settings import Settings

    settings = Settings(GROQ_API_KEY="test")

    assert hasattr(settings, "GROQ_FALLBACK_MODEL_NAME")
    assert settings.GROQ_FALLBACK_MODEL_NAME == "llama-3.1-8b-instant"
    assert hasattr(settings, "GROQ_MAX_RETRIES")
    assert settings.GROQ_MAX_RETRIES == 2
