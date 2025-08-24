"""FastAPI v1 router for SlideForge backend."""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from ..core.config import get_settings
from ..core.logging import get_logger, log_event, log_error, log_performance
from ..models.schema import GenerateRequest, GenerateResponse, PaperMetadata
from ..services.extractor import extract_text_from_pdf
from ..services.sectionizer import split_into_sections
from ..services.summarizer import TextRankSummarizer, HFTransformerSummarizer
from ..services.ppt import build_presentation
from ..utils.fileio import save_uploaded_file, get_output_path, validate_file_size

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/generate", response_model=GenerateResponse)
async def generate_presentation(
    pdf_file: Optional[UploadFile] = File(None, description="PDF file to process"),
    doi: Optional[str] = Form(None, description="DOI identifier"),
    url: Optional[str] = Form(None, description="Paper URL"),
    theme: str = Form("academic", description="Presentation theme"),
    max_bullets: int = Form(6, ge=1, le=10, description="Maximum bullets per section")
) -> GenerateResponse:
    """Generate PowerPoint presentation from PDF or DOI/URL."""
    logger = get_logger(__name__)
    start_time = time.time()
    
    try:
        # Validate input
        if not pdf_file and not doi and not url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either PDF file, DOI, or URL must be provided"
            )
        
        # Process request
        if pdf_file:
            response = await _process_pdf_upload(
                pdf_file, theme, max_bullets, logger
            )
        else:
            response = await _process_doi_url(
                doi, url, theme, max_bullets, logger
            )
        
        # Log performance
        duration_ms = (time.time() - start_time) * 1000
        log_performance(logger, "presentation_generation", duration_ms)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(logger, "presentation_generation_failed", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate presentation: {str(e)}"
        )


@router.get("/download/{file_id}")
async def download_presentation(file_id: str):
    """Download generated PowerPoint file."""
    logger = get_logger(__name__)
    
    try:
        settings = get_settings()
        output_dir = Path(settings.output_dir)
        
        # Find file by ID
        file_pattern = f"{file_id}*.pptx"
        matching_files = list(output_dir.glob(file_pattern))
        
        if not matching_files:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        file_path = matching_files[0]
        
        log_event(logger, "file_download", file_id=file_id, file_path=str(file_path))
        
        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(logger, "file_download_failed", e, file_id=file_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file"
        )


async def _process_pdf_upload(
    pdf_file: UploadFile,
    theme: str,
    max_bullets: int,
    logger
) -> GenerateResponse:
    """Process PDF file upload."""
    # Validate file
    if not pdf_file.filename or not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a PDF"
        )
    
    # Save uploaded file
    file_path = save_uploaded_file(pdf_file)
    
    # Validate file size
    if not validate_file_size(file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit (50MB)"
        )
    
    # Extract text
    text = extract_text_from_pdf(str(file_path))
    
    # Extract sections
    sections = split_into_sections(text)
    
    # Extract metadata
    metadata = _extract_metadata_from_text(text)
    
    # Summarize sections
    summarized_sections = await _summarize_sections(sections, max_bullets, logger)
    
    # Generate PowerPoint
    output_path = get_output_path("presentation.pptx")
    pptx_path, slide_count = build_presentation(
        metadata, summarized_sections, theme, str(output_path)
    )
    
    # Generate file ID
    file_id = output_path.stem
    
    return GenerateResponse(
        pptx_path=str(pptx_path),
        slide_count=slide_count,
        metadata=metadata,
        file_id=file_id
    )


async def _process_doi_url(
    doi: Optional[str],
    url: Optional[str],
    theme: str,
    max_bullets: int,
    logger
) -> GenerateResponse:
    """Process DOI or URL request."""
    # TODO: Implement DOI/URL processing
    # For now, return error
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="DOI/URL processing not yet implemented"
    )


def _extract_metadata_from_text(text: str) -> PaperMetadata:
    """Extract metadata from text."""
    # Simple extraction for now
    lines = text.split('\n')
    
    # Find title (first non-empty line that looks like a title)
    title = "Research Paper"
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) > 10 and len(line) < 200:
            # Check if line contains "Title:" prefix
            if line.lower().startswith('title:'):
                title = line[6:].strip()  # Remove "Title:" prefix
                if title:
                    break
            # Simple heuristic: title is usually longer than author names
            elif not any(char.isdigit() for char in line):
                title = line
                break
    
    # Find authors
    authors = []
    for line in lines[:20]:
        line = line.strip()
        if line and ',' in line and len(line) < 100:
            # Check if line contains "Authors:" prefix
            if line.lower().startswith('authors:'):
                authors_text = line[8:].strip()  # Remove "Authors:" prefix
                if authors_text:
                    authors = [author.strip() for author in authors_text.split(',')]
                    break
    
    return PaperMetadata(
        title=title,
        authors=authors,
        venue=None,
        year=None,
        doi=None,
        url=None,
        abstract=None
    )


async def _summarize_sections(sections, max_bullets: int, logger) -> list:
    """Summarize sections using configured summarizer."""
    settings = get_settings()
    
    # Initialize summarizer
    if settings.summarizer_backend == "hf_transformer":
        try:
            summarizer = HFTransformerSummarizer(settings.hf_model_name)
        except Exception as e:
            logger.warning("HF transformer failed, falling back to TextRank", error=str(e))
            summarizer = TextRankSummarizer()
    else:
        summarizer = TextRankSummarizer()
    
    # Summarize each section
    summarized_sections = []
    for section_name, content in sections.sections.items():
        if content and len(content.strip()) > 50:
            bullets = summarizer.summarize_section(content, max_bullets)
            
            from ..models.schema import SummarizedSection
            summarized_sections.append(
                SummarizedSection(name=section_name, bullets=bullets)
            )
    
    return summarized_sections
