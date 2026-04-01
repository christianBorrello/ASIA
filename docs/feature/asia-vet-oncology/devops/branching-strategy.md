# Branching Strategy -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DEVOPS (Platform Design)
**Architect**: Apex (Platform Architect)
**Date**: 2026-04-01

---

## 1. Strategy: Trunk-Based Development

**Why**: 1 developer, no team coordination, 10-day timeline. Trunk-based is the simplest branching model.

### Branch Model

```
main (protected, always releasable)
  |
  +-- feature/xxx (short-lived, < 1 day)
  |     |
  |     +-- PR -> main (CI must pass)
  |
  +-- feature/yyy
        |
        +-- PR -> main
```

### Rules

1. `main` is always in a working state
2. Feature branches are short-lived (hours, not days)
3. Every merge to `main` goes through a pull request (for CI validation)
4. Squash merge to keep linear history
5. No `develop` branch, no `release/*` branches, no `hotfix/*` branches
6. Tags for demo milestones: `v0.1.0-demo`, `v0.2.0-demo`, etc.

---

## 2. Branch Naming Convention

```
feature/<short-description>     # New functionality
fix/<short-description>         # Bug fixes
chore/<short-description>       # Infrastructure, config, tooling
```

Examples:
- `feature/rag-pipeline`
- `feature/case-mode`
- `fix/citation-verification`
- `chore/docker-compose`

---

## 3. Commit Message Convention

Use Conventional Commits (lightweight):

```
type: short description

Optional body explaining why (not what).
```

Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`

Examples:
- `feat: add self-reflective citation verification`
- `fix: correct evidence scoring threshold for MODERATO`
- `chore: add mypy to pre-push hooks`
- `test: add critical query integration tests`

---

## 4. Workflow for Solo Developer

```
1. git checkout -b feature/xxx main
2. Work, commit frequently (pre-commit hooks run)
3. git push -u origin feature/xxx (pre-push hooks run)
4. Open PR on GitHub (CI runs)
5. CI passes -> squash merge to main
6. Delete feature branch
```

PRs are not for code review (solo dev) but for CI gate enforcement. The PR description serves as a lightweight changelog entry.

---

## 5. Release / Demo Tagging

```bash
# When ready for a demo milestone
git tag -a v0.1.0-demo -m "First demo: RAG pipeline + 5 critical queries"
git push origin v0.1.0-demo
```

Tags are informational. No release branches, no release automation for MVP.

---

## 6. Branch Protection (GitHub)

```
Branch: main
  Require pull request: Yes
  Required approvals: 0 (solo developer)
  Require status checks: Yes (all CI jobs)
  Require linear history: Yes
  Restrict force pushes: Yes
  Restrict deletions: Yes
```

---

## 7. Pipeline Triggers

| Trigger | Pipeline |
|---------|----------|
| Push to `main` | Full CI (lint + typecheck + test + build) |
| Pull request to `main` | Full CI (lint + typecheck + test + build) |
| Tag `v*` | Full CI (future: could add release artifacts) |

No deployment triggers. Deployment is manual: `docker compose up`.
