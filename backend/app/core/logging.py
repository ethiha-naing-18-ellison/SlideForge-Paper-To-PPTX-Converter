"""Structured logging configuration for SlideForge backend."""

from __future__ import annotations

import sys
from typing import Any, Dict

import structlog
from structlog.types import Processor

from .config import get_settings


def configure_logging() -> None:
    """Configure structured logging."""
    settings = get_settings()
    
    # Configure structlog
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def log_event(
    logger: structlog.stdlib.BoundLogger,
    event: str,
    **kwargs: Any
) -> None:
    """Log an event with structured data."""
    logger.info(event, **kwargs)


def log_error(
    logger: structlog.stdlib.BoundLogger,
    event: str,
    error: Exception,
    **kwargs: Any
) -> None:
    """Log an error with structured data."""
    logger.error(
        event,
        error_type=type(error).__name__,
        error_message=str(error),
        **kwargs
    )


def log_performance(
    logger: structlog.stdlib.BoundLogger,
    operation: str,
    duration_ms: float,
    **kwargs: Any
) -> None:
    """Log performance metrics."""
    logger.info(
        "operation_completed",
        operation=operation,
        duration_ms=duration_ms,
        **kwargs
    )
