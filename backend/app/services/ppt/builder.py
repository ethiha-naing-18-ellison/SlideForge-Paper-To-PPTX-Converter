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

from ...models.schema import PaperMetadata, SummarizedSection, LayoutConfig, RenderOptions, StylePalette
from ...utils.fileio import get_output_path


class BuildError(Exception):
    """Raised when PowerPoint generation fails."""
    pass


def build_presentation(
    metadata: PaperMetadata,
    sections: List[SummarizedSection],
    theme: str,
    output_path: str,
    params: GenerationParams = None
) -> Tuple[str, int]:
    """Build PowerPoint presentation from summarized sections.
    
    Args:
        metadata: Paper metadata (title, authors, etc.)
        sections: List of summarized sections
        theme: Presentation theme (academic, minimal, corporate)
        output_path: Output file path
        params: Generation parameters (doc type, title override, target slides)
        
    Returns:
        Tuple of (pptx_path, slide_count)
    """
    try:
        # Use default params if none provided
        params = params or GenerationParams()
        
        # Create presentation with layout config
        prs, layout = init_presentation()
        
        # Apply theme
        _apply_theme(prs, theme)
        
        # Create slides
        slide_count = 0
        
        # Title slide with proper title and doc type
        doc_title = params.title_override or metadata.title or "Untitled Document"
        doc_type_label = params.doc_type.value
        authors_or_owner = ", ".join(metadata.authors[:3]) if metadata.authors else None
        if metadata.authors and len(metadata.authors) > 3:
            authors_or_owner += f" et al. ({len(metadata.authors)} authors)"
        
        add_title_slide(prs, layout, doc_title, doc_type_label, authors_or_owner)
        slide_count += 1
        
        # Agenda slide
        slide_count += _create_agenda_slide(prs, sections, theme)
        
        # Section slides with pagination
        for section in sections:
            if section.bullets:
                slide_count += _create_section_slide_paginated(prs, section, theme, layout)
        
        # Ensure conclusion slide exists
        conclusion_slides = ensure_conclusion_slide(prs, layout, sections)
        if conclusion_slides:
            slide_count += len(conclusion_slides)
        
        # References slide (if available)
        if metadata.doi or metadata.url:
            slide_count += _create_references_slide(prs, metadata, theme)
        
        # Expand to target slide count if needed
        expand_to_target_slides(prs, params.target_slide_count)
        
        # Final cleanup pass to remove any remaining placeholders
        finalize_presentation(prs)
        
        # Save presentation
        prs.save(output_path)
        
        return output_path, len(prs.slides)
        
    except Exception as e:
        raise BuildError(f"Failed to build presentation: {str(e)}")


def init_presentation(layout: LayoutConfig | None = None):
    """Initialize presentation with proper layout configuration."""
    layout = layout or LayoutConfig()
    prs = Presentation()
    prs.slide_width = Inches(layout.slide_width_in)
    prs.slide_height = Inches(layout.slide_height_in)
    return prs, layout

def _apply_theme(prs: Presentation, theme: str) -> None:
    """Apply theme to presentation."""
    # Slide size is now set in init_presentation()
    
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


# --- SlideForge: Safe Pagination Hook (append) ---
from pptx.util import Inches, Pt
from .paginator import split_bullets_to_fit, render_bullets_block
from .cleanup import remove_unused_placeholders
from .richtext import tokenize_inline
from .styling import hex_to_rgb, split_by_keywords
from ...models.schema import RenderOptions, StylePalette

def _usable_box(layout: LayoutConfig) -> tuple[float, float, float, float]:
    """Return (left, top, width, height) in inches for the content area beneath the title."""
    left = layout.margin_left_in
    top = layout.margin_top_in + layout.title_height_in
    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    height = layout.slide_height_in - layout.margin_top_in - layout.margin_bottom_in - layout.title_height_in
    return left, top, width, height

def _blank_layout(prs):
    """
    Return a layout that has no placeholders. Fallback to the last layout if index 6 not available.
    """
    try:
        # Usually layout index 6 is 'Blank' in 16:9 themes
        return prs.slide_layouts[6]
    except Exception:
        # Fallback: pick a layout with least placeholders
        layouts = list(prs.slide_layouts)
        best = min(layouts, key=lambda l: len(getattr(l, "placeholders", [])))
        return best

