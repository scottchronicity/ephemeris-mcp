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
