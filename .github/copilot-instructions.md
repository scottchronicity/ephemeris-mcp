# GitHub Copilot Instructions for Ephemeris MCP

## What This Project Does
Ephemeris MCP is an MCP (Model Context Protocol) server that calculates planetary positions using the Swiss Ephemeris. It provides AI agents with precision astronomical ephemeris data in Tropical Zodiac coordinates.

## Architecture
- `server.py`: FastMCP server exposing `get_planetary_positions` tool
- `engine.py`: Wraps Flatlib to calculate positions for Sun, Moon, planets, angles
- Coordinate system: Geocentric Tropical Ecliptic (Earth-centered, season-aligned)

## Key Technical Details
- Swiss Ephemeris accessed via `flatlib` library
- All times in UTC (ISO-8601 format)
- Positions include: longitude, sign, degrees, declination, motion (direct/retrograde), speed
- Angles (ASC, MC) require geographic coordinates

## When Writing Code
- Always add type hints
- Use `logging.getLogger(__name__)` for logs
- Raise `ValueError` for invalid inputs
- Follow Conventional Commits for commit messages
- Run `make test` before suggesting commits

## File References
- See `AGENTS.md` for full context
- See `docs/adr/` for architectural decisions
- See `.cursorrules` for style rules
