"""File I/O utility functions for SlideForge backend."""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from ..core.config import get_settings


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def is_pdf_file(filename: str) -> bool:
    """Check if file is a PDF."""
    return get_file_extension(filename) == ".pdf"


def ensure_unique_filename(base_path: Path, filename: str) -> Path:
    """Ensure filename is unique by adding timestamp if needed."""
    if not base_path.exists():
        return base_path / filename
    
    name = Path(filename).stem
    ext = Path(filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Try original name first
    new_path = base_path / filename
    if not new_path.exists():
        return new_path
    
    # Add timestamp to make unique
    unique_filename = f"{name}_{timestamp}{ext}"
    return base_path / unique_filename


def save_uploaded_file(
    file: UploadFile,
    directory: Optional[str] = None
) -> Path:
    """Save uploaded file to disk with unique filename."""
    settings = get_settings()
    
    if directory is None:
        directory = settings.upload_dir
    
    upload_path = Path(directory)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Ensure unique filename
    unique_path = ensure_unique_filename(upload_path, file.filename or "upload")
    
    # Save file
    with open(unique_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return unique_path


def cleanup_temp_files(file_paths: list[Path]) -> None:
    """Clean up temporary files."""
    for file_path in file_paths:
        try:
            if file_path.exists():
                file_path.unlink()
        except OSError:
            # Log error but don't fail
            pass


def get_output_path(filename: str) -> Path:
    """Get output path for generated files."""
    settings = get_settings()
    output_dir = Path(settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = Path(filename).stem
    ext = Path(filename).suffix
    
    return output_dir / f"{name}_{timestamp}{ext}"


def validate_file_size(file_path: Path, max_size_mb: int = 50) -> bool:
    """Validate file size is within limits."""
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_path.stat().st_size <= max_size_bytes