def add_blank_slide(prs):
    slide = prs.slides.add_slide(_blank_layout(prs))
    # Defensive: in case the chosen layout still has placeholders, remove them
    try:
        remove_unused_placeholders(slide)
    except Exception:
        pass
    return slide

def add_title_textbox(slide, text: str, left_in: float, top_in: float, width_in: float, height_in: float, pt: int = 32):
    tb = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    run = p.runs[0] if p.runs else p
    try:
        run.font.size = Pt(pt)
    except Exception:
        pass
    try:
        from pptx.enum.text import MSO_AUTO_SIZE
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    except Exception:
        pass
    return tb

def add_titled_slide_placeholder_free(prs, layout_cfg, title_text: str):
    slide = add_blank_slide(prs)
    # Draw our own title box within margins
    left = layout_cfg.margin_left_in
    top = layout_cfg.margin_top_in
    width = layout_cfg.slide_width_in - layout_cfg.margin_left_in - layout_cfg.margin_right_in
    height = layout_cfg.title_height_in
    add_title_textbox(slide, title_text, left, top, width, height, pt=32)
    # Ensure no default placeholders remain
    remove_unused_placeholders(slide)
    return slide

def add_titled_slide(prs, theme_layout, title_text: str):
    slide = prs.slides.add_slide(theme_layout)
    # Robust title: shrink if too long
    if slide.shapes.title:
        title = slide.shapes.title
        title.text_frame.word_wrap = True
        try:
            from pptx.enum.text import MSO_AUTO_SIZE
            title.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        except Exception:
            pass
        title.text_frame.paragraphs[0].text = title_text
        title.text_frame.paragraphs[0].font.size = Pt(32)
        title.text_frame.paragraphs[0].font.bold = True
    return slide

def add_section_with_bullets_paginated(
    prs,
    theme_layout,
    layout: LayoutConfig,
    section_title: str,
    bullets: list[str]
) -> list:
    """Create one or more slides so that content never overflows bounds."""
    slides = []
    left, top, width, height = _usable_box(layout)

    # 1) Split bullets into one-or-more slides, choosing font size that fits or paginating
    chunks = split_bullets_to_fit(
        bullets=bullets,
        box_width_in=width,
        max_height_in=height,
        font_max_pt=layout.bullet_font_max_pt,
        font_min_pt=layout.bullet_font_min_pt,
        line_spacing=layout.bullet_line_spacing,
        max_lines_per_item=layout.bullet_max_lines_per_item,
    )

    # 2) Render each chunk on its own slide
    for idx, (chunk, font_pt) in enumerate(chunks):
        title_text = section_title if idx == 0 else f"{section_title} (cont.)"
        slide = add_titled_slide_placeholder_free(prs, layout, title_text)
        
        # Choose render options based on section type
        if "method" in section_title.lower():
            # Methods get numbered lists with emphasized first words
            render_options = RenderOptions(
                list_type="numbered",
                emphasize_first_words=3,
                highlight_keywords=["step", "process", "method", "technique"]
            )
        else:
            # Other sections get bullets with default styling
            render_options = RenderOptions(
                list_type="bullets",
                emphasize_first_words=0,
                highlight_keywords=["key contribution", "result", "impact", "limitation", "future work"]
            )
        
        render_styled_bullets(
            slide=slide,
            left_in=left, top_in=top, width_in=width, height_in=height,
            bullets=chunk,
            font_pt=font_pt,
            line_spacing=layout.bullet_line_spacing,
            palette=StylePalette(),
            options=render_options
        )
        # Ensure no default placeholders remain after rendering content
        remove_unused_placeholders(slide)
        slides.append(slide)
    return slides

def _create_section_slide_paginated(prs: Presentation, section: SummarizedSection, theme: str, layout: LayoutConfig) -> int:
    """Create paginated slides for a section."""
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    section_name = section.name.value.replace("_", " ").title()
    
    slides = add_section_with_bullets_paginated(
        prs=prs,
        theme_layout=slide_layout,
        layout=layout,
        section_title=section_name,
        bullets=section.bullets
    )
    
    return len(slides)

