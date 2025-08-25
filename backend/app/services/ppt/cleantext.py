"""Text cleanup and markdown to formatting conversion utilities."""

from __future__ import annotations
import re
from typing import List, Tuple
from pptx.dml.color import RGBColor
from pptx.util import Pt

MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
MD_ITAL = re.compile(r"\*(.+?)\*")
MD_UNDER = re.compile(r"__(.+?)__")

SPACE_FIXES = [
    (re.compile(r"\s+([,.;:!?])"), r"\1"),         # no space before punctuation
    (re.compile(r"\(\s+"), "("),                   # no space after opening paren
    (re.compile(r"\s+\)"), ")"),                   # no space before closing paren
    (re.compile(r"\s{2,}"), " "),                  # collapse multiple spaces
    (re.compile(r"…{2,}"), "…"),                   # ellipsis
]

# Additional hygiene patterns
RE_WEIRD_UNI = re.compile(r"[\u200b-\u200f\u202a-\u202e]")  # zero-widths, bidi

GENERIC_TITLES = {"untitled","research paper","document","title","paper","new document"}

def normalize_text(s: str) -> str:
    """Clean up common text formatting issues."""
    if not s:
        return ""
    s = s.strip()
    
    # Remove weird Unicode characters
    s = RE_WEIRD_UNI.sub("", s)
    
    # Apply space fixes
    for pat, rep in SPACE_FIXES:
        s = pat.sub(rep, s)
    
    # Tidy dashes and ellipsis
    s = s.replace(" - ", " — ")
    s = s.replace("..", "…").replace("… …", "…")
    
    # Consistent casing for common hyphenations
    s = s.replace("Low-Cost", "Low-cost")
    
    # Remove any remaining raw markdown markers
    s = s.replace("**", "").replace("*", "").replace("__", "")
    
    return s

def is_generic_title(t: str) -> bool:
    """Check if a title is generic/placeholder."""
    if not t:
        return True
    return t.strip().lower() in GENERIC_TITLES or len(t.strip()) <= 8

def split_runs_from_markdown(text: str) -> List[Tuple[str, dict]]:
    """
    Convert **bold**, *italic*, __underline__ into styled run descriptors.
    Returns list of (text, style_dict) tuples.
    """
    if not text:
        return []
    
    # Find all markdown tokens
    combined = re.compile(r"\*\*.+?\*\*|__.+?__|\*.+?\*")
    runs: List[Tuple[str, dict]] = []
    i = 0
    
    for m in combined.finditer(text):
        start, end = m.span()
        if start > i:
            runs.append((text[i:start], {"b":False,"i":False,"u":False}))
        
        token = text[start:end]
        if token.startswith("**"):
            runs.append((token[2:-2], {"b":True,"i":False,"u":False}))
        elif token.startswith("__"):
            runs.append((token[2:-2], {"b":False,"i":False,"u":True}))
        else:
            runs.append((token[1:-1], {"b":False,"i":True,"u":False}))
        i = end
    
    if i < len(text):
        runs.append((text[i:], {"b":False,"i":False,"u":False}))
    
    return [(normalize_text(t), st) for t,st in runs if normalize_text(t)]

def clean_bullet_text(text: str, max_words: int = 18) -> str:
    """Clean and truncate bullet text to reasonable length."""
    if not text:
        return ""
    
    # Remove key terms inline (they'll be shown in callout box)
    if " — Key terms:" in text:
        text = text.split(" — Key terms:")[0]
    
    # Normalize spacing (but preserve markdown for formatting)
    cleaned = normalize_text(text)
    
    # Split long sentences by semicolons or commas into multiple bullets
    if len(cleaned.split()) > max_words and (";" in cleaned or "," in cleaned):
        # Try to split by semicolons first, then commas
        if ";" in cleaned:
            parts = [p.strip() for p in cleaned.split(";") if p.strip()]
        else:
            parts = [p.strip() for p in cleaned.split(",") if p.strip()]
        
        # Return the first part if it's reasonable length, otherwise truncate
        if parts and len(parts[0].split()) <= max_words:
            return parts[0]
    
    # Truncate if too long (preserve markdown)
    words = cleaned.split()
    if len(words) > max_words:
        # Find the last complete markdown token before max_words
        truncated = " ".join(words[:max_words-1])
        # Add ellipsis if we truncated
        if len(words) > max_words:
            truncated += "…"
        return truncated
    
    return cleaned

def remove_raw_markdown(text: str) -> str:
    """Remove raw markdown markers from text."""
    if not text:
        return ""
    
    # Remove markdown markers
    text = text.replace("**", "").replace("*", "").replace("__", "")
    
    # Clean up extra spaces
    text = " ".join(text.split())
    
    return text.strip()
