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
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
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
