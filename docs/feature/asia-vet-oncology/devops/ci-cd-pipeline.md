# CI/CD Pipeline -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## 1. Pipeline Overview

CI only (no CD). The demo is local -- deployment is `docker compose up`.

**Target**: < 5 minutes total pipeline time.
**Platform**: GitHub Actions (free for public repos).
**Trigger**: Push to `main`, pull requests to `main`.

```
Push/PR --> Lint+Format --> Type Check --> Unit Tests --> Build Verification
              (ruff)        (mypy +        (pytest +        (docker
                            tsc)           vitest)          compose build)
```

---

## 2. Local Quality Gates (Pre-commit / Pre-push)

### Pre-commit Hooks (< 30 seconds)

Run on every `git commit` via the `pre-commit` framework.

```yaml
# .pre-commit-config.yaml
repos:
  # Python formatting + linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Secrets scanning
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Frontend formatting
  - repo: local
    hooks:
      - id: prettier
        name: prettier
        entry: npx prettier --write --ignore-unknown
        language: system
        files: '\.(ts|tsx|js|jsx|json|css|md)$'
        pass_filenames: true

      - id: eslint
        name: eslint
        entry: npx eslint --fix
        language: system
        files: '\.(ts|tsx|js|jsx)$'
        pass_filenames: true
```

### Pre-push Hooks (< 2 minutes)

Run on every `git push` for heavier checks.

```yaml
# In .pre-commit-config.yaml, add stages
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: mypy backend/asia --ignore-missing-imports
        language: system
        types: [python]
        stages: [pre-push]
        pass_filenames: false

      - id: tsc
        name: typescript check
        entry: npx tsc --noEmit
        language: system
        files: '\.(ts|tsx)$'
        stages: [pre-push]
        pass_filenames: false

      - id: pytest-fast
        name: pytest (unit only)
        entry: pytest backend/tests/unit -x -q --no-header
        language: system
        types: [python]
        stages: [pre-push]
        pass_filenames: false

      - id: vitest
        name: vitest
        entry: npx vitest run
        language: system
        files: '\.(ts|tsx)$'
        stages: [pre-push]
        pass_filenames: false
```

### Setup

```bash
# Install pre-commit
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

---

## 3. GitHub Actions Workflow

### Commit Stage Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ──────────────────────────────────────────────
  # Backend checks (parallel)
  # ──────────────────────────────────────────────
  backend-lint:
    name: Backend Lint + Format
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check backend/
      - run: ruff format --check backend/

  backend-typecheck:
    name: Backend Type Check
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r backend/requirements.txt mypy
      - run: mypy backend/asia --ignore-missing-imports

  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: asia_test
          POSTGRES_USER: asia
          POSTGRES_PASSWORD: asia_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U asia"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r backend/requirements.txt -r backend/requirements-test.txt
      - name: Run unit tests
        run: pytest backend/tests/unit -v --tb=short --junitxml=reports/unit.xml
      - name: Run integration tests
        run: pytest backend/tests/integration -v --tb=short --junitxml=reports/integration.xml
        env:
          DATABASE_URL: postgresql+asyncpg://asia:asia_test@localhost:5432/asia_test
      - name: Coverage report
        run: |
          pytest backend/tests/unit backend/tests/integration \
            --cov=backend/asia --cov-report=term --cov-report=json:reports/coverage.json \
            --tb=short
      - name: Coverage gate
        run: |
          COVERAGE=$(python -c "import json; print(json.load(open('reports/coverage.json'))['totals']['percent_covered'])")
          echo "Coverage: ${COVERAGE}%"
          python -c "
          import json, sys
          cov = json.load(open('reports/coverage.json'))['totals']['percent_covered']
          if cov < 70:
              print(f'FAIL: Coverage {cov}% is below 70% threshold')
              sys.exit(1)
          print(f'PASS: Coverage {cov}% meets 70% threshold')
          "

  backend-architecture:
    name: Architecture Enforcement
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install import-linter -r backend/requirements.txt
      - run: cd backend && lint-imports

  # ──────────────────────────────────────────────
  # Frontend checks (parallel)
  # ──────────────────────────────────────────────
  frontend-lint:
    name: Frontend Lint + Format
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm ci
      - run: cd frontend && npx eslint src/
      - run: cd frontend && npx prettier --check src/

  frontend-typecheck:
    name: Frontend Type Check
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm ci
      - run: cd frontend && npx tsc --noEmit

  frontend-test:
    name: Frontend Tests
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm ci
      - run: cd frontend && npx vitest run --reporter=verbose

  # ──────────────────────────────────────────────
  # Security scanning (parallel)
  # ──────────────────────────────────────────────
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Gitleaks (secrets detection)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # ──────────────────────────────────────────────
  # Build verification (depends on all checks)
  # ──────────────────────────────────────────────
  build:
    name: Docker Compose Build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs:
      - backend-lint
      - backend-typecheck
      - backend-test
      - backend-architecture
      - frontend-lint
      - frontend-typecheck
      - frontend-test
      - security
    steps:
      - uses: actions/checkout@v4
      - name: Build all images
        run: docker compose build
```

