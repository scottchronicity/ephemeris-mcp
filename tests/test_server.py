# See AGENTS.md for project context and conventions

import json
from unittest.mock import patch

import pytest


class TestGetPlanetaryPositionsTool:
    """Test suite for the get_planetary_positions MCP tool."""

    @pytest.fixture
    def mock_calculate_chart(self):
        """Mock the calculate_chart function to avoid Swiss Ephemeris dependency in tests."""
        with patch("ephemeris_mcp.server.calculate_chart") as mock:
            mock.return_value = {
                "timestamp": "2025-12-16T15:28:00+00:00",
                "location": {"latitude": 42.3314, "longitude": -83.0458},
                "bodies": {
                    "Sun": {
                        "longitude": 289.5,
                        "sign": "Capricorn",
                        "degrees": 19.5,
                        "declination": -22.1,
                        "motion": "direct",
                        "speed": 1.0,
                    },
                    "Moon": {
                        "longitude": 45.2,
                        "sign": "Taurus",
                        "degrees": 15.2,
                        "declination": 5.3,
                        "motion": "direct",
                        "speed": 13.2,
                    },
                },
                "angles": {
                    "Ascendant": {"longitude": 120.0, "sign": "Leo", "degrees": 0.0},
                    "Midheaven": {"longitude": 30.0, "sign": "Aries", "degrees": 0.0},
                },
            }
            yield mock

    def test_tool_registration(self):
        """Verify the tool is registered in the server."""
        from ephemeris_mcp.server import get_planetary_positions

        # Check that the function exists and is callable
        assert callable(get_planetary_positions)
        assert get_planetary_positions.__name__ == "get_planetary_positions"

    def test_successful_calculation_with_defaults(self, mock_calculate_chart):
        """Test successful planetary position calculation with default parameters."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00")

        # Verify calculate_chart was called with correct parameters
        mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=42.3314, lon=-83.0458)

        # Verify result structure
        assert isinstance(result, dict)
        assert "timestamp" in result
        assert "location" in result
        assert "bodies" in result
        assert "angles" in result

    def test_successful_calculation_with_custom_location(self, mock_calculate_chart):
        """Test calculation with custom latitude and longitude."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=51.5, longitude=-0.1)

        mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=51.5, lon=-0.1)

        assert result["location"]["latitude"] == 42.3314  # From mock
        assert result["location"]["longitude"] == -83.0458  # From mock

    def test_valid_iso_timestamp_formats(self, mock_calculate_chart):
        """Test various valid ISO-8601 timestamp formats."""
        from ephemeris_mcp.server import get_planetary_positions

        valid_timestamps = [
            "2025-12-16T15:28:00",
            "2025-12-16T15:28:00Z",
            "2025-12-16T15:28:00+00:00",
            "2025-12-16T15:28:00.000Z",
            "2025-12-31T23:59:59",
        ]

        for timestamp in valid_timestamps:
            mock_calculate_chart.reset_mock()
            result = get_planetary_positions(iso_time=timestamp)
            assert result is not None
            mock_calculate_chart.assert_called_once()

    def test_latitude_boundary_values(self, mock_calculate_chart):
        """Test latitude boundary values (-90 to 90)."""
        from ephemeris_mcp.server import get_planetary_positions

        boundary_latitudes = [-90.0, -45.0, 0.0, 45.0, 90.0]

        for lat in boundary_latitudes:
            mock_calculate_chart.reset_mock()
            result = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=lat, longitude=0.0)
            assert result is not None
            mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=lat, lon=0.0)

    def test_longitude_boundary_values(self, mock_calculate_chart):
        """Test longitude boundary values (-180 to 180)."""
        from ephemeris_mcp.server import get_planetary_positions

        boundary_longitudes = [-180.0, -90.0, 0.0, 90.0, 180.0]

        for lon in boundary_longitudes:
            mock_calculate_chart.reset_mock()
            result = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=0.0, longitude=lon)
            assert result is not None
            mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=0.0, lon=lon)

    def test_result_contains_all_expected_bodies(self, mock_calculate_chart):
        """Verify result includes Sun and Moon at minimum."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00")

        assert "Sun" in result["bodies"]
        assert "Moon" in result["bodies"]

        # Verify body structure
        for body_name, body_data in result["bodies"].items():
            assert "longitude" in body_data
            assert "sign" in body_data
            assert "degrees" in body_data
            assert "declination" in body_data
            assert "motion" in body_data
            assert "speed" in body_data

    def test_result_contains_angles(self, mock_calculate_chart):
        """Verify result includes Ascendant and Midheaven."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00")

        assert "Ascendant" in result["angles"]
        assert "Midheaven" in result["angles"]

        # Verify angle structure
        for angle_name, angle_data in result["angles"].items():
            assert "longitude" in angle_data
            assert "sign" in angle_data
            assert "degrees" in angle_data

    def test_error_propagation_from_engine(self):
        """Test that errors from the engine are properly propagated."""
        from ephemeris_mcp.server import get_planetary_positions

        with patch("ephemeris_mcp.server.calculate_chart") as mock:
            mock.side_effect = ValueError("Invalid timestamp format")

            with pytest.raises(ValueError, match="Invalid timestamp format"):
                get_planetary_positions(iso_time="invalid-timestamp")

    def test_result_is_json_serializable(self, mock_calculate_chart):
        """Verify the result can be serialized to JSON (important for MCP protocol)."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00")

        # Should not raise exception
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized == result

    def test_timestamp_in_past(self, mock_calculate_chart):
        """Test calculation for historical dates."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2000-01-01T00:00:00")

        mock_calculate_chart.assert_called_once_with(iso_date="2000-01-01T00:00:00", lat=42.3314, lon=-83.0458)
        assert result is not None

    def test_timestamp_in_future(self, mock_calculate_chart):
        """Test calculation for future dates."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2050-12-31T23:59:59")

        mock_calculate_chart.assert_called_once_with(iso_date="2050-12-31T23:59:59", lat=42.3314, lon=-83.0458)
        assert result is not None

    def test_location_precision(self, mock_calculate_chart):
        """Test that location coordinates are passed with precision."""
        from ephemeris_mcp.server import get_planetary_positions

        get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=43.123456, longitude=-84.987654)

        mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=43.123456, lon=-84.987654)

    def test_negative_coordinates(self, mock_calculate_chart):
        """Test with negative latitude and longitude (Southern/Western hemispheres)."""
        from ephemeris_mcp.server import get_planetary_positions

        result = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=-33.9, longitude=-151.2)

        mock_calculate_chart.assert_called_once_with(iso_date="2025-12-16T15:28:00", lat=-33.9, lon=-151.2)
        assert result is not None


class TestServerModule:
    """Test suite for server module-level functionality."""

    def test_mcp_server_instance_exists(self):
        """Verify the FastMCP server instance is created."""
        from ephemeris_mcp.server import mcp

        assert mcp is not None
        # Verify mcp has the correct type
        assert type(mcp).__name__ == "FastMCP"

    def test_server_has_correct_name(self):
        """Verify the MCP server has the correct name."""
        from ephemeris_mcp.server import mcp

        # FastMCP server should have a name attribute
        assert hasattr(mcp, "name")
        assert mcp.name == "EphemerisMCP"

    def test_tool_function_exists(self):
        """Verify the tool function is exported from the module."""
        from ephemeris_mcp.server import get_planetary_positions

        assert callable(get_planetary_positions)
        assert get_planetary_positions.__doc__ is not None

    def test_module_imports(self):
        """Verify all required imports are available."""
        import ephemeris_mcp.server as server_module

        # Check that engine is imported
        assert hasattr(server_module, "calculate_chart")

        # Check that FastMCP is available
        assert hasattr(server_module, "FastMCP")

        # Check that the function is exported
        assert hasattr(server_module, "get_planetary_positions")


class TestServerIntegration:
    """Integration tests with the actual engine (not mocked)."""

    def test_real_calculation_integration(self):
        """Test actual calculation with real engine (integration test)."""
        from ephemeris_mcp.server import get_planetary_positions

        # This test uses the real calculate_chart function
        result = get_planetary_positions(iso_time="2025-12-16T15:28:00")

        # Verify structure
        assert isinstance(result, dict)
        assert "meta" in result
        assert "bodies" in result

        # Verify meta data
        assert result["meta"]["timestamp"] == "2025-12-16T15:28:00"
        assert result["meta"]["lat"] == 42.3314
        assert result["meta"]["lon"] == -83.0458

        # Verify bodies have numeric positions
        for body_name, body_data in result["bodies"].items():
            assert isinstance(body_data["longitude"], (int, float))
            assert 0 <= body_data["longitude"] < 360

    def test_different_locations_produce_different_angles(self):
        """Verify that different geographic locations produce different house cusps."""
        from ephemeris_mcp.server import get_planetary_positions

        result1 = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=42.3314, longitude=-83.0458)

        result2 = get_planetary_positions(iso_time="2025-12-16T15:28:00", latitude=51.5, longitude=-0.1)

        # Planetary positions should be the same (geocentric)
        assert result1["bodies"]["Sun"]["longitude"] == result2["bodies"]["Sun"]["longitude"]

        # But angles should differ (location-dependent)
        assert result1["bodies"]["Ascendant"]["longitude"] != result2["bodies"]["Ascendant"]["longitude"]

    def test_main_function_exists(self):
        """Test that main() function is callable and properly configured."""
        from ephemeris_mcp.server import main

        # Verify main exists and is callable
        assert callable(main)

        # Verify the function signature
        import inspect

        sig = inspect.signature(main)
        assert len(sig.parameters) == 0  # main() takes no arguments

    def test_mcp_server_run_configuration(self):
        """Test that the MCP server is properly configured for running."""
        from unittest.mock import patch

        from ephemeris_mcp.server import mcp

        # Verify mcp has a run method
        assert hasattr(mcp, "run")
        assert callable(mcp.run)

        # Test that main would call mcp.run (we mock it to prevent actual execution)
        with patch.object(mcp, "run") as mock_run:
            from ephemeris_mcp.server import main

            # This won't actually run the server due to our mock
            try:
                main()
            except SystemExit:
                pass  # main() might call sys.exit, which is fine

            # Verify run was called
            mock_run.assert_called_once()
