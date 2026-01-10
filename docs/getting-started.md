# Getting Started

## Prerequisites

- Python 3.11
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional, for containerized deployment)

## Local Development

```bash
# Clone the repository
git clone https://github.com/scottchronicity/astro-mcp.git
cd astro-mcp

# Install dependencies
make install

# Run tests
make test

# Start the MCP server
uv run astro-mcp
```

## Docker

```bash
# Build the image
make docker-build

# Run the container
docker run -i astro-mcp:latest
```

## Using with AI Agents

AstroMCP exposes a single MCP tool: `get_planetary_positions`

**Parameters:**
- `iso_time`: ISO-8601 timestamp (e.g., `2026-01-10T15:00:00`)
- `latitude`: Observer latitude (default: 43.8)
- `longitude`: Observer longitude (default: -84.7)

**Returns:** JSON with planetary positions in Tropical Zodiac coordinates.

## Development Commands

| Command | Description |
|---------|-------------|
| `make install` | Sync dependencies |
| `make format` | Format code with Ruff |
| `make lint` | Lint code with Ruff |
| `make test` | Run tests with coverage |
| `make docker-build` | Build Docker image |
| `make release-dry-run` | Preview next release |
