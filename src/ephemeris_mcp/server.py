from mcp.server.fastmcp import FastMCP

from ephemeris_mcp.engine import calculate_chart
from ephemeris_mcp.logging_config import setup_logging

# Initialize logging
setup_logging()

mcp = FastMCP("EphemerisMCP")


@mcp.tool()
def get_planetary_positions(iso_time: str, latitude: float = 42.3314, longitude: float = -83.0458) -> dict:
    """
    Returns precise astrological positions (Tropical Zodiac) for a given time/place.

    Args:
        iso_time: ISO-8601 string (e.g., '2025-12-16T15:28:00')
        latitude: Observer latitude (default: Detroit, MI)
        longitude: Observer longitude (default: Detroit, MI)
    """
    data = calculate_chart(iso_date=iso_time, lat=latitude, lon=longitude)
    return data


def main():
    mcp.run()


if __name__ == "__main__":
    main()
