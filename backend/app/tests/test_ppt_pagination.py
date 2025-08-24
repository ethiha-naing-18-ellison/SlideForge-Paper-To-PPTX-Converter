import os
import pytest
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches

# Add the app directory to the path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.services.ppt.builder import add_section_with_bullets_paginated, init_presentation
from app.models.schema import LayoutConfig, SummarizedSection, SectionName

EMU_PER_INCH = 914400

def test_paginate_bullets_no_overflow(tmp_path):
    """Test that pagination prevents slide overflow."""
    prs, layout = init_presentation(LayoutConfig())
    theme_layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]

    # Create very long bullets that would definitely overflow
    bullets = [
        "This is a very long bullet that should be wrapped properly and never overflow the slide even when it contains a lot of descriptive text about the method and results that are important for the audience to understand.",
        "Another extremely long bullet point that describes complex methodologies and experimental procedures in great detail to ensure comprehensive understanding of the research approach and its implications for the field.",
        "A third bullet that continues with even more detailed explanations about statistical analysis methods, data processing techniques, and validation procedures that were employed during the course of this comprehensive research study."
    ] * 5  # Repeat to create many bullets

    slides = add_section_with_bullets_paginated(prs, theme_layout, layout, "Methods", bullets)
    assert len(slides) >= 2  # Should create multiple slides

    # invariant: all shapes must be within bounds (top+height <= usable bottom)
    usable_bottom = Inches(layout.slide_height_in - layout.margin_bottom_in)
    for s in slides:
        for shp in s.shapes:
            if not hasattr(shp, "top") or not hasattr(shp, "height"):
                continue
            # Check that shape doesn't overflow (with small tolerance for rounding)
            assert shp.top + shp.height <= usable_bottom + 1000  # 1000 EMU tolerance

    out = tmp_path / "out.pptx"
    prs.save(str(out))
    assert out.exists() and out.stat().st_size > 0

def test_paginator_functions():
    """Test individual paginator functions."""
    from app.services.ppt.paginator import estimate_lines, paragraph_height_in, total_bullets_height_in
    
    # Test line estimation
    text = "This is a test sentence that should be wrapped"
    lines = estimate_lines(text, box_width_in=5.0, font_pt=16)
    assert lines >= 1
    
    # Test paragraph height calculation
    height = paragraph_height_in(3, font_pt=16, line_spacing=1.15)
    assert height > 0
    
    # Test total bullets height
    bullets = ["Short bullet", "Longer bullet with more words", "Very long bullet with many words that should wrap to multiple lines"]
    total_height = total_bullets_height_in(bullets, box_width_in=5.0, font_pt=16, line_spacing=1.15)
    assert total_height > 0

def test_layout_config():
    """Test layout configuration."""
    layout = LayoutConfig()
    assert layout.slide_width_in == 13.333
    assert layout.slide_height_in == 7.5
    assert layout.bullet_font_max_pt == 20
    assert layout.bullet_font_min_pt == 16

def test_usable_box_calculation():
    """Test usable box calculation."""
    from app.services.ppt.builder import _usable_box
    
    layout = LayoutConfig()
    left, top, width, height = _usable_box(layout)
    
    # Check that usable box is smaller than slide
    assert width < layout.slide_width_in
    assert height < layout.slide_height_in
    
    # Check that margins are respected
    assert left == layout.margin_left_in
    assert top == layout.margin_top_in + layout.title_height_in

def test_section_pagination_integration():
    """Test integration with SummarizedSection."""
    prs, layout = init_presentation(LayoutConfig())
    theme_layout = prs.slide_layouts[1]
    
    # Create a section with many bullets
    section = SummarizedSection(
        name=SectionName.METHODS,
        bullets=[
            "First bullet point with some content",
            "Second bullet point that is longer and contains more detailed information about the methodology",
            "Third bullet point that continues with even more detailed explanations about the experimental setup and procedures",
            "Fourth bullet point describing the data collection process and analysis techniques",
            "Fifth bullet point about validation methods and quality control measures",
            "Sixth bullet point covering statistical analysis and significance testing",
            "Seventh bullet point about result interpretation and discussion of findings"
        ]
    )
    
    slides = add_section_with_bullets_paginated(
        prs, theme_layout, layout, section.name.value.replace("_", " ").title(), section.bullets
    )
    
    assert len(slides) >= 1
    assert all(hasattr(slide, 'shapes') for slide in slides)
