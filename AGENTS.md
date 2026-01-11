# AGENTS.md - AI Agent Context

> **This is the source of truth for AI agents working on this codebase.**

## Project Overview

Ephemeris MCP is a Model Context Protocol (MCP) server providing precision astronomical ephemeris calculations via the Swiss Ephemeris.

## Codebase Map

| Path | Purpose |
|------|---------|
| `src/ephemeris_mcp/server.py` | MCP server interface (FastMCP) |
| `src/ephemeris_mcp/engine.py` | Physics calculation engine (Flatlib/Swiss Ephemeris) |
| `tests/test_engine.py` | Unit tests for calculation engine |
| `docs/adr/` | Architecture Decision Records |

## Command Palette

```bash
make install      # Sync dependencies with uv
make format       # Format code with Ruff
make lint         # Lint code with Ruff
make test         # Run pytest with coverage
make docker-build # Build Docker image
make release-dry-run # Preview semantic release
make act-ci       # Run CI workflow locally
```

## Stack

- **Python:** 3.11
- **Package Manager:** uv
- **Build Backend:** hatchling
- **Linter/Formatter:** Ruff
- **Testing:** pytest + pytest-cov
- **MCP SDK:** mcp (FastMCP)
- **Astrology:** flatlib (wraps Swiss Ephemeris)

## Coding Standards

1. **Type hints required** on all function signatures
2. **Composition over inheritance**
3. **Line length:** 120 characters
4. **Imports:** sorted by Ruff (isort rules)
5. **Docstrings:** Google style

## Boundaries (DO NOT)

- Commit secrets, API keys, or tokens
- Use `print()` for debugging (use `logging`)
- Modify `uv.lock` manually (run `uv lock`)
- Skip type hints on public functions

## File Header Template

Add to new source files:

```python
# See AGENTS.md for project context and conventions
```

## Key ADRs

- **ADR 001:** Geocentric Tropical Ecliptic coordinates (why this reference frame)
- **ADR 002:** Semantic versioning with Conventional Commits
- **ADR 003:** CI/CD pipeline architecture
- **ADR 004:** Agent governance file structure
