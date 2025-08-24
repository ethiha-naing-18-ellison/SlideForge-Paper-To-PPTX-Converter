# backend/app/services/ppt/cleanup.py
from __future__ import annotations

def remove_unused_placeholders(slide) -> int:
    """
    Remove empty/default placeholders (e.g., 'Click to add text/title') from a slide.
    Returns number of shapes removed.
    """
    removed = 0
    # Collect first (can't mutate while iterating directly)
    to_remove = []
    for shp in slide.shapes:
        try:
            if not getattr(shp, "is_placeholder", False):
                continue
            # If it has text, check whether it's effectively empty/default UI text
            if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
                txt = "".join(p.text or "" for p in shp.text_frame.paragraphs).strip().lower()
                if txt == "" or txt.startswith("click to add"):
                    to_remove.append(shp)
            else:
                # Non-text placeholder not used -> remove
                to_remove.append(shp)
        except Exception:
            # If anything odd, skip rather than breaking generation
            continue

    for shp in to_remove:
        try:
            el = shp._element  # python-pptx private element accessor
            el.getparent().remove(el)
            removed += 1
        except Exception:
            continue
    return removed
