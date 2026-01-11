# See AGENTS.md for project context and conventions

import logging

import pytest
import structlog


@pytest.fixture(autouse=True)
def configure_logging():
    """Configure logging for tests to prevent log spam and ensure consistent behavior."""
    # Set up structlog for tests with minimal output
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    # Also configure stdlib logging for compatibility
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )

    yield

    # Cleanup after test
    logging.shutdown()


@pytest.fixture
def enable_debug_logging():
    """Fixture to enable debug logging for specific tests that need it."""
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    logger = structlog.get_logger("ephemeris_mcp")

    yield logger

    # Reset to warning level
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
