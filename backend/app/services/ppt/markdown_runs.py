# backend/app/services/ppt/markdown_runs.py
import re
from typing import List, Tuple

TOK = re.compile(r"\*\*.+?\*\*|__.+?__|\*.+?\*")

def to_runs(text: str) -> List[Tuple[str, dict]]:
    """Convert markdown text to styled runs for PPTX rendering."""
    if not text:
        return []
    
    out, i = [], 0
    
    for m in TOK.finditer(text):
        if m.start() > i:
            out.append((text[i:m.start()], {"b": False, "i": False, "u": False}))
        
        t = m.group(0)
        if t.startswith("**"):
            out.append((t[2:-2], {"b": True, "i": False, "u": False}))
        elif t.startswith("__"):
            out.append((t[2:-2], {"b": False, "i": False, "u": True}))
        else:
            out.append((t[1:-1], {"b": False, "i": True, "u": False}))
        
        i = m.end()
    
    if i < len(text):
        out.append((text[i:], {"b": False, "i": False, "u": False}))
    
    return [(seg.strip(), st) for seg, st in out if seg.strip()]
