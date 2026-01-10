# ADR 002: Semantic Versioning with Conventional Commits

## Status
Accepted

## Context
The project needs automated version management that:
- Eliminates manual version bumping
- Generates changelogs automatically
- Triggers releases based on commit content
- Integrates with CI/CD pipelines

## Decision
Adopt **python-semantic-release** with **Conventional Commits** specification.

### Commit Format
- `feat: description` → Minor version bump (0.1.0 → 0.2.0)
- `fix: description` → Patch version bump (0.1.0 → 0.1.1)
- `feat!: description` or `BREAKING CHANGE:` → Major bump (0.1.0 → 1.0.0)
- `chore:`, `docs:`, `style:`, `refactor:`, `test:` → No release

### Version Location
Single source of truth: `pyproject.toml:project.version`

### Release Flow
1. Push to `main` with conventional commit
2. semantic-release analyzes commits since last tag
3. If releasable commits found: bump version, create tag, create GitHub Release
4. Downstream jobs (Docker build) trigger on new release

## Consequences
- **Positive:** Fully automated releases, consistent versioning, auto-generated changelogs
- **Negative:** Requires commit message discipline (enforced by PR workflow)
- **Tradeoff:** Chose `upload_to_pypi = false` initially (MCP servers distributed via Docker)
