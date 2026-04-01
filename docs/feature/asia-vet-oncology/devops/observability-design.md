# Observability Design -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## 1. MVP Observability Scope

**Decision**: Structured JSON logs to stdout only. No external monitoring stack (Prometheus, Grafana, Loki). This is proportional to a local demo with 1-3 users.

**Why no monitoring stack**:
- 0 concurrent users outside demo sessions
- No SLOs to enforce (demo, not production)
- 8GB RAM budget leaves no room for Prometheus + Grafana (~500MB additional)
- `docker compose logs -f api` provides real-time log viewing
- Post-MVP: add Prometheus + Grafana if ASIA moves to a hosted environment

---

## 2. Structured Logging Strategy

### Library

**Python backend**: `structlog` (MIT license). JSON output by default, human-readable console output for local development.

**Frontend**: Browser `console.log` with structured context (no logging library needed for MVP).

### Configuration

```python
# backend/asia/config/logging.py
import structlog
import logging
import sys

def configure_logging(log_level: str = "INFO", log_format: str = "json"):
    """Configure structured logging for the application."""

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )
```

### Log Format Toggle

| Environment | `LOG_FORMAT` | Output |
|-------------|-------------|--------|
| Docker Compose (default) | `json` | Structured JSON to stdout |
| Local development (no Docker) | `console` | Human-readable colored output |

Toggle via environment variable. JSON is default because `docker compose logs` captures stdout.

---

## 3. Log Event Taxonomy

Every log event has a consistent structure:

```json
{
  "event": "query.synthesis_completed",
  "level": "info",
  "timestamp": "2026-04-15T10:30:00.000Z",
  "request_id": "uuid",
  "duration_ms": 4200,
  ...event-specific fields
}
```

### RAG Pipeline Events

| Event | Level | Key Fields | Purpose |
|-------|-------|------------|---------|
| `query.received` | info | `query_text`, `case_id`, `has_context` | Query entered pipeline |
| `query.embedded` | debug | `embedding_ms`, `model` | Embedding timing |
| `retrieval.completed` | info | `top_k`, `max_similarity`, `avg_similarity`, `chunk_ids` | Retrieval quality signal |
| `retrieval.no_evidence` | warn | `max_similarity`, `threshold`, `query_text` | Below confidence threshold |
| `synthesis.started` | info | `chunk_count`, `has_case_context` | LLM synthesis beginning |
| `synthesis.token_streamed` | debug | `token_count` | Streaming progress (every 50 tokens) |
| `verification.started` | info | `citation_count` | Self-reflective pass beginning |
| `verification.result` | info | `citation_id`, `status` (SUPPORTA/PARZIALE/NON_SUPPORTA) | Per-citation verification |
| `verification.citation_removed` | warn | `citation_id`, `claim_text`, `reason` | Citation failed verification |
| `query.completed` | info | `total_ms`, `evidence_level`, `citation_count`, `verified_count` | Pipeline complete |
| `query.timeout` | warn | `total_ms`, `phase` (synthesis/verification) | Pipeline exceeded 25s |
| `query.error` | error | `error_type`, `error_message`, `phase` | Pipeline failure |

### Ingestion Events

| Event | Level | Key Fields | Purpose |
|-------|-------|------------|---------|
| `ingestion.started` | info | `source` | Run beginning |
| `ingestion.paper_fetched` | debug | `pmid`, `doi`, `title` | Individual paper |
| `ingestion.paper_duplicate` | debug | `pmid`, `doi` | Skipped duplicate |
| `ingestion.paper_embedded` | debug | `paper_id`, `chunk_count` | Embedding complete |
| `ingestion.completed` | info | `papers_new`, `papers_updated`, `errors`, `duration_ms` | Run complete |
| `ingestion.error` | error | `error_type`, `paper_id`, `source` | Individual paper error |

### API Events

| Event | Level | Key Fields | Purpose |
|-------|-------|------------|---------|
| `http.request` | info | `method`, `path`, `status_code`, `duration_ms` | Request log |
| `sse.connection_opened` | debug | `endpoint`, `client_ip` | SSE stream started |
| `sse.connection_closed` | debug | `endpoint`, `duration_ms` | SSE stream ended |
| `health.check` | debug | `status`, `db_ok` | Health endpoint hit |

### LLM Adapter Events

| Event | Level | Key Fields | Purpose |
|-------|-------|------------|---------|
| `llm.request` | info | `provider`, `model`, `prompt_tokens`, `max_tokens` | LLM call sent |
| `llm.response` | info | `provider`, `response_tokens`, `duration_ms` | LLM call returned |
| `llm.rate_limited` | warn | `provider`, `retry_after_s` | Rate limit hit |
| `llm.error` | error | `provider`, `error_type`, `retry_count` | LLM call failed |

---

## 4. Request Context Propagation

Every HTTP request gets a `request_id` (UUID) added to structlog context. All log events within that request include the ID for correlation.

```python
# Middleware pattern
@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    return response
```

This enables tracing a complete RAG pipeline execution through `docker compose logs -f api | grep <request_id>`.

---

## 5. Log Viewing for MVP

### Real-time

```bash
# All services
docker compose logs -f

# API only (most useful)
docker compose logs -f api

# Filter by event type (using jq)
docker compose logs -f api --no-log-prefix | jq 'select(.event == "query.completed")'

# Filter by request
docker compose logs -f api --no-log-prefix | jq 'select(.request_id == "uuid-here")'
```

### After the Fact

```bash
# Find slow queries (> 10 seconds)
docker compose logs api --no-log-prefix | jq 'select(.event == "query.completed" and .total_ms > 10000)'

# Find citation removals
docker compose logs api --no-log-prefix | jq 'select(.event == "verification.citation_removed")'

# Find no-evidence responses
docker compose logs api --no-log-prefix | jq 'select(.event == "retrieval.no_evidence")'
```

---

## 6. Log Retention

**MVP**: Docker Compose default log retention. Logs persist until `docker compose down`.

Configure Docker log rotation to prevent disk fill during extended sessions:

```yaml
# In docker-compose.yml, per service
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 7. Post-MVP Observability Path

When ASIA moves beyond local demo, add in this order:

| Priority | Addition | Trigger |
|----------|----------|---------|
| 1 | Prometheus metrics endpoint (`/metrics`) | When deployed to a server |
| 2 | Grafana dashboard (RED metrics for API) | When Prometheus is added |
| 3 | SLO monitoring (availability + latency) | When SLOs are defined |
| 4 | Alerting (PagerDuty/Slack) | When users depend on availability |
| 5 | Distributed tracing (OpenTelemetry) | When debugging cross-service issues |

For MVP, structured logs provide the debugging capability needed: request correlation, pipeline timing, citation verification results, and error context.
