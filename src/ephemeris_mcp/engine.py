import datetime

import structlog
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

logger = structlog.get_logger(__name__)


def calculate_chart(iso_date: str, lat: float, lon: float) -> dict:
    """
    Calculates Geocentric Tropical Ecliptic coordinates.
    Uses Swiss Ephemeris via Flatlib.
    """
    try:
        # 1. Parse ISO string using standard lib
        # Replace Z with +00:00 to ensure Python handles UTC correctly
        dt = datetime.datetime.fromisoformat(iso_date.replace("Z", "+00:00"))

        # 2. Convert to Flatlib's specific requirements
        flat_date = dt.strftime("%Y/%m/%d")
        flat_time = dt.strftime("%H:%M:%S")

        date = Datetime(flat_date, flat_time, "+00:00")
        pos = GeoPos(lat, lon)

        # Calculate the chart with all planets including outer planets
        # Note: Angles (ASC, MC) are calculated automatically and accessed via chart.get()
        chart = Chart(
            date,
            pos,
            IDs=[
                const.SUN,
                const.MOON,
                const.MERCURY,
                const.VENUS,
                const.MARS,
                const.JUPITER,
                const.SATURN,
                const.URANUS,
                const.NEPTUNE,
                const.PLUTO,
                const.NORTH_NODE,
                const.SOUTH_NODE,
                const.CHIRON,
            ],
        )

        output = {
            "meta": {"timestamp": iso_date, "lat": lat, "lon": lon, "system": "Geocentric Tropical Zodiac"},
            "bodies": {},
            "houses": {},
        }

        # Define bodies to track
        bodies = [
            (const.SUN, "Sun"),
            (const.MOON, "Moon"),
            (const.MERCURY, "Mercury"),
            (const.VENUS, "Venus"),
            (const.MARS, "Mars"),
            (const.JUPITER, "Jupiter"),
            (const.SATURN, "Saturn"),
            (const.URANUS, "Uranus"),
            (const.NEPTUNE, "Neptune"),
            (const.PLUTO, "Pluto"),
            (const.NORTH_NODE, "North Node"),
            (const.SOUTH_NODE, "South Node"),
            (const.CHIRON, "Chiron"),
        ]

        # Define angles to track
        angles = [
            (const.ASC, "Ascendant"),
            (const.MC, "Midheaven"),
            (const.DESC, "Descendant"),
            (const.IC, "Imum Coeli"),
        ]

        # Define house cusps to track
        houses = [
            (const.HOUSE1, "House 1"),
            (const.HOUSE2, "House 2"),
            (const.HOUSE3, "House 3"),
            (const.HOUSE4, "House 4"),
            (const.HOUSE5, "House 5"),
            (const.HOUSE6, "House 6"),
            (const.HOUSE7, "House 7"),
            (const.HOUSE8, "House 8"),
            (const.HOUSE9, "House 9"),
            (const.HOUSE10, "House 10"),
            (const.HOUSE11, "House 11"),
            (const.HOUSE12, "House 12"),
        ]

        for body_id, friendly_name in bodies:
            try:
                obj = chart.get(body_id)
                speed = getattr(obj, "lonspeed", 0.0)

                output["bodies"][friendly_name] = {
                    "longitude": float(f"{obj.lon:.4f}"),
                    "sign": str(obj.sign),
                    "sign_degrees": float(f"{obj.signlon:.4f}"),
                    "declination": float(f"{obj.lat:.4f}"),
                    "motion": "retrograde" if speed < 0 else "direct",
                    "speed": float(f"{speed:.4f}"),
                }
            except (KeyError, AttributeError) as e:
                logger.warning(
                    "Could not calculate body",
                    body=friendly_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                continue

        # Process angles (ASC, MC, DESC, IC)
        for angle_id, friendly_name in angles:
            try:
                obj = chart.get(angle_id)
                output["bodies"][friendly_name] = {
                    "longitude": float(f"{obj.lon:.4f}"),
                    "sign": str(obj.sign),
                    "sign_degrees": float(f"{obj.signlon:.4f}"),
                    "declination": float(f"{obj.lat:.4f}"),
                    "motion": "direct",
                    "speed": 0.0,
                }
            except (KeyError, AttributeError) as e:
                logger.warning(
                    "Could not calculate angle",
                    angle=friendly_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                continue

        # Process house cusps
        for house_id, friendly_name in houses:
            try:
                obj = chart.get(house_id)
                output["houses"][friendly_name] = {
                    "longitude": float(f"{obj.lon:.4f}"),
                    "sign": str(obj.sign),
                    "sign_degrees": float(f"{obj.signlon:.4f}"),
                }
            except (KeyError, AttributeError) as e:
                logger.warning(
                    "Could not calculate house",
                    house=friendly_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                continue

        return output

    except Exception as e:
        logger.error(
            "Calculation failed",
            error=str(e),
            error_type=type(e).__name__,
            iso_date=iso_date,
            lat=lat,
            lon=lon,
            exc_info=True,
        )
        raise ValueError(f"Physics Engine Error: {str(e)}")
