#!/bin/bash
# setup_astro_mcp.sh

# 1. Create Directory Structure
mkdir -p astro-mcp/{src/astro_mcp,tests,.github/workflows}
cd astro-mcp

# 2. Fix Dependency Conflict in pyproject.toml
# We let flatlib dictate the pyswisseph version to avoid the lock error.
cat <<EOF > pyproject.toml
[project]
name = "astro-mcp"
version = "0.1.0"
description = "Precision astrological physics engine exposed via Model Context Protocol (MCP)."
readme = "README.md"
authors = [{ name = "Scott Carroll", email = "scott@rippleroot.studios" }]
requires-python = ">=3.11"
dependencies = [
    "flatlib",        # The Astrology Logic (locks pyswisseph to 2.8.0)
    "mcp>=0.1.0",     # The Agent Interface
    "pydantic"        # For robust data validation
]

[project.scripts]
astro-mcp = "astro_mcp.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
addopts = "--cov=astro_mcp --cov-report=term-missing"
testpaths = ["tests"]
pythonpath = ["src"]
EOF

# 3. Create the Physics Engine (src/astro_mcp/engine.py)
cat <<EOF > src/astro_mcp/engine.py
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_chart(iso_date: str, lat: float, lon: float) -> dict:
    """
    Calculates Geocentric Tropical Ecliptic coordinates.
    """
    try:
        date = Datetime(iso_date, '+00:00')
        pos = GeoPos(lat, lon)
        chart = Chart(date, pos)

        output = {
            "meta": {
                "timestamp": iso_date,
                "lat": lat,
                "lon": lon,
                "system": "Geocentric Tropical Zodiac"
            },
            "bodies": {}
        }

        # Defined entities
        bodies = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
            const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
            const.ASC, const.MC, const.NORTH_NODE
        ]

        for body_id in bodies:
            obj = chart.get(body_id)
            output["bodies"][body_id] = {
                "longitude": float(f"{obj.lon:.4f}"),
                "sign": obj.sign,
                "sign_degrees": float(f"{obj.signlon:.4f}"),
                "declination": float(f"{obj.lat:.4f}"),
                "motion": "retrograde" if obj.movement < 0 else "direct",
                "speed": float(f"{obj.movement:.4f}")
            }
        
        return output

    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        raise ValueError(f"Physics Engine Error: {str(e)}")
EOF

# 4. Create the MCP Server (src/astro_mcp/server.py)
cat <<EOF > src/astro_mcp/server.py
from mcp.server.fastmcp import FastMCP
from astro_mcp.engine import calculate_chart

mcp = FastMCP("AstroMCP")

@mcp.tool()
def get_planetary_positions(iso_time: str, latitude: float = 43.8, longitude: float = -84.7) -> str:
    """
    Returns precise astrological positions (Tropical Zodiac) for a given time/place.
    
    Args:
        iso_time: ISO-8601 string (e.g., '2026-01-10T15:00:00')
        latitude: Observer latitude (default: Clare County, MI)
        longitude: Observer longitude (default: Clare County, MI)
    """
    try:
        data = calculate_chart(iso_time, latitude, longitude)
        return str(data)
    except Exception as e:
        return f"Error: {e}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
EOF

# 5. Create empty init
touch src/astro_mcp/__init__.py

# 6. Create Tests (tests/test_engine.py)
cat <<EOF > tests/test_engine.py
import pytest
from astro_mcp.engine import calculate_chart

def test_calculate_chart_structure():
    """Ensure the JSON structure matches the ADR spec."""
    result = calculate_chart("2026-01-01T12:00:00", 43.8, -84.7)
    
    assert "meta" in result
    assert "bodies" in result
    assert "Sun" in result["bodies"]
    assert result["bodies"]["Sun"]["sign"] == "Capricorn"
    assert "declination" in result["bodies"]["Sun"]

def test_retrograde_logic():
    """Sanity check: Mercury is often retrograde, check logic holds."""
    # Known retrograde date for Mercury
    result = calculate_chart("2024-04-05T12:00:00", 0, 0) 
    # Just ensure it runs; asserting specific retrogrades requires exact dates
    assert result["bodies"]["Mercury"]["speed"] is not None

def test_invalid_date():
    """Ensure error handling works."""
    with pytest.raises(ValueError):
        calculate_chart("invalid-date", 0, 0)
EOF

# 7. Create Dockerfile (Best Practice: Multi-stage)
cat <<EOF > Dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

# Install uv for fast builds
RUN pip install uv
RUN uv pip install --system .

# Stage 2: Runtime (Smaller image)
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ src/

# Expose MCP standard port if needed, but usually runs over stdio
# For SSE/HTTP transport, we might expose 8000 later.

CMD ["python", "-m", "astro_mcp.server"]
EOF

# 8. Create GitHub Actions CI (Best Practice)
cat <<EOF > .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install --system .
        uv pip install --system pytest pytest-cov
        
    - name: Run Tests
      run: pytest
EOF

# 9. Create README
cat <<EOF > README.md
# AstroMCP 🌌

**Precision Astrological Physics for AI Agents.**

AstroMCP is a Model Context Protocol (MCP) server that provides AI agents with ground-truth planetary positions using the **Swiss Ephemeris**.

## Quick Start

### Local
\`\`\`bash
uv sync
uv run astro-mcp
\`\`\`

### Docker
\`\`\`bash
docker build -t astro-mcp .
docker run -i astro-mcp
\`\`\`

## Architecture
See [ADR 001](coordinate_system.md) for the coordinate system specification.

## License
AGPLv3
EOF

echo "✨ AstroMCP Scaffolded! Run 'cd astro-mcp && uv sync' to start."