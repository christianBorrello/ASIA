# ADR-001: LLM Adapter Pattern

## Status

Accepted

## Context

ASIA requires an LLM for two tasks: (1) generating Italian clinical synthesis from retrieved paper chunks, and (2) self-reflective citation verification. The MVP uses Groq's free tier hosting Llama 3.3 70B, but this dependency must be swappable because:

- Groq free tier may have rate limits, downtime, or policy changes
- Llama 3.3 70B may prove insufficient for Italian medical terminology
- Future needs may include local inference (Ollama), or higher-quality providers (Anthropic, OpenAI)
- The open-source nature of the project means contributors may use different LLM providers

The system needs a clean abstraction that isolates LLM provider details from the RAG pipeline logic.

## Decision

Implement an abstract `LLMProvider` port (Python Protocol or ABC) with two methods: `generate()` for synchronous completion and `stream()` for token-by-token async iteration. Each LLM provider is an adapter implementing this port. Provider selection is controlled by environment variable.

The port interface:

- `generate(prompt, max_tokens, temperature) -> str` -- for citation verification (needs full response)
- `stream(prompt, max_tokens, temperature) -> AsyncIterator[str]` -- for synthesis (streaming to SSE)

Provider-specific concerns (rate limiting, retry, authentication) are encapsulated within each adapter.

## Alternatives Considered

### 1. LangChain/LlamaIndex abstraction

LangChain and LlamaIndex provide built-in LLM abstractions. **Rejected** because: (a) adds a large dependency tree for a single abstraction, (b) abstractions are opinionated and leak framework concepts into the domain, (c) Christian is learning Python -- a simple custom port is easier to understand and debug than a framework abstraction, (d) framework lock-in is worse than provider lock-in.

### 2. Direct Groq SDK usage without abstraction

Call Groq SDK directly from the RAG pipeline. **Rejected** because: (a) makes provider swap a rewrite of business logic, (b) Groq-specific error handling leaks into domain code, (c) testing requires mocking Groq SDK internals rather than a clean interface.

### 3. OpenAI-compatible API as standard

Use OpenAI's API format as the standard interface (many providers are OpenAI-compatible). **Rejected** because: (a) not all providers are OpenAI-compatible (Anthropic has a different API), (b) still couples to a specific API contract rather than a domain-level abstraction, (c) conflates protocol compatibility with architectural isolation.

## Consequences

### Positive

- RAG pipeline is testable with a mock LLM provider (deterministic responses)
- Provider swap requires only a new adapter class + env var change
- Each adapter handles its own rate limiting, retry, and error mapping
- Contributors can add their preferred provider without modifying core logic

### Negative

- Small abstraction overhead (one extra layer of indirection)
- Each new provider requires implementing the adapter (though it is typically <100 lines)
- Prompt format differences between providers (some handle system prompts differently) may require adapter-level prompt wrapping
