from __future__ import annotations
import re
from typing import Dict, List, Tuple

# Use the improved canonicalization from sections.py
from ..services.ppt.sections import canonicalize

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

def split_to_sections(raw_text: str) -> Dict[str, str]:
    """Heuristic split by headings: lines in ALL CAPS / Title Case, colon lines, etc."""
    lines = raw_text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = "OTHER"
    buf: List[str] = []
    def flush():
        nonlocal buf, current
        if buf:
            sections[current] = sections.get(current,"") + "\n".join(buf).strip()+"\n"
            buf = []
    
    for ln in lines:
        # Enhanced heading detection patterns
        ln_stripped = ln.strip()
        
        # Pattern 1: Numbered sections like "1. INTRODUCTION", "2. LITERATURE REVIEW"
        if re.match(r"^\d+\.\s*[A-Z][A-Z\s&]+$", ln_stripped):
            flush()
            current = canonicalize(ln_stripped)
            continue
            
        # Pattern 2: Numbered sections with dots like "1.1. Background"
        if re.match(r"^\d+\.\d+\.\s*[A-Z][A-Za-z\s&]+$", ln_stripped):
            flush()
            current = canonicalize(ln_stripped)
            continue
            
        # Pattern 3: ALL CAPS sections
        if re.match(r"^\s*[A-Z][A-Z \-/&\d]{3,}\s*$", ln_stripped):
            flush()
            current = canonicalize(ln_stripped)
            continue
            
        # Pattern 4: Title Case sections ending with colon
        if re.match(r"^\s*[A-Z][A-Za-z \-/&\d]{3,}\s*:$", ln_stripped):
            flush()
            current = canonicalize(ln_stripped)
            continue
            
        # Pattern 5: Abstract detection
        if ln_stripped.upper().startswith("ABSTRACT"):
            flush()
            current = canonicalize(ln_stripped)
            continue
            
        # Pattern 6: References/Bibliography
        if ln_stripped.upper().startswith("REFERENCES") or ln_stripped.upper().startswith("BIBLIOGRAPHY"):
            flush()
            current = canonicalize(ln_stripped)
            continue
        
        buf.append(ln)
    flush()
    return sections

def sentences(text: str) -> List[str]:
    parts = SENT_SPLIT.split(re.sub(r"\s+", " ", text.strip()))
    return [p.strip() for p in parts if p.strip()]
