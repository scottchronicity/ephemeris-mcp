# Makefile for EphemerisMCP

# Variables
IMAGE_NAME := ephemeris-mcp
VERSION := 0.1.0
PYTHON_VERSION := 3.11

.PHONY: all help install format lint test build clean docker-build docker-run docker-happycase-public docker-happycase-mcp act

all: install format lint test

help:
	@echo "Ephemeris MCP Development Commands"
	@echo "==================================="
	@echo "make install      - Sync dependencies (uses Python $(PYTHON_VERSION))"
	@echo "make format       - Format code using Ruff"
	@echo "make format-check - Check code formatting without modifying"
	@echo "make lint         - Lint code using Ruff"
	@echo "make test         - Run tests with coverage"
	@echo "make validate-dev - Run development validation (install, lint, format-check, test)"
	@echo "make clean        - Remove artifacts and cache"
	@echo "make docker-build     - Build the Docker image"
	@echo "make docker-run       - Run the Docker container interactively"
	@echo "make docker-happycase - Test the Docker image with a simple query"
	@echo "make docker-happycase-public - Test the public GHCR image with a simple query"
	@echo "make docker-happycase-mcp - Test the MCP server interface (agent-style)"
	@echo "make docker-dev       - Full Docker dev workflow (validate, build, test)"
	@echo "make docker-clean     - Remove Docker images"
	@echo "make validate-happycase - Test engine locally with a simple query"
	@echo "make act          - Run GitHub Actions locally (requires 'act')"
	@echo "make release-dry-run - Dry-run semantic release"
	@echo "make audit        - Audit dependencies"
	@echo "make act-ci       - Run CI workflow locally with act"
	@echo "make act-release  - Run Release workflow locally with act (dry-run)"
	@echo ""
	@echo "PyPI Publishing:"
	@echo "make build        - Build distribution packages (wheel + sdist)"
	@echo "make test-pypi-local - Test local build installation"
	@echo "make validate-happycase-pypi - Test PyPI installed version"
	@echo "make publish-test - Publish to TestPyPI (requires API token)"
	@echo "make publish      - Publish to PyPI (requires API token)"

# --- Development ---

lock:
	@echo "🔒 Locking dependencies..."
	uv lock

sync: lock
	@echo "📦 Syncing dependencies with Python $(PYTHON_VERSION)..."
	uv sync --all-groups --python $(PYTHON_VERSION)

install: sync
	@echo "✅ Dependencies installed."

format:
	@echo "✨ Formatting code..."
	uv run ruff format .

format-check:
	@echo "🔍 Checking code formatting..."
	uv run ruff format --check .

lint:
	@echo "🔍 Linting code..."
	uv run ruff check . --fix

test:
	@echo "🧪 Running tests..."
	uv run pytest

validate-dev:
	@echo "🔍 Running simple development validation..."
	$(MAKE) install
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) test
	@echo "✅ Development simple validation complete!"

validate-happycase:
	@echo "🧪 Testing engine locally with planetary positions query..."
	@echo "📍 Querying: 2025-12-16T15:28:00Z at New York (40.7128, -74.0060)"
	@uv run python -c "from ephemeris_mcp.engine import calculate_chart; result = calculate_chart('2025-12-16T15:28:00Z', 40.7128, -74.0060); print('✅ Engine working!\n'); print('🌟 BODIES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}° ({data[\"motion\"]})') for name, data in result['bodies'].items()]; print('\n🏠 HOUSES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}°') for name, data in result['houses'].items()]"
	@echo "\n✅ Happy case test passed!"

validate-dev-full: validate-dev
	@echo "🔍 Running full development validation..."
	$(MAKE) release-dry-run
	@echo "🎬 Running act-ci (expected to fail locally with exit code 1)..."
	-$(MAKE) act-ci || echo "✅ act-ci failed as expected in local environment"
	@echo "✅ Full development validation complete!"

clean:
	@echo "🧹 Cleaning up..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

# --- Docker ---

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t $(IMAGE_NAME):$(VERSION) .
	docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest
	@echo "✅ Docker image built: $(IMAGE_NAME):$(VERSION) and $(IMAGE_NAME):latest"

docker-run:
	@echo "🚀 Running container interactively..."
	docker run -it --rm $(IMAGE_NAME):latest

docker-happycase:
	@echo "🧪 Testing Docker image with planetary positions query..."
	@echo "📍 Querying: 2025-12-16T15:28:00Z at New York (40.7128, -74.0060)"
	@docker run --rm $(IMAGE_NAME):latest python -c "from ephemeris_mcp.engine import calculate_chart; import json; result = calculate_chart('2025-12-16T15:28:00Z', 40.7128, -74.0060); print('✅ Docker image working!\n'); print('🌟 BODIES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}° ({data[\"motion\"]})') for name, data in result['bodies'].items()]; print('\n🏠 HOUSES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}°') for name, data in result['houses'].items()]"
	@echo "\n✅ Docker test passed!"

