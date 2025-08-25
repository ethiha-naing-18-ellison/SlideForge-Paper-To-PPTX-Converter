"""PowerPoint generation services for SlideForge backend."""

try:
    from .builder import build_presentation
    from .expander import expand_to_target_slides
    __all__ = ["build_presentation", "expand_to_target_slides"]
except ImportError:
    # Allow importing other modules even if pptx is not available
    __all__ = []
