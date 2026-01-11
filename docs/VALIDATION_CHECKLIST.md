# Validation Checklist

Complete these steps IN ORDER after implementation is complete.

## Phase 1: Local Validation (5 minutes)

- [x] Run `make install` - should complete without errors
- [x] Run `make lint` - should pass with no issues
- [x] Run `make test` - all tests should pass
- [x] Run `make release-dry-run` - should show version analysis
- [x] Run `make act-ci` - should simulate PR workflow successfully

## Phase 2: Git & Push (2 minutes)

- [x] Review changed files: `git status`
- [x] Stage all changes: `git add -A`
- [x] Commit: `git commit -m "feat: add production CI/CD and agent governance"`
- [x] Push: `git push origin main`

## Phase 3: Verify GitHub Actions (3 minutes)

- [x] Go to GitHub → Actions tab
- [x] Verify "Release" workflow triggered
- [x] Watch workflow complete (should create v0.2.0 release)
- [ ] Check Releases page for new release with changelog

## Phase 4: Verify Docker Image (2 minutes)

- [x] Go to GitHub → Packages (right sidebar)
- [x] Find `ephemeris-mcp` package (<https://github.com/scottchronicity/ephemeris-mcp/pkgs/container/ephemeris-mcp>)
- [x] Verify tags: `v0.2.0` and `latest` (latest
v1.0.0))

## Phase 5: GHCR Public Access (Optional)

If you want the Docker image publicly pullable:

1. Go to GitHub → Packages → ephemeris-mcp
2. Click "Package settings"
3. Scroll to "Danger Zone"
4. Click "Change visibility" → Public

Test:

```bash
docker pull ghcr.io/scottchronicity/ephemeris-mcp:latest
docker run -i ghcr.io/scottchronicity/ephemeris-mcp:latest
```

## Phase 6: PyPI Setup (Optional, Later)

1. Create account at <https://pypi.org>
2. Go to Account Settings → API tokens → Add token
3. In GitHub: Settings → Secrets → Actions → New secret
   - Name: `PYPI_TOKEN`
   - Value: (paste token)
4. Edit `pyproject.toml`: change `upload_to_pypi = false` to `true`
5. Commit and push to trigger release with PyPI upload

## Troubleshooting

### `make act-ci` fails with Docker errors

- Ensure Docker Desktop is running
- Try: `docker system prune -f`
- If on Apple Silicon: ensure act uses `--container-architecture linux/amd64`

### Release workflow shows "No release will be made"

- Commit messages must follow Conventional Commits
- Use `feat:` for minor bump, `fix:` for patch
- `chore:` and `docs:` do NOT trigger releases

### GHCR push fails with 403

1. Go to repo Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Save

### semantic-release can't push tags

- Ensure `fetch-depth: 0` in checkout step
- Verify GITHUB_TOKEN has write access
