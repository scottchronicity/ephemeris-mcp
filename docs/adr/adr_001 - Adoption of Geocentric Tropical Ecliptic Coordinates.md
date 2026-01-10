# ADR 001: Adoption of Geocentric Tropical Ecliptic Coordinates

## Status
Accepted

## Context
The system requires a spatial reference frame to reason about celestial mechanics in a way that is historically and semantically consistent with human astrological communication. 

Standard astronomical coordinate systems (Heliocentric, J2000, Equatorial) are optimized for physics and space navigation. However, these systems do not map cleanly to the symbolic logic used in astrology (Signs, Houses, Aspects). Using a raw physical model would require the agent to perform complex, error-prone transformations during every reasoning step.

We need a simplified, "Earth-as-Observer" normalized coordinate system that treats the Earth's "tilt" and the Sun's apparent path as the ground truth.

## Decision
We shall adopt the **Geocentric Tropical Ecliptic Coordinate System** as the foundational logic for all agent-based spatial reasoning. 

This system fixes the Earth at the center of the observable universe and locks the coordinate grid to the Earth's seasons (the Vernal Equinox) rather than the fixed stars (Sidereal).

## Technical Specification

### 1. The Reference Frame (Ground Truth)
The system shall utilize the following axioms for spatial positioning:

* **Center:** Geocentric (Earth Center).
* **Primary Plane:** The Ecliptic (The apparent path of the Sun around the Earth).
* **Zero Point ($0^\circ$):** The **Vernal Equinox**. This is defined as the intersection of the Ecliptic and the Celestial Equator where the Sun moves from South to North. 
    * *Note:* This effectively "locks" the coordinate system to the Earth's axial tilt. Precession of the equinoxes is accounted for by the moving reference frame, keeping the seasons aligned with the signs.

### 2. Coordinate Definitions
To minimize dimensionality, we shall represent all celestial objects using the following vector components:

* **Celestial Longitude ($\lambda$):** An angle from $0^\circ$ to $360^\circ$ along the Ecliptic.
    * *Usage:* Determines the Zodiac Sign.
    * *Calculation:* `Sign = floor(Longitude / 30)`.
* **Declination ($\delta$):** The angular distance North (+) or South (-) of the Celestial Equator.
    * *Usage:* Essential for calculating Parallels/Contra-parallels and "Out of Bounds" status.
* **Orbital Motion:** A scalar value representing daily speed.
    * *Value:* Positive for Direct, Negative for Retrograde ($R_x$).

### 3. Observable Entities
The agent shall track the following entities as distinct objects within this coordinate space:

* **The Luminaries:** Sun, Moon.
* **The Planets:** Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.
* **The Angles:** (Dependent on specific observer Topocentric coordinates)
    * *Ascendant (ASC):* Intersection of the Ecliptic and the Eastern Horizon.
    * *Midheaven (MC):* Intersection of the Ecliptic and the Local Meridian.
* **Calculated Points:**
    * *Lunar Nodes:* Mean North Node (Rahu) and South Node (Ketu).
    * *Black Moon Lilith:* Mean Lunar Apogee.

### 4. Data Exchange Schema
All internal reasoning and external communication shall utilize the following JSON structure for state vectors:

```json
{
  "meta": {
    "timestamp": "ISO-8601",
    "observer_frame": "Geocentric",
    "coordinate_system": "Tropical Zodiac"
  },
  "bodies": {
    "[BODY_NAME]": {
      "long_abs": "float (0-360)",
      "long_dms": "string (Degree Minute Second)",
      "sign": "string (Aries-Pisces)",
      "declination": "float (+/- degrees)",
      "motion_state": "direct | retrograde | stationary",
      "speed_daily": "float"
    }
  }
}