# See AGENTS.md for project context and conventions

"""Logging configuration for EphemerisMCP.

This module provides structured logging setup using structlog:
- JSON-serializable structured events
- Context binding and processors
- Integration with stdlib logging for compatibility
"""

import logging
import sys

import structlog


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application-wide logging with structlog.

    Args:
        level: Logging level (default: INFO)
    """
    # Configure structlog processors
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.dev.ConsoleRenderer(),  # Human-readable for development
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging for compatibility
    logging.basicConfig(
        format="%(message)s",
        level=level,
        stream=sys.stderr,
    )
