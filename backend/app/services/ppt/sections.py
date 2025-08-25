# backend/app/services/ppt/sections.py
import re
from typing import Dict, Tuple

CANON_MAP = {
    "INTRODUCTION": ("INTRODUCTION", "BACKGROUND", "OVERVIEW", "MOTIVATION"),
    "METHODS": ("METHOD", "METHODS", "METHODOLOGY", "PROCEDURE", "EXPERIMENTS", "MATERIALS AND METHODS"),
    "RESULTS": ("RESULT", "RESULTS", "FINDINGS", "EVALUATION"),
    "DISCUSSION": ("DISCUSSION", "ANALYSIS", "INSIGHTS"),
    "LIMITATIONS": ("LIMITATION", "LIMITATIONS", "THREATS TO VALIDITY"),
    "CONCLUSION": ("CONCLUSION", "CONCLUSIONS", "CLOSING REMARKS"),
}

def canonicalize(name: str) -> str:
    """Convert any section name to its canonical form."""
    n = (name or "").upper().strip()
    
    # Remove problematic prefixes first
    n = n.replace("OTHER — ", "").replace("ADDITIONAL INFORMATION — ", "")
    
    # Remove numbered prefixes like "1.", "1.1.", "2.", etc.
    n = re.sub(r"^\d+\.\d*\.?\s*", "", n)
    
    for canon_name, variants in CANON_MAP.items():
        if any(v in n for v in variants):
            return canon_name
    
    # Handle special cases
    if "ABSTRACT" in n or "SUMMARY" in n:
        return "INTRODUCTION"
    
    # Handle REFERENCES/BIBLIOGRAPHY
    if "REFERENCES" in n or "BIBLIOGRAPHY" in n:
        return "OTHER"
    
    # Try to extract meaningful section name from the original text
    # Remove common prefixes and clean up
    cleaned = n.replace("TITLE", "").replace("KEYWORDS", "").replace("ABSTRACT", "").strip()
    if cleaned and len(cleaned) > 3:
        # If we have meaningful content after cleaning, try to map it
        for canon_name, variants in CANON_MAP.items():
            if any(v in cleaned for v in variants):
                return canon_name
    
    return "OTHER"

def cont_title(base: str, idx: int) -> str:
    """Generate continuation title with (cont.) for multi-slide sections."""
    if idx == 0:
        return base
    return f"{base} (cont.)"

def get_section_display_name(canon_name: str) -> str:
    """Get the proper display name for a canonical section."""
    display_names = {
        "INTRODUCTION": "Introduction",
        "METHODS": "Methods",
        "RESULTS": "Results", 
        "DISCUSSION": "Discussion",
        "LIMITATIONS": "Limitations",
        "CONCLUSION": "Conclusion",
        "OTHER": "Additional Information"
    }
    return display_names.get(canon_name, canon_name.title())

def clean_section_title(title: str) -> str:
    """Clean section titles by removing problematic prefixes and formatting."""
    if not title:
        return ""
    
    # Remove problematic prefixes
    title = title.replace("Other — ", "").replace("Additional Information — ", "")
    
    # If the title is just "Additional Information", try to extract meaningful content
    if title.strip() == "Additional Information":
        # This might be a section that should have a more specific name
        return "Overview"
    
    # Remove raw markdown
    title = title.replace("**", "").replace("*", "").replace("__", "")
    
    # Clean up extra spaces
    title = " ".join(title.split())
    
    return title.strip()
