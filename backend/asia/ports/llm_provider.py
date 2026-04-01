from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol


class LLMProvider(Protocol):
    async def generate(self, prompt: str, system_prompt: str | None = None) -> str: ...

    async def stream(
        self, prompt: str, system_prompt: str | None = None
    ) -> AsyncIterator[str]: ...
