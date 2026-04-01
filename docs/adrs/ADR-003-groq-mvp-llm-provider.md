# ADR-003: Groq as MVP LLM Provider

## Status

Accepted

## Context

ASIA requires an LLM capable of: (1) generating coherent Italian medical synthesis from English paper chunks, (2) sentence-level citation attribution, (3) self-reflective verification, (4) streaming responses. The constraint is zero operating cost for MVP.

Available options are constrained by the EUR 0 budget and the MacBook Air M1 8GB RAM development hardware.

## Decision

Use Groq's free tier hosting Llama 3.3 70B as the MVP LLM provider, accessed via the LLM Adapter pattern (ADR-001).

Groq free tier provides:
- Llama 3.3 70B: sufficient quality for Italian medical text
- 30 requests/minute, 6000 tokens/minute on free tier
- Fast inference (~500 tokens/second) via custom LPU hardware
- Streaming support (SSE-compatible)

## Alternatives Considered

### 1. Ollama with Llama 3.3 8B (local)

Run a small model locally. **Rejected** because: (a) 8B parameter models produce significantly lower quality Italian medical text compared to 70B, (b) even quantized 8B models consume ~4-5GB RAM, leaving insufficient memory for PostgreSQL + sentence-transformers + Docker, (c) inference speed on M1 8GB is slow (~10-20 tokens/second) making the 30-second response target difficult.

### 2. Ollama with Llama 3.3 70B (local)

Run the full 70B model locally. **Rejected** because: the quantized 70B model requires ~35-40GB RAM. MacBook Air M1 has 8GB. Physically impossible.

### 3. Together AI free tier

Together AI offers free tier with open-source models. **Rejected** because: (a) free tier limits are more restrictive than Groq, (b) inference speed is slower, (c) less established free tier SLA.

### 4. Anthropic Claude (paid)

Claude excels at Italian text and structured output. **Rejected** because: EUR 0 budget constraint. However, the LLM Adapter pattern (ADR-001) makes this a viable future option if budget becomes available.

### 5. Google Gemini free tier

Gemini offers a free tier. **Rejected** because: (a) free tier has significant rate limits, (b) streaming support is less mature, (c) Italian medical text quality with Gemini 1.5 Flash is untested for this domain.

## Consequences

### Positive

- Zero operating cost for MVP
- 70B model provides good Italian language quality
- Fast inference reduces time-to-first-token
- LLM Adapter pattern means this decision is fully reversible

### Negative

- Network dependency: demo requires internet access
- Free tier may change or be discontinued (mitigated by adapter pattern)
- Rate limits (30 req/min) could be hit with aggressive testing but are sufficient for 1-3 concurrent demo users
- Llama 3.3 70B Italian medical quality is untested -- must benchmark against 5 critical queries early in development. Fallback: try Mixtral 8x7B on Groq, or consider paid provider.
