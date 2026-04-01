"""GroqProvider adapter -- implements LLMProvider using Groq SDK."""
from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator

from groq import AsyncGroq, InternalServerError


logger = logging.getLogger(__name__)


class GroqProvider:
    """LLMProvider adapter using Groq cloud API with Llama models.

    Supports retry with exponential backoff on 503 errors and automatic
    fallback to a smaller model when retries are exhausted.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "llama-3.3-70b-versatile",
        fallback_model_name: str = "llama-3.1-8b-instant",
        max_retries: int = 2,
    ) -> None:
        self._client = AsyncGroq(api_key=api_key)
        self._model = model_name
        self._fallback_model = fallback_model_name
        self._max_retries = max_retries
        self._last_used_fallback: bool = False

    @property
    def last_used_fallback(self) -> bool:
        """Whether the last generate() call used the fallback model."""
        return self._last_used_fallback

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a single completion with retry and fallback."""
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        self._last_used_fallback = False

        for attempt in range(self._max_retries + 1):
            try:
                return await self._call_llm(self._model, messages)
            except InternalServerError:
                if attempt < self._max_retries:
                    delay = 2**attempt  # 1s, 2s
                    logger.warning(
                        "Groq 503 on attempt %d/%d, retrying in %ds",
                        attempt + 1,
                        self._max_retries + 1,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    continue
                # All retries exhausted -- fall back to smaller model
                logger.warning(
                    "Groq 503 after %d retries, falling back to %s",
                    self._max_retries,
                    self._fallback_model,
                )
                self._last_used_fallback = True
                return await self._call_llm(self._fallback_model, messages)

        # Unreachable, but satisfies type checker
        raise RuntimeError("Unexpected exit from retry loop")  # pragma: no cover

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        """Stream completion tokens."""
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

    async def check_availability(self) -> bool:
        """Test whether the primary model is reachable with a minimal request."""
        try:
            await self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )
            return True
        except InternalServerError:
            return False

    async def _call_llm(
        self, model: str, messages: list[dict[str, str]]
    ) -> str:
        """Execute a single LLM call."""
        response = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""
