"""PowerPoint presentation builder service."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from ...models.schema import PaperMetadata, SummarizedSection
from ...utils.fileio import get_output_path


class BuildError(Exception):
    """Raised when PowerPoint generation fails."""
    pass


def build_presentation(
    metadata: PaperMetadata,
    sections: List[SummarizedSection],
    theme: str,
    output_path: str
) -> Tuple[str, int]:
    """Build PowerPoint presentation from summarized sections.
    
    Args:
        metadata: Paper metadata (title, authors, etc.)
        sections: List of summarized sections
        theme: Presentation theme (academic, minimal, corporate)
        output_path: Output file path
        
    Returns:
        Tuple of (pptx_path, slide_count)
    """
    try:
        # Create presentation
        prs = Presentation()
        
        # Apply theme
        _apply_theme(prs, theme)
        
        # Create slides
        slide_count = 0
        
        # Title slide
        slide_count += _create_title_slide(prs, metadata, theme)
        
        # Agenda slide
        slide_count += _create_agenda_slide(prs, sections, theme)
        
        # Section slides
        for section in sections:
            if section.bullets:
                slide_count += _create_section_slide(prs, section, theme)
        
        # References slide (if available)
        if metadata.doi or metadata.url:
            slide_count += _create_references_slide(prs, metadata, theme)
        
        # Save presentation
        prs.save(output_path)
        
        return output_path, slide_count
        
    except Exception as e:
        raise BuildError(f"Failed to build presentation: {str(e)}")


def _apply_theme(prs: Presentation, theme: str) -> None:
    """Apply theme to presentation."""
    # Set slide size (16:9 aspect ratio)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    # Theme-specific settings
    if theme == "academic":
        _apply_academic_theme(prs)
    elif theme == "minimal":
        _apply_minimal_theme(prs)
    elif theme == "corporate":
        _apply_corporate_theme(prs)
    else:
        _apply_academic_theme(prs)  # Default


def _apply_academic_theme(prs: Presentation) -> None:
    """Apply academic theme (serif fonts, formal styling)."""
    # This would typically load a .potx template
    # For now, we'll create a basic theme programmatically
    pass


def _apply_minimal_theme(prs: Presentation) -> None:
    """Apply minimal theme (clean, simple styling)."""
    pass


def _apply_corporate_theme(prs: Presentation) -> None:
    """Apply corporate theme (professional, branded styling)."""
    pass


def _create_title_slide(prs: Presentation, metadata: PaperMetadata, theme: str) -> int:
    """Create title slide."""
    slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    title = slide.shapes.title
    title.text = metadata.title
    _format_title(title, theme)
    
    # Subtitle (authors and venue)
    subtitle = slide.placeholders[1]
    subtitle_text = []
    
    if metadata.authors:
        authors_text = ", ".join(metadata.authors[:3])  # First 3 authors
        if len(metadata.authors) > 3:
            authors_text += f" et al. ({len(metadata.authors)} authors)"
        subtitle_text.append(authors_text)
    
    if metadata.venue:
        subtitle_text.append(metadata.venue)
    
    if metadata.year:
        subtitle_text.append(str(metadata.year))
    
    subtitle.text = "\n".join(subtitle_text)
    _format_subtitle(subtitle, theme)
    
    return 1


def _create_agenda_slide(prs: Presentation, sections: List[SummarizedSection], theme: str) -> int:
    """Create agenda slide."""
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    title = slide.shapes.title
    title.text = "Agenda"
    _format_title(title, theme)
    
    # Content
    content = slide.placeholders[1]
    agenda_items = []
    
    for section in sections:
        if section.bullets:
            section_name = section.name.value.replace("_", " ").title()
            agenda_items.append(f"• {section_name}")
    
    content.text = "\n".join(agenda_items)
    _format_content(content, theme)
    
    return 1


def _create_section_slide(prs: Presentation, section: SummarizedSection, theme: str) -> int:
    """Create slide for a section."""
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    title = slide.shapes.title
    section_name = section.name.value.replace("_", " ").title()
    title.text = section_name
    _format_title(title, theme)
    
    # Content
    content = slide.placeholders[1]
    content.text = "\n".join([f"• {bullet}" for bullet in section.bullets])
    _format_content(content, theme)
    
    return 1


def _create_references_slide(prs: Presentation, metadata: PaperMetadata, theme: str) -> int:
    """Create references slide."""
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    title = slide.shapes.title
    title.text = "References"
    _format_title(title, theme)
    
    # Content
    content = slide.placeholders[1]
    references = []
    
    if metadata.doi:
        references.append(f"DOI: {metadata.doi}")
    
    if metadata.url:
        references.append(f"URL: {metadata.url}")
    
    if metadata.venue and metadata.year:
        references.append(f"Published in: {metadata.venue} ({metadata.year})")
    
    content.text = "\n".join(references)
    _format_content(content, theme)
    
    return 1


def _format_title(title_shape, theme: str) -> None:
    """Format title text."""
    title_shape.text_frame.paragraphs[0].font.size = Pt(36)
    title_shape.text_frame.paragraphs[0].font.bold = True
    
    if theme == "academic":
        title_shape.text_frame.paragraphs[0].font.name = "Times New Roman"
    else:
        title_shape.text_frame.paragraphs[0].font.name = "Arial"


def _format_subtitle(subtitle_shape, theme: str) -> None:
    """Format subtitle text."""
    subtitle_shape.text_frame.paragraphs[0].font.size = Pt(24)
    subtitle_shape.text_frame.paragraphs[0].font.italic = True
    
    if theme == "academic":
        subtitle_shape.text_frame.paragraphs[0].font.name = "Times New Roman"
    else:
        subtitle_shape.text_frame.paragraphs[0].font.name = "Arial"


def _format_content(content_shape, theme: str) -> None:
    """Format content text."""
    content_shape.text_frame.paragraphs[0].font.size = Pt(20)
    
    if theme == "academic":
        content_shape.text_frame.paragraphs[0].font.name = "Times New Roman"
    else:
        content_shape.text_frame.paragraphs[0].font.name = "Arial"
