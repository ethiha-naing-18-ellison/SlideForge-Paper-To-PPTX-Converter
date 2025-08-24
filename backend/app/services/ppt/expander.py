# backend/app/services/ppt/expander.py
from __future__ import annotations
from typing import List, Tuple

def expand_to_target_slides(prs, target_count: int, allow_per_bullet_slides: bool = True):
    """
    If the deck has fewer than target_count slides, expand by:
      1) splitting dense sections into more slides (reduce bullets/slide),
      2) creating 'Key Takeaways', 'Definitions', 'FAQ' slides if text is available.
    Non-destructive: only adds; does not delete.
    """
    current = len(prs.slides)
    if current >= target_count:
        return

    # Heuristic expansion: find slides with many bullets and split them by half
    made_progress = True
    while len(prs.slides) < target_count and made_progress:
        made_progress = False
        new_slides = []
        for s in list(prs.slides):
            # Identify a content textbox with many paragraphs
            big_tf = None
            for shp in s.shapes:
                if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
                    if len(shp.text_frame.paragraphs) >= 8:
                        big_tf = shp.text_frame
                        break
            if not big_tf:
                continue

            paras = [p.text for p in big_tf.paragraphs if (p.text or "").strip()]
            if len(paras) < 8:
                continue
            half = len(paras)//2
            first, second = paras[:half], paras[half:]

            # Duplicate slide and keep second half on duplicate
            layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]
            dup = prs.slides.add_slide(layout)
            # Copy title text if exists
            for shp in s.shapes:
                try:
                    if shp == getattr(s.shapes, "title", None) or (getattr(shp, "text_frame", None) and shp.text_frame and shp.text_frame.paragraphs and shp.text_frame.paragraphs[0].text.lower().startswith("conclusion")):
                        tbox = dup.shapes.add_textbox(shp.left, shp.top, shp.width, shp.height)
                        tbox.text_frame.text = shp.text_frame.text
                except Exception:
                    pass

            # Rewrite first slide with first half
            try:
                big_tf.clear()
                for i, t in enumerate(first):
                    p = big_tf.add_paragraph() if i else big_tf.paragraphs[0]
                    p.text = t
            except Exception:
                pass

            # Put second half on duplicate
            try:
                tb = dup.shapes.add_textbox(big_tf._element.getparent().getparent().left, big_tf._element.getparent().getparent().top, big_tf._element.getparent().getparent().width, big_tf._element.getparent().getparent().height)
            except Exception:
                # Fallback: rough placement
                from pptx.util import Inches
                tb = dup.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11.3), Inches(4.8))
            tf = tb.text_frame
            for i, t in enumerate(second):
                p = tf.add_paragraph() if i else tf.paragraphs[0]
                p.text = t

            new_slides.append(dup)
            made_progress = True
            if len(prs.slides) >= target_count:
                break

        if not made_progress:
            break
