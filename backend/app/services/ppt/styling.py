# backend/app/services/ppt/styling.py
from __future__ import annotations
import re
from typing import Iterable, Tuple
from pptx.dml.color import RGBColor

def hex_to_rgb(hex_color: str) -> RGBColor:
    hc = hex_color.lstrip("#")
    return RGBColor(int(hc[0:2], 16), int(hc[2:4], 16), int(hc[4:6], 16))

def split_by_keywords(text: str, keywords: Iterable[str]) -> list[Tuple[str, bool]]:
    """
    Returns [(segment, is_key)], highlighting any keyword occurrences (case-insensitive).
    """
    if not keywords:
        return [(text, False)]
    # Build regex that preserves words; prioritize longest keywords
    kws = sorted([k.strip() for k in keywords if k.strip()], key=len, reverse=True)
    if not kws:
        return [(text, False)]
    pat = re.compile(r"(" + "|".join(re.escape(k) for k in kws) + r")", re.IGNORECASE)
    out: list[Tuple[str, bool]] = []
    last = 0
    for m in pat.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], False))
        out.append((text[m.start():m.end()], True))
        last = m.end()
    if last < len(text):
        out.append((text[last:], False))
    return out
