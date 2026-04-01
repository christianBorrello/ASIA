"""GroqProvider adapter -- implements LLMProvider using Groq SDK."""
from __future__ import annotations

from collections.abc import AsyncIterator

from groq import AsyncGroq


class GroqProvider:
    """LLMProvider adapter using Groq cloud API with Llama models."""

    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile") -> None:
        self._client = AsyncGroq(api_key=api_key)
        self._model = model_name

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a single completion."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        """Stream completion tokens."""
        messages = []
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
