"""Footer utilities for adding slide numbers and document titles."""

from __future__ import annotations
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def short_title(t: str, max_chars: int = 40) -> str:
    """Create a short version of the title for footer display."""
    if not t:
        return "SlideForge"
    t = t.strip()
    return (t[:max_chars] + "…") if len(t) > max_chars else t

def add_footer_to_slide(slide, layout, doc_title: str, page_num: int | None = None):
    """Add a footer to a slide with short title and optional page number."""
    from .cleantext import normalize_text
    
    # Clean and normalize the title
    doc_title = normalize_text(doc_title)
    label = short_title(doc_title, 40)
    
    # Right-aligned positioning
    x = layout.slide_width_in - layout.margin_right_in - 4.5
    y = layout.slide_height_in - layout.margin_bottom_in + 0.08
    
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(4.5), Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    
    if page_num is not None:
        p.text = f"{label} · {page_num}"
    else:
        p.text = f"{label}"
    
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(145, 152, 161)
    p.alignment = 2  # Right alignment

def apply_footer_to_all_slides(prs, layout, doc_title: str):
    """Apply footer to all slides in the presentation."""
    for idx, slide in enumerate(prs.slides, start=1):
        try:
            add_footer_to_slide(slide, layout, doc_title, idx)
        except Exception:
            continue  # Skip if footer can't be added to this slide
