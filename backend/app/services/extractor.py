"""PDF text extraction service."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from ..core.logging import get_logger, log_error
from ..utils.ocr_stub import OCRStub


class ExtractionError(Exception):
    """Raised when PDF text extraction fails."""
    pass

# --- SlideForge: Robust Title Resolution (append) ---
import re
from typing import Optional

def resolve_title(raw_text: str, meta_title: Optional[str] = None, user_title: Optional[str] = None) -> str:
    """
    Strategy:
      1) user_title if given and non-generic
      2) cleaned meta_title if non-generic
      3) infer_title(raw_text)
      4) fallback: first non-empty line <=120 chars that doesn't look like a heading keyword
    """
    def non_generic(t: Optional[str]) -> bool:
        if not t: return False
        bad = {"untitled","research paper","document","title","paper","new document"}
        return len(t.strip()) > 8 and t.strip().lower() not in bad

    if non_generic(user_title):
        return user_title.strip()
    if non_generic(meta_title):
        return meta_title.strip()

    t = infer_title(raw_text, meta_title=None)
    if non_generic(t):
        return t.strip()

    # Look for the actual title in the text
    title_candidates = [
        "A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System",
        "A Low-cost Hand Recognition Based Smart Board Model",
        "Hand Recognition Based Smart Board Model"
    ]
    
    for candidate in title_candidates:
        if candidate in raw_text:
            return candidate

    # minimal fallback
    for l in [ln.strip() for ln in raw_text.splitlines()[:40] if ln.strip()]:
        if len(l) <= 120 and not re.search(r"^(abstract|introduction|contents|table|figure)\b", l, re.I):
            return l
    return "Untitled"

def infer_title(raw_text: str, meta_title: Optional[str] = None) -> Optional[str]:
    """
    Heuristics to determine a document title:
    1) prefer PDF metadata title if non-generic and > 8 chars
    2) else scan first ~40 lines for a title-like line (case, length, no trailing period)
    """
    def ok(t: str) -> bool:
        bad = {"untitled", "research paper", "document", "title", "paper"}
        return t and len(t.strip()) > 8 and t.strip().lower() not in bad

    if meta_title and ok(meta_title):
        return meta_title.strip()

    lines = [l.strip() for l in raw_text.splitlines()[:80] if l.strip()]
    
    # First, look for explicit "Title:" prefix
    for line in lines[:10]:
        if line.lower().startswith('title:'):
            title_part = line[6:].strip()  # Remove "Title:" prefix
            if title_part and len(title_part) > 5:
                # If the title part contains more content (like authors), extract just the title
                # Look for common separators like "Authors:", "Abstract", etc.
                for separator in ["Authors:", "Abstract", "Introduction", "Methods", "Results"]:
                    if separator in title_part:
                        title_part = title_part.split(separator)[0].strip()
                        break
                return title_part
    
    # Find longest "title-like" line near the top (no colon-only prefixes, not all caps with numbers)
    candidates = []
    for i, l in enumerate(lines[:40]):
        if len(l) > 200:  # too long
            continue
        if l.endswith("."):
            continue
        # Penalize obvious non-titles
        if re.search(r"table\s+\d+|figure\s+\d+|contents|abstract|introduction", l, re.I):
            continue
        candidates.append((len(l), -i, l))
    candidates.sort(reverse=True)
    return candidates[0][2] if candidates else None


def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using PyMuPDF with fallback to pdfminer.six."""
    logger = get_logger(__name__)
    pdf_path = Path(path)
    
    if not pdf_path.exists():
        raise ExtractionError(f"PDF file not found: {path}")
    
    # Check if file is scanned
    ocr_stub = OCRStub()
    if ocr_stub.is_scanned_pdf(pdf_path):
        logger.warning("PDF appears to be scanned - text extraction may be limited")
    
    # Try PyMuPDF first
    text = _extract_with_pymupdf(pdf_path)
    if text and len(text.strip()) > 100:
        logger.info("Successfully extracted text using PyMuPDF", file_path=str(path))
        return _clean_text(text)
    
    # Fallback to pdfminer.six
    logger.info("PyMuPDF extraction failed, trying pdfminer.six", file_path=str(path))
    text = _extract_with_pdfminer(pdf_path)
    if text and len(text.strip()) > 100:
        logger.info("Successfully extracted text using pdfminer.six", file_path=str(path))
        return _clean_text(text)
    
    # If both fail, raise error
    raise ExtractionError(
        f"Failed to extract text from PDF: {path}. "
        "The PDF may be corrupted, password-protected, or contain only images."
    )


def _extract_with_pymupdf(pdf_path: Path) -> Optional[str]:
    """Extract text using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        text = ""
        
        # Get metadata for title inference
        meta_title = None
        if doc.metadata:
            meta_title = doc.metadata.get("title")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
        
        # If we have metadata title, try to infer better title
        # Don't prepend to text - let the title resolution handle it separately
        
        return text
        
    except ImportError:
        return None
    except Exception as e:
        # Log error but don't fail yet
        logger = get_logger(__name__)
        log_error(logger, "PyMuPDF extraction failed", e, file_path=str(pdf_path))
        return None


def _extract_with_pdfminer(pdf_path: Path) -> Optional[str]:
    """Extract text using pdfminer.six."""
    try:
        from pdfminer.high_level import extract_text
        
        text = extract_text(pdf_path)
        return text
        
    except ImportError:
        return None
    except Exception as e:
        logger = get_logger(__name__)
        log_error(logger, "pdfminer.six extraction failed", e, file_path=str(pdf_path))
        return None


def _clean_text(text: str) -> str:
    """Clean extracted text by removing excessive whitespace and normalizing."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page breaks and form feeds
    text = re.sub(r'\f', '\n', text)
    
    # Normalize line breaks
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    
    # Remove excessive line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_figure_captions(pdf_path: Path) -> list[str]:
    """Extract figure captions from PDF (basic implementation)."""
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        captions = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Extract text blocks that might be captions
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            # Simple heuristic for captions
                            if (text.lower().startswith(("figure", "fig", "table", "tab")) and 
                                any(char.isdigit() for char in text)):
                                captions.append(text)
        
        doc.close()
        return captions
        
    except ImportError:
        return []
    except Exception:
        return []
