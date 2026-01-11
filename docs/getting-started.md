# Getting Started

## Prerequisites

- Python 3.11
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional, for containerized deployment)

## Local Development

```bash
# Clone the repository
git clone https://github.com/scottchronicity/ephemeris-mcp.git
cd ephemeris-mcp

# Install dependencies
make install

# Run tests
make test

# Start the MCP server
uv run ephemeris-mcp
```

## Docker

```bash
# Build the image
make docker-build

# Run the container
docker run -i ephemeris-mcp:latest
```

## Using with AI Agents

EphemerisMCP exposes a single MCP tool: `get_planetary_positions`

**Parameters:**
- `iso_time`: ISO-8601 timestamp (e.g., `2025-12-16T15:28:00`)
- `latitude`: Observer latitude (default: 42.3314, Detroit, MI)
- `longitude`: Observer longitude (default: -83.0458, Detroit, MI)

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
