"""Core configuration and utilities for SlideForge backend."""

from .config import get_settings
from .logging import get_logger

__all__ = ["get_settings", "get_logger"]
