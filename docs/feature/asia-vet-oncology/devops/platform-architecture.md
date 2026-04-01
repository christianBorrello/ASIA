# Platform Architecture -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## 1. Deployment Topology

**Target**: Local MacBook Air M1, 8GB RAM, Docker Compose.
**Strategy**: Recreate (stop-and-replace). No zero-downtime requirement for a local demo.

```
+--------------------------------------------------+
|  MacBook Air M1 (8GB RAM)                        |
|                                                  |
|  +--------------------------------------------+  |
|  | Docker Compose                              |  |
|  |                                             |  |
|  |  +----------+  +----------+  +----------+  |  |
|  |  | frontend |  |   api    |  |    db    |  |  |
|  |  | Next.js  |  | FastAPI  |  | PG 16 + |  |  |
|  |  | :3000    |  | :8000    |  | pgvector |  |  |
|  |  |  300MB   |  |  1.5GB   |  | :5432    |  |  |
|  |  +----------+  +----------+  |  500MB   |  |  |
|  |                              +----------+  |  |
|  |  Docker Desktop overhead: ~500MB           |  |
|  +--------------------------------------------+  |
|                                                  |
|  OS + browser: ~3.0GB                            |
|  Total: ~5.8GB | Headroom: ~2.2GB                |
+--------------------------------------------------+
```

---

## 2. Docker Compose Design

### Service Definitions

```yaml
# docker-compose.yml
services:
  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: asia
      POSTGRES_USER: asia
      POSTGRES_PASSWORD: asia_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql
    deploy:
      resources:
        limits:
          memory: 512M
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U asia"]
      interval: 5s
      timeout: 3s
      retries: 5

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://asia:asia_dev@db:5432/asia
      GROQ_API_KEY: ${GROQ_API_KEY}
      EMBEDDING_MODEL: all-MiniLM-L6-v2
      LOG_LEVEL: INFO
      LOG_FORMAT: json
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 1536M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - api
    deploy:
      resources:
        limits:
          memory: 384M

volumes:
  pgdata:
```

### Rejected Simple Alternatives

**Alternative 1: Run everything natively (no Docker)**
- What: Python venv + local PostgreSQL + npm dev server
- Expected Impact: 100% of requirements met
- Why Insufficient: Not rejected outright -- this is a viable fallback. Docker Compose chosen for reproducibility across machines and one-command startup (`docker compose up`). If M1 memory is tight, native mode is the escape hatch.

**Alternative 2: Single container with all services**
- What: One Docker image with PostgreSQL + FastAPI + Next.js
- Expected Impact: 90% of requirements
- Why Insufficient: Violates separation of concerns, complicates development iteration (rebuild everything on any change), and makes it harder to resource-limit individual services.

---

## 3. Container Images

### Backend (api)

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

# Install system deps for psycopg and sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding model at build time (avoids runtime download)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY asia/ asia/

