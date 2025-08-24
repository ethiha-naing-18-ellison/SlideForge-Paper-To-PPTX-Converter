"""OCR stub for future OCR functionality."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class OCRStub:
    """Stub class for OCR functionality."""
    
    def __init__(self) -> None:
        """Initialize OCR stub."""
        self.available = False
        self._check_availability()
    
    def _check_availability(self) -> None:
        """Check if OCR is available."""
        try:
            # Future: Check for Tesseract installation
            # import pytesseract
            # pytesseract.get_tesseract_version()
            self.available = False
        except ImportError:
            self.available = False
    
    def extract_text_from_image(self, image_path: Path) -> Optional[str]:
        """Extract text from image using OCR."""
        if not self.available:
            raise NotImplementedError(
                "OCR functionality not available. "
                "Install Tesseract and pytesseract for OCR support."
            )
        
        # Future implementation
        return None
    
    def is_scanned_pdf(self, pdf_path: Path) -> bool:
        """Check if PDF appears to be scanned (no selectable text)."""
        # This is a heuristic - in practice, you'd need more sophisticated detection
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            text = ""
            
            # Check first few pages for text
            for page_num in range(min(3, len(doc))):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            
            # If very little text, likely scanned
            return len(text.strip()) < 100
            
        except ImportError:
            # PyMuPDF not available, assume not scanned
            return False
        except Exception:
            # Error reading PDF, assume not scanned
            return False
