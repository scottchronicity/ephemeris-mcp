# Ephemeris MCP 🌌

**Precision Astronomical Ephemeris for AI Agents.**

Ephemeris MCP is a Model Context Protocol (MCP) server that provides AI agents with precision planetary positions using the **Swiss Ephemeris**.

## Quick Start

### Install via PyPI (Recommended)

```bash
# Install with uvx (recommended - fast & isolated, no local install needed)
uvx ephemeris-mcp

# Or install globally with pip
pip install ephemeris-mcp
python -m ephemeris_mcp
```

### Register with MCP Clients

Add to your MCP client configuration (client will start server on-demand):

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ephemeris-mcp": {
      "command": "uvx",
      "args": ["ephemeris-mcp"]
    }
  }
}
```

**VS Code/Cursor/Windsurf** (Cline MCP settings):

```json
{
  "mcpServers": {
    "ephemeris-mcp": {
      "command": "uvx",
      "args": ["ephemeris-mcp"]
    }
  }
}
```

The client starts the server process automatically, communicates over stdin/stdout, then terminates it when done.

## Alternative: Docker

If you prefer container isolation:

```bash
# Pull latest image
docker pull ghcr.io/scottchronicity/ephemeris-mcp:latest

# Test it
docker run --rm -i ghcr.io/scottchronicity/ephemeris-mcp:latest
```

Configure MCP client with Docker:

```json
{
  "mcpServers": {
    "ephemeris-mcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/scottchronicity/ephemeris-mcp:latest"]
    }
  }
}
```

## Local Development

```bash
# Clone and install
git clone https://github.com/scottchronicity/ephemeris-mcp.git
cd ephemeris-mcp
uv sync

# Run tests
make test

# Run locally
uv run ephemeris-mcp

# Test the engine directly
make validate-happycase
```

## Available Tools

### `get_planetary_positions`

Returns precise Tropical Zodiac positions for all planets, Sun, Moon, and chart angles.

**Parameters:**
- `iso_time` (string): ISO-8601 timestamp (e.g., `"2025-12-16T15:28:00Z"`)
- `latitude` (float): Observer latitude (default: 42.3314 - Detroit, MI)
- `longitude` (float): Observer longitude (default: -83.0458 - Detroit, MI)

**Returns:**
- `bodies`: Sun, Moon, planets with sign, degrees, motion (direct/retrograde), speed, declination
- `houses`: Ascendant (ASC) and Midheaven (MC) with sign and degrees

## Architecture

See [docs/adr/](docs/adr/) for architectural decisions:
- **ADR 001**: Geocentric Tropical Ecliptic coordinates specification
- **ADR 002**: Semantic versioning with Conventional Commits
- **ADR 003**: CI/CD pipeline architecture

## License

AGPLv3

