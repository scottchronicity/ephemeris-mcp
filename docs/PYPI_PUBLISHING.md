# PyPI Publishing Guide

This guide walks through publishing `ephemeris-mcp` to PyPI for the first time.

## Overview

The project uses:

- **Automated publishing**: GitHub Actions publishes to PyPI on every release
- **Trusted Publishing (OIDC)**: No API tokens needed in CI/CD
- **Semantic versioning**: Versions managed by `python-semantic-release`
- **Manual publishing**: Optional for testing or emergencies

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - <https://test.pypi.org/account/register/> (for testing)
   - <https://pypi.org/account/register/> (for production)

2. **Configure GitHub Repository**:
   - Go to repository Settings → Environments
   - Create environment named `pypi`
   - Add deployment protection rules if desired

3. **Set up Trusted Publishing** (Recommended):

   **On PyPI:**
   - Go to <https://pypi.org/manage/account/publishing/>
   - Click "Add a new pending publisher"
   - Fill in:
     - PyPI Project Name: `ephemeris-mcp`
     - Owner: `scottchronicity`
     - Repository name: `ephemeris-mcp`
     - Workflow name: `cd-release.yml`
     - Environment name: `pypi`

   **On TestPyPI** (for testing):
   - Go to <https://test.pypi.org/manage/account/publishing/>
   - Follow same steps as above

## First-Time Publishing

### Option 1: Automated via GitHub Actions (Recommended)

This is already configured! Just create a release:

```bash
# Make some changes and commit using Conventional Commits
git add .
git commit -m "feat: add new feature"
git push origin main

# The workflow will:
# 1. Determine version bump (feat = minor, fix = patch)
# 2. Create GitHub release with changelog
# 3. Publish to PyPI automatically
# 4. Build and push Docker image
```

The release workflow (`cd-release.yml`) handles everything automatically when you push to `main` with Conventional Commits.

### Option 2: Manual Publishing (for testing)

#### Test with Local Build

```bash
# Build the package
make build

# Test local installation
make test-pypi-local
```

#### Publish to TestPyPI

```bash
# Install twine if needed
uv pip install twine

# Get TestPyPI token:
# 1. Go to https://test.pypi.org/manage/account/token/
# 2. Create token with scope "Entire account" or specific to ephemeris-mcp
# 3. Save it securely (shows only once!)

# Set token as environment variable
export TWINE_PASSWORD="pypi-..."  # Your TestPyPI token

# Publish to TestPyPI
make publish-test
```

#### Test TestPyPI Installation

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ephemeris-mcp

# Test it works
python -c "from ephemeris_mcp.engine import calculate_chart; print('✅ Works!')"
```

#### Publish to Production PyPI

```bash
# Get PyPI token:
# 1. Go to https://pypi.org/manage/account/token/
# 2. Create token with scope "Entire account" or specific to ephemeris-mcp
# 3. Save it securely!

# Set token
export TWINE_PASSWORD="pypi-..."  # Your PyPI token

# Publish (includes confirmation prompt)
make publish
```

## Automated Publishing Workflow

The GitHub Actions workflow (`.github/workflows/cd-release.yml`) automatically:

1. **On push to `main`** (with Conventional Commit):
   - Runs `python-semantic-release` to determine version bump
   - Updates `pyproject.toml` version
   - Creates git tag (e.g., `v0.2.0`)
   - Generates changelog from commits
   - Creates GitHub Release

2. **After successful release**:
   - **PyPI Job**: Builds wheel + sdist, publishes to PyPI via Trusted Publishing
   - **Docker Job**: Builds Docker image, pushes to GHCR

## Versioning

Follows Semantic Versioning via Conventional Commits:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:` | Patch (0.1.0 → 0.1.1) | Bug fixes |
| `feat:` | Minor (0.1.0 → 0.2.0) | New features |
| `BREAKING CHANGE:` | Major (0.1.0 → 1.0.0) | Breaking changes |
| `docs:`, `chore:` | None | No release |

## Verification

After publishing, verify the package:

```bash
# Test PyPI installation
make validate-happycase-pypi

# Or manually
uvx ephemeris-mcp --help
```

Check package page:

- <https://pypi.org/project/ephemeris-mcp/>
- <https://test.pypi.org/project/ephemeris-mcp/> (TestPyPI)

## Troubleshooting

### "Filename has already been used"

- PyPI doesn't allow re-uploading same version
- Increment version in `pyproject.toml` or delete package on TestPyPI

### "Invalid or non-existent authentication information"

- Check `TWINE_PASSWORD` is set correctly
- Verify token hasn't expired
- Ensure token has correct scope

### "Trusted publishing not configured"

- Complete Trusted Publishing setup on PyPI (see Prerequisites)
- Verify environment name matches (`pypi`)
- Check workflow name is correct (`cd-release.yml`)

### Build fails in CI

```bash
# Test build locally
make build
make test-pypi-local
```

## Security Notes

- **Never commit API tokens** to git
- Use Trusted Publishing for CI/CD (no tokens needed)
- For manual publishing, use environment variables
- Tokens are scoped: create project-specific tokens when possible

## Resources

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Python Semantic Release Docs](https://python-semantic-release.readthedocs.io/)
- [Conventional Commits Spec](https://www.conventionalcommits.org/)
