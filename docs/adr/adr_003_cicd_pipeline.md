# ADR 003: CI/CD Pipeline Architecture

## Status
Accepted

## Context
Need automated testing, linting, and release pipeline that:
- Validates all PRs before merge
- Automates releases on main branch
- Builds and publishes Docker images
- Uses reproducible builds

## Decision

### Two-Workflow Architecture

**ci-pr.yml** (Pull Request validation):
- Triggers on PR to main
- Steps: uv sync --frozen → ruff check → ruff format --check → pytest
- Must pass before merge

**cd-release.yml** (Release on main):
- Triggers on push to main
- Job 1: semantic-release (outputs version if released)
- Job 2: Docker build/push (conditional on release)

### Key Technical Choices

**uv sync --frozen**
Critical for reproducibility. The `--frozen` flag:
- Fails if uv.lock is out of sync with pyproject.toml
- Guarantees exact versions from lockfile
- Prevents "works on my machine" issues

**GHCR over Docker Hub**
- Native GitHub integration (uses GITHUB_TOKEN, no extra secrets)
- Unlimited public images
- Tags: `ghcr.io/scottchronicity/ephemeris-mcp:vX.Y.Z` and `:latest`

**GitHub Actions Permissions**
Workflow needs `contents: write` (for tags) and `packages: write` (for GHCR).

## Consequences
- **Positive:** Zero-touch releases, reproducible builds, no secret management for GHCR
- **Negative:** GHCR requires manual visibility change for public access
- **Tradeoff:** No PR title enforcement initially (reduces complexity)