def finalize_presentation(prs):
    """Final cleanup pass to remove any remaining placeholders."""
    for s in prs.slides:
        try:
            remove_unused_placeholders(s)
        except Exception:
            continue
    return prs


# --- SlideForge Enhanced Bullet Rendering (append) ---
from pptx.util import Inches, Pt
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.oxml.xmlchemy import OxmlElement

def render_styled_bullets(
    slide,
    left_in: float, top_in: float, width_in: float, height_in: float,
    bullets: list[str],
    font_pt: int,
    line_spacing: float,
    palette: StylePalette,
    options: RenderOptions,
):
    box = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    tf = box.text_frame
    tf.word_wrap = True
    try:
        from pptx.enum.text import MSO_AUTO_SIZE
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    except Exception:
        pass

    tf.clear()  # start clean

    for idx, raw in enumerate(bullets):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.level = 0
        p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
        p.space_after = Pt(6)
        p.line_spacing = line_spacing

        # numbering vs bullets
        if options.list_type == "numbered":
            p.numbered = True
        else:
            p.level = 0  # default bullet from theme
            p.numbered = False

        text_to_render = raw

        # Optional: emphasize first N words in bold
        if options.emphasize_first_words and " " in text_to_render:
            parts = text_to_render.split()
            n = min(len(parts), options.emphasize_first_words)
            text_to_render = "**" + " ".join(parts[:n]) + "** " + " ".join(parts[n:])

        # Keyword highlighting (colorize matches)
        segments_key = split_by_keywords(text_to_render, options.highlight_keywords)
        for seg_text, is_key in segments_key:
            # Inline markup
            if options.enable_inline_markup:
                rt_parts = tokenize_inline(seg_text)
            else:
                rt_parts = [(seg_text, {"bold": False, "italic": False, "underline": False})]

            for txt, style in rt_parts:
                run = p.add_run()
                run.text = txt
                if font_pt:
                    run.font.size = Pt(font_pt)
                run.font.bold = style.get("bold", False)
                run.font.italic = style.get("italic", False)
                run.font.underline = style.get("underline", False)

                # base color
                run.font.color.rgb = hex_to_rgb(palette.text_primary)
                # key color override
                if is_key and options.key_color:
                    run.font.color.rgb = hex_to_rgb(options.key_color)

# --- SlideForge: Title, Conclusion, Target Slides (append) ---
from ...models.schema import LayoutConfig, GenerationParams, DocumentType
from .cleanup import remove_unused_placeholders
from .paginator import render_bullets_block
from .expander import expand_to_target_slides

def add_title_slide(prs, layout: LayoutConfig, doc_title: str, doc_type_label: str, authors_or_owner: str | None = None):
    slide = add_titled_slide_placeholder_free(prs, layout, doc_title or "Untitled")
    # Add subtitle line (doc type + optional owner)
    left = layout.margin_left_in
    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    top = layout.margin_top_in + layout.title_height_in + 0.15
    height = 0.6
    subtitle = doc_type_label if not authors_or_owner else f"{doc_type_label}  •  {authors_or_owner}"
    add_title_textbox(slide, subtitle, left, top, width, height, pt=18)
    remove_unused_placeholders(slide)
    return slide

def ensure_conclusion_slide(prs, layout: LayoutConfig, summarized_sections: list):
    """
    If a 'Conclusion' section was not rendered, synthesize one from existing bullets.
    """
    found = False
    for s in prs.slides:
        for shp in s.shapes:
            if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
                txt = "".join(p.text or "" for p in shp.text_frame.paragraphs).strip().lower()
                if txt.startswith("conclusion") or "conclusion (cont.)" in txt:
                    found = True
                    break
        if found:
            break
    if found:
        return

    # Synthesize: collect up to 6 top bullets across sections
    bullets = []
    for sec in summarized_sections:
        for b in getattr(sec, "bullets", [])[:2]:
            bullets.append(b)
        if len(bullets) >= 6:
            break

    if not bullets:
        bullets = ["This document has been summarized into key insights.", "Please see previous slides for details."]

    slides = add_section_with_bullets_paginated(
        prs=prs,
        theme_layout=None,   # not used by placeholder_free path
        layout=layout,
        section_title="Conclusion",
        bullets=bullets
    )
    return slides
