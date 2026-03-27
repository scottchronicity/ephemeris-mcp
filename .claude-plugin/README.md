# ephemeris-mcp

Precision astronomical ephemeris for AI agents. Provides planetary positions and chart angles via the Swiss Ephemeris.

## Quick Start

```
/plugin install scottchronicity/ephemeris-mcp
```

No manual setup required — the plugin uses `uvx` for zero-install execution directly from PyPI.

## Features

- **Swiss Ephemeris Integration** — High-precision planetary calculations powered by the Swiss Ephemeris via Flatlib
- **Tropical Zodiac Coordinates** — Geocentric tropical ecliptic positions aligned to the vernal equinox
- **Complete Celestial Coverage** — Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron, and Lunar Nodes
- **House Cusps & Angles** — All 12 house cusps plus Ascendant, Midheaven, Descendant, and Imum Coeli
- **Retrograde Detection** — Reports direct/retrograde motion status and longitudinal speed for every body

## Tools

### `get_planetary_positions`

Returns precise tropical zodiac positions for a given time and place.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `iso_time` | string | Yes | ISO-8601 datetime (e.g. `2025-12-16T15:28:00`) |
| `latitude` | float | No | Observer latitude (default: 42.3314) |
| `longitude` | float | No | Observer longitude (default: -83.0458) |

**Returns:** Positions for 13 celestial bodies and 4 angular points, each including longitude, zodiac sign, sign degrees, declination, motion, and speed. Plus all 12 house cusps.
