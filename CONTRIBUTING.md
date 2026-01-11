# Contributing to EphemerisMCP

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ephemeris-mcp.git`
3. Install dependencies: `make install`
4. Create a branch: `git checkout -b feat/your-feature`

## Development Workflow

```bash
# Make changes, then:
make format  # Auto-format code
make lint    # Check for issues
make test    # Run tests
```

## Commit Messages

We use **Conventional Commits** for automated releases:

| Prefix | Purpose | Version Bump |
|--------|---------|--------------|
| `feat:` | New feature | Minor (0.1.0 → 0.2.0) |
| `fix:` | Bug fix | Patch (0.1.0 → 0.1.1) |
| `docs:` | Documentation | None |
| `chore:` | Maintenance | None |
| `refactor:` | Code restructure | None |
| `test:` | Test changes | None |

**Examples:**
- `feat: add lunar phase calculation`
- `fix: correct retrograde detection for Mercury`
- `docs: update API examples`

## Pull Request Process

1. Ensure all tests pass: `make test`
2. Ensure code is formatted: `make format`
3. Update documentation if needed
4. Submit PR with descriptive title (Conventional Commit format)
5. Wait for CI to pass
6. Request review

## Code Standards

- Type hints on all functions
- Docstrings on public functions
- No `print()` statements (use `logging`)
- See `AGENTS.md` for full guidelines

## Questions?

Open an issue with the `question` label.
