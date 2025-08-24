"""PowerPoint generation services for SlideForge backend."""

from .builder import build_presentation
from .expander import expand_to_target_slides

__all__ = ["build_presentation", "expand_to_target_slides"]