docker-happycase-public:
	@echo "🧪 Testing public GHCR image with planetary positions query..."
	@echo "📦 Pulling ghcr.io/scottchronicity/ephemeris-mcp:latest..."
	@docker pull ghcr.io/scottchronicity/ephemeris-mcp:latest
	@echo "📍 Querying: 2025-12-16T15:28:00Z at New York (40.7128, -74.0060)"
	@docker run --rm ghcr.io/scottchronicity/ephemeris-mcp:latest python -c "from ephemeris_mcp.engine import calculate_chart; import json; result = calculate_chart('2025-12-16T15:28:00Z', 40.7128, -74.0060); print('✅ Public image working!\n'); print('🌟 BODIES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}° ({data[\"motion\"]})') for name, data in result['bodies'].items()]; print('\n🏠 HOUSES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}°') for name, data in result['houses'].items()]"
	@echo "\n✅ Public image test passed!"

docker-happycase-mcp:
	@echo "🧪 Testing MCP server interface (agent-style)..."
	@python3 test_mcp_client.py

docker-dev: validate-dev docker-build docker-happycase
	@echo "✅ Full Docker dev workflow complete!"
	@echo "📦 Image ready: $(IMAGE_NAME):$(VERSION)"
	@echo "🚀 To run: make docker-run"

docker-clean:
	@echo "🧹 Removing Docker images..."
	docker rmi $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest || true
	@echo "✅ Docker images removed"

# --- CI/CD (Local) ---

act:
	@echo "🎬 Running GitHub Actions locally..."
	# Requires 'act' installed via brew install act
	act -j test --container-architecture linux/amd64

release-dry-run:
	@echo "🔍 Dry-run semantic release..."
	uv run semantic-release version --print --no-commit --no-push --no-tag

audit:
	@echo "🔒 Auditing dependencies..."
	uv pip compile pyproject.toml -o /dev/null --quiet && echo "✅ Dependencies resolve cleanly"

act-ci:
	@echo "🎬 Running CI workflow locally with act..."
	act pull_request --container-architecture linux/amd64 -W .github/workflows/ci-pr.yml

act-release:
	@echo "🎬 Running Release workflow locally with act (dry-run)..."
	act push --container-architecture linux/amd64 -W .github/workflows/cd-release.yml --dryrun
# --- PyPI Publishing ---

build:
	@echo "📦 Building distribution packages..."
	uv build
	@echo "✅ Build complete! Check dist/ directory"
	@ls -lh dist/

test-pypi-local:
	@echo "🧪 Testing local build installation..."
	@echo "Creating fresh virtual environment for testing..."
	@rm -rf /tmp/ephemeris-mcp-test-env
	@uv venv /tmp/ephemeris-mcp-test-env
	@echo "Installing from local build..."
	@uv pip install --python /tmp/ephemeris-mcp-test-env dist/*.whl
	@echo "Testing import..."
	@/tmp/ephemeris-mcp-test-env/bin/python -c "from ephemeris_mcp.engine import calculate_chart; print('✅ Import successful')"
	@echo "Testing entry point exists..."
	@test -f /tmp/ephemeris-mcp-test-env/bin/ephemeris-mcp && echo "✅ CLI entry point installed" || echo "❌ Entry point missing"
	@echo "Testing engine with sample query..."
	@/tmp/ephemeris-mcp-test-env/bin/python -c "from ephemeris_mcp.engine import calculate_chart; result = calculate_chart('2025-12-16T15:28:00Z', 40.7128, -74.0060); print(f'✅ Engine working! Sun in {result[\"bodies\"][\"Sun\"][\"sign\"]}')"
	@echo "✅ Local build test passed!"
	@rm -rf /tmp/ephemeris-mcp-test-env

validate-happycase-pypi:
	@echo "🧪 Testing PyPI installed version..."
	@echo "Creating fresh virtual environment..."
	@rm -rf /tmp/ephemeris-mcp-pypi-test
	@uv venv /tmp/ephemeris-mcp-pypi-test
	@echo "Installing from PyPI..."
	@uv pip install --python /tmp/ephemeris-mcp-pypi-test ephemeris-mcp
	@echo "📍 Querying: 2025-12-16T15:28:00Z at New York (40.7128, -74.0060)"
	@/tmp/ephemeris-mcp-pypi-test/bin/python -c "from ephemeris_mcp.engine import calculate_chart; result = calculate_chart('2025-12-16T15:28:00Z', 40.7128, -74.0060); print('✅ PyPI version working!\n'); print('🌟 BODIES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}° ({data[\"motion\"]})') for name, data in result['bodies'].items()]; print('\n🏠 HOUSES:'); [print(f'  {name:18} {data[\"sign\"]:10} {data[\"sign_degrees\"]:6.2f}°') for name, data in result['houses'].items()]"
	@echo "\n✅ PyPI happy case test passed!"
	@rm -rf /tmp/ephemeris-mcp-pypi-test

publish-test:
	@echo "🚀 Publishing to TestPyPI..."
	@echo "⚠️  Requires TWINE_PASSWORD env var with TestPyPI token"
	@uv build
	@uv run twine upload --repository testpypi dist/* --username __token__

publish:
	@echo "🚀 Publishing to PyPI..."
	@echo "⚠️  Requires TWINE_PASSWORD env var with PyPI token"
	@echo "⚠️  This will publish to production PyPI!"
	@read -p "Are you sure? [y/N] " -n 1 -r; echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv build && uv run twine upload dist/* --username __token__; \
	else \
		echo "Cancelled."; \
	fi