CMD ["uvicorn", "asia.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS base

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Dev mode for MVP (hot reload)
CMD ["npm", "run", "dev"]
```

### Database

Uses `pgvector/pgvector:pg16` directly. Init script creates the `vector` extension and schema:

```sql
-- backend/db/init.sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Schema from data-models.md applied here
-- (tables: papers, chunks, cases, case_queries, ingestion_runs)
```

---

## 4. Resource Limits

| Service | Memory Limit | CPU Limit | Rationale |
|---------|-------------|-----------|-----------|
| db | 512MB | -- (no limit) | ~2000 papers + IVFFlat index. Generous for corpus size. |
| api | 1536MB | -- (no limit) | sentence-transformers model (~80MB) + FastAPI + Python runtime |
| frontend | 384MB | -- (no limit) | Next.js dev server. Production build would be ~150MB. |

CPU limits omitted: M1 has 8 cores, no contention with 3 services. Adding CPU limits would only slow startup.

Total container memory: 2432MB (~2.4GB). With Docker Desktop overhead (~500MB): ~2.9GB for Docker. Remaining ~5.1GB for macOS + browser.

---

## 5. Networking

All services on a single Docker Compose default bridge network. No external exposure beyond localhost.

| Service | Internal Port | External Port | Access |
|---------|--------------|--------------|--------|
| db | 5432 | 5432 | localhost only (for dev tools like pgAdmin/DBeaver) |
| api | 8000 | 8000 | localhost only (frontend + browser) |
| frontend | 3000 | 3000 | localhost only (browser) |

No TLS for MVP. Demo is localhost-only.

---

## 6. Volume Strategy

| Volume | Type | Purpose |
|--------|------|---------|
| `pgdata` | Named volume | PostgreSQL data persistence across restarts |

No other persistent volumes needed. Container images are stateless. Embedding model is baked into the API image at build time.

---

## 7. Local Development Setup

### Prerequisites

- Docker Desktop for Mac (Apple Silicon)
- Git
- `.env` file with `GROQ_API_KEY`

### First-Time Setup

```bash
# 1. Clone repository
git clone <repo-url> && cd asia

# 2. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Start everything
docker compose up --build

# 4. Run ingestion (first time only)
docker compose exec api python -m asia.services.ingestion_service

# 5. Open browser
open http://localhost:3000
```

### Daily Development

```bash
# Start services
docker compose up

# Rebuild after dependency changes
docker compose up --build

# View logs
docker compose logs -f api

# Stop
docker compose down

# Reset database
docker compose down -v && docker compose up
```

### Development Without Docker (Fallback)

If M1 memory is too tight with Docker:

```bash
# Terminal 1: PostgreSQL (install via Homebrew)
brew install postgresql@16 pgvector
brew services start postgresql@16

# Terminal 2: Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn asia.main:app --reload --port 8000

# Terminal 3: Frontend
cd frontend
npm install
npm run dev
```

---

## 8. Environment Variables

| Variable | Service | Required | Default | Description |
|----------|---------|----------|---------|-------------|
| `GROQ_API_KEY` | api | Yes | -- | Groq API key for LLM inference |
| `DATABASE_URL` | api | Yes | (set in compose) | PostgreSQL connection string |
| `EMBEDDING_MODEL` | api | No | `all-MiniLM-L6-v2` | sentence-transformers model name |
| `LOG_LEVEL` | api | No | `INFO` | Python log level |
| `LOG_FORMAT` | api | No | `json` | `json` for structured, `console` for dev |
| `POSTGRES_DB` | db | Yes | `asia` | Database name |
| `POSTGRES_USER` | db | Yes | `asia` | Database user |
| `POSTGRES_PASSWORD` | db | Yes | `asia_dev` | Database password |
| `NEXT_PUBLIC_API_URL` | frontend | Yes | `http://localhost:8000` | API base URL |

### Secret Management (MVP)

- `GROQ_API_KEY` stored in `.env` file (gitignored)
- Database credentials are hardcoded dev-only values (no production use)
- `.env.example` committed to repo with placeholder values

---

## 9. Rollback Procedure

For a local demo with recreate strategy, rollback is straightforward:

1. **Application rollback**: `git checkout <previous-tag> && docker compose up --build`
2. **Database rollback**: `docker compose down -v && docker compose up` (re-run init + ingestion)
3. **Configuration rollback**: `.env` file is local, revert manually

No database migrations for MVP (schema created fresh via init.sql). Post-MVP, add Alembic for migration management.

---

## 10. Startup Order and Health Checks

```
db (healthy) --> api (healthy) --> frontend
```

- `db`: `pg_isready` health check, 5s interval, 5 retries
- `api`: HTTP GET `/health` endpoint, 10s interval, 30s start period (embedding model load)
- `frontend`: depends on api (no health check -- Next.js dev server is fast)

The 30-second start period for the API is critical: sentence-transformers downloads and loads the model on first start.
