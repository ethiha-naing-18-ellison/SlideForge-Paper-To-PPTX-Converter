"""Utility functions for SlideForge backend."""

from .fileio import (
    ensure_unique_filename,
    get_file_extension,
    is_pdf_file,
    save_uploaded_file,
)
from .ocr_stub import OCRStub

__all__ = [
    "ensure_unique_filename",
    "get_file_extension", 
    "is_pdf_file",
    "save_uploaded_file",
    "OCRStub",
]
