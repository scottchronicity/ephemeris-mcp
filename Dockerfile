# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy manifest
COPY pyproject.toml .
COPY .python-version .

# Install dependencies (system-wide for Docker)
RUN uv pip install --system .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ src/

# Run via module
CMD ["python", "-m", "astro_mcp.server"]
