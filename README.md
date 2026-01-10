# AstroMCP 🌌

**Precision Astrological Physics for AI Agents.**

AstroMCP is a Model Context Protocol (MCP) server that provides AI agents with ground-truth planetary positions using the **Swiss Ephemeris**.

## Quick Start

### Local
```bash
uv sync
uv run astro-mcp
```

### Docker
```bash
docker build -t astro-mcp .
docker run -i astro-mcp
```

## Architecture
See [ADR 001](coordinate_system.md) for the coordinate system specification.

## License
AGPLv3
