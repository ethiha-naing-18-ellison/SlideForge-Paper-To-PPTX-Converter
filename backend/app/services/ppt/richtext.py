# backend/app/services/ppt/richtext.py
from __future__ import annotations
import re
from typing import List, Tuple

# Supports **bold**, *italic*, __underline__
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"\*(.+?)\*")
UNDER = re.compile(r"__(.+?)__")

# Process in a single pass by replacing with tokens then splitting
TOKENS = [
    ("B", BOLD),
    ("I", ITAL),
    ("U", UNDER),
]

def tokenize_inline(text: str) -> List[Tuple[str, dict]]:
    """
    Convert a string with simple markup into a list of (segment, style_dict).
    style_dict: {"bold": bool, "italic": bool, "underline": bool}
    """
    if not text:
        return [("", {"bold": False, "italic": False, "underline": False})]

    # Replace with non-overlapping tokens
    # We'll scan from left to right; nested styles are applied in encounter order.
    segments: List[Tuple[str, dict]] = []
    i = 0
    current = {"bold": False, "italic": False, "underline": False}
    buf = ""

    def flush():
        nonlocal buf
        if buf:
            segments.append((buf, current.copy()))
            buf = ""

    # Build a combined regex
    combined = re.compile(r"\*\*.+?\*\*|\*.+?\*|__.+?__")
    for m in combined.finditer(text):
        start, end = m.span()
        inner = text[start:end]
        # pre-text
        if start > i:
            buf += text[i:start]
            flush()
        # style token
        if inner.startswith("**") and inner.endswith("**"):
            segments.append((inner[2:-2], {"bold": True, "italic": False, "underline": False}))
        elif inner.startswith("*") and inner.endswith("*"):
            segments.append((inner[1:-1], {"bold": False, "italic": True, "underline": False}))
        elif inner.startswith("__") and inner.endswith("__"):
            segments.append((inner[2:-2], {"bold": False, "italic": False, "underline": True}))
        i = end

    # tail
    if i < len(text):
        buf += text[i:]
    flush()

    return segments
