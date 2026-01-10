from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        flat_date = dt.strftime('%Y/%m/%d')
        flat_time = dt.strftime('%H:%M:%S')
        
        date = Datetime(flat_date, flat_time, '+00:00')
        pos = GeoPos(lat, lon)
        
        # Calculate the chart with all planets including outer planets
        # Note: Angles (ASC, MC, NORTH_NODE) cannot be included in IDs parameter
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
                const.PLUTO
            ]
        )

        output = {
            "meta": {
                "timestamp": iso_date,
                "lat": lat,
                "lon": lon,
                "system": "Geocentric Tropical Zodiac"
            },
            "bodies": {}
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
            (const.ASC, "Ascendant"),
            (const.MC, "Midheaven"),
            (const.NORTH_NODE, "North Node")
        ]

        for body_id, friendly_name in bodies:
            try:
                obj = chart.get(body_id)
                
                # Access speed directly from the object attribute
                # Angles (ASC/MC) might not have speed, default to 0.0
                speed = getattr(obj, 'lonspeed', 0.0)
                
                output["bodies"][friendly_name] = {
                    "longitude": float(f"{obj.lon:.4f}"),
                    "sign": str(obj.sign),
                    "sign_degrees": float(f"{obj.signlon:.4f}"),
                    "declination": float(f"{obj.lat:.4f}"),
                    "motion": "retrograde" if speed < 0 else "direct",
                    "speed": float(f"{speed:.4f}")
                }
            except KeyError:
                # Skip planets that couldn't be calculated
                logger.warning(f"Could not calculate {friendly_name}")
                continue
        
        return output

    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        raise ValueError(f"Physics Engine Error: {str(e)}")