---

## 4. Quality Gates Summary

| Gate | Stage | Type | Threshold | Tool |
|------|-------|------|-----------|------|
| Python formatting | Local + CI | Blocking | Zero violations | ruff format |
| Python linting | Local + CI | Blocking | Zero violations | ruff check |
| TypeScript linting | Local + CI | Blocking | Zero violations | eslint |
| TypeScript formatting | Local + CI | Blocking | Zero violations | prettier |
| Python type checking | Pre-push + CI | Blocking | Zero errors | mypy |
| TypeScript type checking | Pre-push + CI | Blocking | Zero errors | tsc |
| Python unit tests | Pre-push + CI | Blocking | 100% pass | pytest |
| Python integration tests | CI | Blocking | 100% pass | pytest |
| Frontend tests | Pre-push + CI | Blocking | 100% pass | vitest |
| Code coverage | CI | Blocking | >= 70% | pytest-cov |
| Architecture enforcement | CI | Blocking | Zero violations | import-linter |
| Secrets detection | Local + CI | Blocking | Zero secrets | gitleaks |
| Docker build | CI | Blocking | Successful build | docker compose |

### Coverage Target: 70% (not 80%)

Standard production target is 80%. For this MVP with a 10-day timeline, 70% is realistic. The 5 critical query integration tests provide more quality signal than raw coverage percentage. Raise to 80% post-MVP.

---

## 5. Pipeline Timing Budget

| Job | Estimated Time | Parallel Group |
|-----|---------------|----------------|
| backend-lint | ~30s | Group A |
| backend-typecheck | ~60s | Group A |
| backend-test | ~120s | Group A |
| backend-architecture | ~30s | Group A |
| frontend-lint | ~30s | Group A |
| frontend-typecheck | ~30s | Group A |
| frontend-test | ~30s | Group A |
| security | ~30s | Group A |
| build | ~120s | Group B (sequential) |

**Total estimated time**: ~4 minutes (Group A parallel: ~2 min, Group B: ~2 min). Within the < 5 minute target.

---

## 6. Caching Strategy

| Cache | Key | Path |
|-------|-----|------|
| pip | `runner.os-pip-hashFiles('**/requirements.txt')` | `~/.cache/pip` |
| npm | `runner.os-npm-hashFiles('frontend/package-lock.json')` | `~/.npm` |
| Docker layers | Built-in Docker BuildKit cache | -- |

GitHub Actions caches are free for public repos. Caching reduces typical run from ~4 min to ~3 min.

---

## 7. Branch Protection Rules

Configure on GitHub after repository creation:

```
Branch: main
- Require pull request before merging: Yes
  - Required approvals: 0 (solo developer -- self-merge allowed)
  - Dismiss stale reviews: N/A
- Require status checks to pass: Yes
  - Required checks:
    - backend-lint
    - backend-typecheck
    - backend-test
    - backend-architecture
    - frontend-lint
    - frontend-typecheck
    - frontend-test
    - security
    - build
- Require linear history: Yes (squash merge)
- Restrict force pushes: Yes
- Restrict deletions: Yes
```

Solo developer note: PR reviews are not enforced (0 approvals required) but the developer should still create PRs for CI validation before merging to main.

---

## 8. Future CI Additions (Post-MVP)

Not included now, but documented for post-MVP:

| Addition | When | Why |
|----------|------|-----|
| Contract tests (pact-python) | After external API integration stabilizes | Validate Groq/PubMed/SemanticScholar contracts |
| Critical query acceptance tests | After RAG pipeline is functional | The 5 critical queries as CI acceptance stage |
| DAST scanning (OWASP ZAP) | If exposed beyond localhost | Not needed for local demo |
| Dependency scanning (Trivy) | Post-MVP | SCA for Python/Node dependencies |
| Container image scanning | Post-MVP | Scan built images for vulnerabilities |
| Performance tests | Post-MVP | SSE streaming latency benchmarks |
