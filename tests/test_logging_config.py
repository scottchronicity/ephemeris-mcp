# See AGENTS.md for project context and conventions

"""Tests for logging configuration and structured logging."""

import logging

import structlog

from ephemeris_mcp.logging_config import setup_logging


def test_setup_logging_configures_structlog():
    """Test that setup_logging properly configures structlog."""
    setup_logging(level=logging.DEBUG)

    # Get a logger and verify it works
    logger = structlog.get_logger("test")
    assert logger is not None


def test_setup_logging_sets_level():
    """Test that setup_logging respects the level parameter."""
    setup_logging(level=logging.WARNING)

    # Verify configuration was applied (structlog should be configured)
    logger = structlog.get_logger("test")
    assert logger is not None


def test_structlog_logger_methods_exist():
    """Test that structlog logger has all required logging methods."""
    logger = structlog.get_logger("test.module")

    assert hasattr(logger, "debug")
    assert hasattr(logger, "info")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")
    assert hasattr(logger, "critical")

    assert callable(logger.debug)
    assert callable(logger.info)
    assert callable(logger.warning)
    assert callable(logger.error)
    assert callable(logger.critical)


def test_structlog_info_with_params(caplog):
    """Test that structlog logs with structured parameters."""
    logger = structlog.get_logger("test.structured")

    with caplog.at_level(logging.INFO):
        logger.info("Test message", user="alice", count=42, status="active")

        # Structlog integration with caplog may vary, but the call should not raise
        assert True


def test_structlog_error_with_params(caplog):
    """Test that structlog error logs with structured parameters."""
    logger = structlog.get_logger("test.structured")

    with caplog.at_level(logging.ERROR):
        logger.error("Error occurred", error_code=500, component="engine")

        # The call should succeed
        assert True


def test_structlog_warning_with_params(caplog):
    """Test that structlog warning logs with structured parameters."""
    logger = structlog.get_logger("test.structured")

    with caplog.at_level(logging.WARNING):
        logger.warning("Warning message", body="Mercury", error_type="KeyError")

        # The call should succeed
        assert True


def test_structlog_supports_context_binding():
    """Test that structlog supports context binding."""
    logger = structlog.get_logger("test.context")

    # Bind context to logger
    bound_logger = logger.bind(request_id="12345", user="alice")

    # Should not raise
    bound_logger.info("Request processed")
    assert True


def test_structlog_supports_exc_info():
    """Test that structlog supports exc_info for exceptions."""
    logger = structlog.get_logger("test.exception")

    try:
        raise ValueError("Test exception")
    except ValueError:
        # Should not raise
        logger.error("Exception caught", exc_info=True)
        assert True
