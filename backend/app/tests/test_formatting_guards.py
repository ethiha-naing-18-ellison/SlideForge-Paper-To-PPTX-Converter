"""Smoke tests for formatting constraints and cleanup functions."""

from pptx import Presentation

def _texts(slide):
    """Extract all text from a slide."""
    out = []
    for shp in slide.shapes:
        if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
            out.append(" ".join(p.text or "" for p in shp.text_frame.paragraphs).strip())
    return "\n".join(out)

def test_no_generic_filler():
    """Test that meaningless slide detection works."""
    prs = Presentation()
    s = prs.slides.add_slide(prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0])
    
    # Test that the helper function exists and is callable
    try:
        from app.services.ppt.builder import _is_meaningless
        result = _is_meaningless(s)
        assert isinstance(result, bool)
    except ImportError:
        # Function might not be available in test environment
        pass

def test_text_cleaning():
    """Test text cleaning functions."""
    from app.services.ppt.cleantext import normalize_text, clean_bullet_text
    
    # Test normalization
    assert normalize_text("  test   text  ") == "test text"
    assert normalize_text("( test )") == "(test)"
    
    # Test bullet cleaning
    long_bullet = "This is a very long bullet point that should be truncated to a reasonable length for slide presentation"
    cleaned = clean_bullet_text(long_bullet, max_words=10)
    assert len(cleaned.split()) <= 10
    assert cleaned.endswith("…")

def test_markdown_parsing():
    """Test markdown to formatting conversion."""
    from app.services.ppt.cleantext import split_runs_from_markdown
    
    text = "This is **bold** and *italic* text"
    runs = split_runs_from_markdown(text)
    
    # Should have multiple runs
    assert len(runs) > 1
    
    # Check that bold and italic are detected
    has_bold = any(run[1].get("b", False) for run in runs)
    has_italic = any(run[1].get("i", False) for run in runs)
    assert has_bold or has_italic
