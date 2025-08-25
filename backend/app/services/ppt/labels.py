# backend/app/services/ppt/labels.py
import re
from typing import List

LABEL_PREFIX = re.compile(r"^(title|keywords?|key\s*terms?|abstract|summary)\s*:\s*", re.I)
NUM_HEAD = re.compile(r"^\s*\d+(\.\d+)*\.\s*([A-Z].+)$")   # "1." "1.1." headings

def strip_label_prefix(line: str) -> str:
    """Strip label prefixes like 'Title:', 'Keywords:', '1. INTRODUCTION' etc."""
    if not line:
        return ""
    
    # Remove label prefixes
    line = LABEL_PREFIX.sub("", line).strip()
    
    # Remove numbered headings like "1. INTRODUCTION" -> "INTRODUCTION"
    m = NUM_HEAD.match(line)
    if m:
        return m.group(2).strip()
    
    return line

def clean_section_text(text: str) -> str:
    """Clean section text by removing common artifacts."""
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned = strip_label_prefix(line.strip())
        if cleaned and cleaned.lower() not in {"report", "other", "untitled"}:
            cleaned_lines.append(cleaned)
    
    return '\n'.join(cleaned_lines)
