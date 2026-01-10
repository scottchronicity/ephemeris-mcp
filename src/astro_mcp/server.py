from mcp.server.fastmcp import FastMCP

from astro_mcp.engine import calculate_chart

mcp = FastMCP("AstroMCP")


@mcp.tool()
def get_planetary_positions(iso_time: str, latitude: float = 43.8, longitude: float = -84.7) -> dict:
    """
    Returns precise astrological positions (Tropical Zodiac) for a given time/place.

    Args:
        iso_time: ISO-8601 string (e.g., '2026-01-10T15:00:00')
        latitude: Observer latitude (default: Clare County, MI)
        longitude: Observer longitude (default: Clare County, MI)
    """
    data = calculate_chart(iso_date=iso_time, lat=latitude, lon=longitude)
    return data


def main():
    mcp.run()


if __name__ == "__main__":
    main()
