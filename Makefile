# Makefile for AstroMCP

# Variables
IMAGE_NAME := astro-mcp
VERSION := 0.1.0
PYTHON_VERSION := 3.11

.PHONY: all help install format lint test build clean docker-build docker-run act

all: install format lint test

help:
	@echo "AstroMCP Development Commands"
	@echo "============================="
	@echo "make install      - Sync dependencies (uses Python $(PYTHON_VERSION))"
	@echo "make format       - Format code using Ruff"
	@echo "make lint         - Lint code using Ruff"
	@echo "make test         - Run tests with coverage"
	@echo "make clean        - Remove artifacts and cache"
	@echo "make docker-build - Build the Docker image"
	@echo "make docker-run   - Run the Docker container"
	@echo "make act          - Run GitHub Actions locally (requires 'act')"

# --- Development ---

install:
	@echo "📦 Syncing dependencies with Python $(PYTHON_VERSION)..."
	uv sync --python $(PYTHON_VERSION)

format:
	@echo "✨ Formatting code..."
	uv run ruff format .

lint:
	@echo "🔍 Linting code..."
	uv run ruff check . --fix

test:
	@echo "🧪 Running tests..."
	uv run pytest

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

docker-run:
	@echo "🚀 Running container..."
	docker run -it --rm $(IMAGE_NAME):latest

# --- CI/CD (Local) ---

act:
	@echo "🎬 Running GitHub Actions locally..."
	# Requires 'act' installed via brew install act
	act -j test --container-architecture linux/amd64
