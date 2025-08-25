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
    max_bullets: int = Form(6, ge=1, le=10, description="Maximum bullets per section"),
    doc_type: str = Form("Report", description="Document type"),
    title_override: Optional[str] = Form(None, description="Override document title"),
    target_slide_count: int = Form(20, ge=5, le=50, description="Target number of slides"),
    # --- SlideForge: Summary Configuration Parameters ---
    abstractive: bool = Form(False, description="Enable abstractive summarization"),
    abstractive_model_name: Optional[str] = Form(None, description="HuggingFace model for abstractive summarization"),
    diversity_lambda: float = Form(0.65, ge=0.0, le=1.0, description="MMR diversity parameter"),
    coverage_weight: float = Form(0.35, ge=0.0, le=1.0, description="Coverage vs salience tradeoff"),
    max_section_sentences: int = Form(10, ge=5, le=20, description="Maximum sentences to rank per section"),
    default_target_bullets: int = Form(4, ge=2, le=8, description="Default bullets per section"),
    default_max_words: int = Form(18, ge=10, le=25, description="Default max words per bullet"),
    default_emphasize_words: int = Form(2, ge=0, le=5, description="Default words to emphasize"),
    methods_numbered: bool = Form(True, description="Use numbered lists for Methods section"),
    include_keyphrases: bool = Form(True, description="Include keyphrases in summaries"),
    # --- SlideForge: Paging Configuration Parameters ---
    bullets_per_slide: int = Form(4, ge=2, le=8, description="Bullets per slide (hard cap)"),
    min_slides_per_section: int = Form(1, ge=1, le=3, description="Minimum slides per section"),
    max_slides_per_section: int = Form(5, ge=3, le=10, description="Maximum slides per section"),
    allow_supplementary_sections: bool = Form(True, description="Add supplementary slides when needed"),
    # --- SlideForge: Slide Planner Configuration Parameters ---
    planner_target_slides: int = Form(20, ge=5, le=50, description="Target total slides for planner"),
    planner_max_supplementary: int = Form(1, ge=0, le=2, description="Maximum supplementary slides (0-2)"),
    planner_min_per_section: int = Form(1, ge=1, le=3, description="Minimum slides per section"),
    planner_max_per_section: int = Form(6, ge=3, le=10, description="Maximum slides per section"),
    planner_bullets_per_slide: int = Form(4, ge=2, le=8, description="Bullets per slide for planner")
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
        
        # Build summary configuration
        from ..models.schema import GlobalSummaryConfig, SectionSummarySpec
        
        # Create default spec
        default_spec = SectionSummarySpec(
            target_bullets=default_target_bullets,
            max_words_per_bullet=default_max_words,
            emphasize_first_words=default_emphasize_words,
            include_keyphrases=include_keyphrases
        )
        
        # Create per-section overrides
        per_section = {}
        if methods_numbered:
            per_section["METHODS"] = SectionSummarySpec(
                target_bullets=default_target_bullets,
                max_words_per_bullet=default_max_words,
                list_type="numbered",
                emphasize_first_words=default_emphasize_words,
                include_keyphrases=include_keyphrases
            )
        
        summary_cfg = GlobalSummaryConfig(
            default=default_spec,
            per_section=per_section,
            abstractive=abstractive,
            abstractive_model_name=abstractive_model_name,
            diversity_lambda=diversity_lambda,
            coverage_weight=coverage_weight,
            max_section_sentences=max_section_sentences
        )
        
        # Build paging configuration
        from ..models.schema import PagingConfig, DeckTargets
        paging_cfg = PagingConfig(
            bullets_per_slide=bullets_per_slide,
            min_slides_per_section=min_slides_per_section,
            max_slides_per_section=max_slides_per_section
        )
        deck_targets = DeckTargets(
            target_slide_count=target_slide_count,
            allow_supplementary_sections=allow_supplementary_sections
        )
        
        # Build planner configuration
        from ..models.schema import SlidePlannerConfig
        planner_cfg = SlidePlannerConfig(
            target_total_slides=planner_target_slides,
            max_supplementary_slides=planner_max_supplementary,
            min_slides_per_section=planner_min_per_section,
            max_slides_per_section=planner_max_per_section,
            bullets_per_slide=planner_bullets_per_slide
        )
        
        # Process request
        if pdf_file:
            response = await _process_pdf_upload(
                pdf_file, theme, max_bullets, logger, doc_type, title_override, 
                target_slide_count, summary_cfg, paging_cfg, deck_targets, planner_cfg
            )
        else:
            response = await _process_doi_url(
                doi, url, theme, max_bullets, logger, doc_type, title_override, 
                target_slide_count, summary_cfg, paging_cfg, deck_targets, planner_cfg
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
    logger,
    doc_type: str,
    title_override: Optional[str],
    target_slide_count: int,
    summary_cfg: GlobalSummaryConfig,
    paging_cfg: PagingConfig,
    deck_targets: DeckTargets,
    planner_cfg: SlidePlannerConfig
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
    
    # Extract metadata
    metadata = _extract_metadata_from_text(text)
    
    # Create generation parameters
    from ..models.schema import GenerationParams, DocumentType
    try:
        doc_type_enum = DocumentType(doc_type)
    except ValueError:
        doc_type_enum = DocumentType.GENERAL_REPORT
    
    params = GenerationParams(
        doc_type=doc_type_enum,
        title_override=title_override,
        target_slide_count=target_slide_count
    )
    
    # Generate PowerPoint using new AI summarization
    output_path = get_output_path("presentation.pptx")
    from app.services.ppt.builder import build_deck_from_text
    from app.models.schema import LayoutConfig
    
    layout = LayoutConfig()
    prs = build_deck_from_text(
        raw_text=text,
        meta_title=metadata.title,
        user_title=title_override,
        params=params,
        layout=layout,
        summary_cfg=summary_cfg,
        paging_cfg=paging_cfg,
        deck_targets=deck_targets,
        planner_cfg=planner_cfg
    )
    
    # Save presentation
    prs.save(str(output_path))
    pptx_path = str(output_path)
    slide_count = len(prs.slides)
    
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
    logger,
    doc_type: str,
    title_override: Optional[str],
    target_slide_count: int,
    summary_cfg: GlobalSummaryConfig,
    paging_cfg: PagingConfig,
    deck_targets: DeckTargets,
    planner_cfg: SlidePlannerConfig
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
