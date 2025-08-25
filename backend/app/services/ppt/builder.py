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

from app.models.schema import PaperMetadata, SummarizedSection, LayoutConfig, RenderOptions, StylePalette
from app.utils.fileio import get_output_path


class BuildError(Exception):
    """Raised when PowerPoint generation fails."""
    pass


# --- SlideForge: Use AI section summaries (append) ---
from app.summarizer.section_summarizer import summarize_sections
from app.models.schema import GlobalSummaryConfig, SectionSummarySpec, PagingConfig, DeckTargets, SlidePlannerConfig
from app.services.extractor import resolve_title

# --- SlideForge: Formatting Fixes (append) ---
from .titleblock import create_clean_title_slide
from .footer import apply_footer_to_all_slides
from .cleantext import normalize_text, split_runs_from_markdown, clean_bullet_text, remove_raw_markdown
from .callouts import add_keyterms_callout
from .bullets_preprocess import preprocess_for_slide
from .markdown_runs import to_runs
from .sections import canonicalize, cont_title, get_section_display_name, clean_section_title
from .labels import strip_label_prefix
from app.summarizer.conclusion import create_conclusion_slide_content

def build_deck_from_text(
    raw_text: str,
    meta_title: str | None,
    user_title: str | None,
    params,              # GenerationParams from earlier work
    layout: LayoutConfig,
    summary_cfg: GlobalSummaryConfig | None = None,
    paging_cfg: PagingConfig | None = None,
    deck_targets: DeckTargets | None = None,
    planner_cfg: SlidePlannerConfig | None = None
):
    summary_cfg = summary_cfg or GlobalSummaryConfig()
    prs, layout = init_presentation(layout)
    # Title
    title = resolve_title(raw_text, meta_title=meta_title, user_title=user_title)
    create_clean_title_slide(prs, layout, title, params.doc_type.value, authors=None)

    # Use simple section mapper for better section detection
    sections_raw = map_sections_by_content(raw_text)
    sec_map = {}
    
    # Summarize each detected section
    for section_name, section_text in sections_raw.items():
        if section_text.strip():
            bullets = summarize_section_with_budget(
                section_text, 
                summary_cfg,
                summary_cfg.default.target_bullets,
                summary_cfg.default.max_words_per_bullet
            )
            if bullets:
                sec_map[section_name] = bullets

    # Use topic-aware rendering if planner config is provided, otherwise fall back to old method
    if planner_cfg:
        render_deck_topic_aware(prs, raw_text, layout, summary_cfg, planner_cfg)
    else:
        # Fallback to old rendering method
        order = ["ABSTRACT","INTRODUCTION","METHODS","RESULTS","DISCUSSION","LIMITATIONS","CONCLUSION","FUTURE WORK","OTHER"]
        paging = paging_cfg or DEFAULT_PAGING  # Use provided paging config or default
        
        for name in order:
            if name in sec_map and sec_map[name]:
                bullets = sec_map[name]
                
                # Remove inline key terms before preprocessing (already handled in sanitize_lines)
                bullets = [b for b in bullets if b]
                
                # Get canonical section name
                canon_name = canonicalize(name)
                display_name = clean_section_title(get_section_display_name(canon_name))
                
                # Preprocess bullets for this section
                pre_bullets, list_type = preprocess_for_slide(
                    raw_lines=bullets,
                    canon_section=canon_name,
                    max_words_per_bullet=18,
                    max_bullets=5,
                    emphasize_n_words=2,
                )
                
                # Create render options
                options = RenderOptions(
                    list_type=list_type,  # 'numbered' for Methods, else 'bullets'
                    enable_inline_markup=True,
                    emphasize_first_words=0,  # already applied by preprocessor
                )
                
                # Use new paging function instead of old pagination
                slides = render_section_with_paging(
                    prs=prs,
                    layout=layout,
                    section_title=display_name,
                    bullets=pre_bullets,
                    paging=paging,
                    font_pt=layout.bullet_font_min_pt,
                    line_spacing=layout.bullet_line_spacing,
                    options=options,
                    palette=StylePalette()
                )
                
                # Add key terms callout to first slide of each section
                if slides and name in sec_map:
                    # Extract key terms from this section's text
                    from app.nlp.keyphrase import extract_keyphrases
                    section_text = " ".join(bullets)
                    key_terms = extract_keyphrases(section_text, top_k=3)
                    if key_terms:
                        add_keyterms_callout(slides[0], layout, key_terms)

    # Enhanced expansion to meet target slide count
    from app.services.ppt.expander import expand_to_target_slides, expand_to_target_slides_supplement, add_supplementary
    
    # First try splitting any dense slides
    expand_to_target_slides(prs, params.target_slide_count)
    
    # Use planner config if provided, otherwise use deck targets or params
    if planner_cfg:
        target_count = planner_cfg.target_total_slides
        # If still short, add limited supplementary slides (capped)
        needed = target_count - len(prs.slides)
        if needed > 0:
            add_supplementary(prs, max_supplementary=planner_cfg.max_supplementary_slides, raw_text=raw_text)
    else:
        # Use deck targets if provided, otherwise use params
        target_count = deck_targets.target_slide_count if deck_targets else params.target_slide_count
        
        # If still short, add supplementary slides
        if len(prs.slides) < target_count:
            expand_to_target_slides_supplement(prs, target_count, raw_text)
    
    # Apply final formatting: footers, conclusion, cleanup
    _apply_final_formatting(prs, layout, title, sec_map)
    
    return prs

# --- SlideForge: Per-section Paging Hook (append) ---
from app.models.schema import PagingConfig, DeckTargets
from app.services.ppt.pager import chunk_bullets

DEFAULT_PAGING = PagingConfig(bullets_per_slide=4, min_slides_per_section=1, max_slides_per_section=5)

def render_section_with_paging(
    prs,
    layout,
    section_title: str,
    bullets: list[str],
    paging: PagingConfig,
    font_pt: int,
    line_spacing: float,
    options,   # RenderOptions from styling
    palette    # StylePalette
):
    # Split bullets into per-slide chunks
    pages = chunk_bullets(
        bullets=bullets,
        bullets_per_slide=paging.bullets_per_slide,
        min_slides=paging.min_slides_per_section,
        max_slides=paging.max_slides_per_section,
    )

    slides = []
    left = layout.margin_left_in
    top = layout.margin_top_in + layout.title_height_in
    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    height = layout.slide_height_in - layout.margin_top_in - layout.margin_bottom_in - layout.title_height_in

    for idx, page_bullets in enumerate(pages):
        title = section_title if idx == 0 else f"{section_title} (cont.)"
        slide = add_titled_slide_placeholder_free(prs, layout, title)
        # Use the same styled bullet renderer (already no-overflow safe via our earlier pagination)
        render_styled_bullets(
            slide=slide,
            left_in=left, top_in=top, width_in=width, height_in=height,
            bullets=page_bullets,
            font_pt=font_pt,
            line_spacing=line_spacing,
            palette=palette,
            options=options
        )
        remove_unused_placeholders(slide)
        slides.append(slide)
    return slides

# --- SlideForge: Topic-aware section rendering (append) ---
from app.services.ppt.planner import allocate_slides
from app.nlp.segmenter import split_to_sections, sentences
from app.nlp.topic_chunker import cluster_sentences, topic_subtitles
from app.summarizer.section_summarizer import summarize_section_with_budget
from app.nlp.abstractive import abstractive_summarize
from .simple_sections import map_sections_by_content

def render_deck_topic_aware(
    prs, raw_text: str, layout, summary_cfg, planner: SlidePlannerConfig
):
    # 1) Decide slides per section
    section_to_n = allocate_slides(
        raw_text=raw_text,
        target_total=planner.target_total_slides - 1,  # reserve title
        min_per=planner.min_slides_per_section,
        max_per=planner.max_slides_per_section,
        bias=planner.allocation_bias or {"INTRODUCTION":1.2,"METHODS":1.4,"RESULTS":1.4,"CONCLUSION":1.1}
    )

    # 2) For each section, create topic clusters and render subslides
    sections_raw = map_sections_by_content(raw_text)
    for raw_h, text in sections_raw.items():
        name = canonicalize(raw_h)
        desired_slides = max(planner.min_slides_per_section, section_to_n.get(name, 0))
        if desired_slides <= 0:
            continue

        # cluster sentences into desired_slides topics
        sents = sentences(text)[: max(5, summary_cfg.max_section_sentences * 2)]
        clusters = cluster_sentences(sents, desired_slides)
        subtitles = topic_subtitles(sents, clusters)

        for idx, ids in enumerate(clusters):
            # bullet budget for this subslide
            bullet_budget = planner.bullets_per_slide
            chosen = [sents[i] for i in ids]
            bullets = abstractive_summarize(chosen, summary_cfg.abstractive_model_name if summary_cfg.abstractive else None, summary_cfg.default.max_words_per_bullet)
            bullets = bullets[:bullet_budget]
            
            # Remove inline key terms before preprocessing (already handled in sanitize_lines)
            bullets = [b for b in bullets if b]
            
            # Get canonical section name
            canon_name = canonicalize(name)
            display_name = clean_section_title(get_section_display_name(canon_name))
            
            # Preprocess bullets for this topic
            pre_bullets, list_type = preprocess_for_slide(
                raw_lines=bullets,
                canon_section=canon_name,
                max_words_per_bullet=18,
                max_bullets=5,
                emphasize_n_words=2,
            )
            
            subtitle = f"{display_name} — {subtitles[idx]}" if subtitles[idx] else display_name
            slides = render_section_with_paging(
                prs=prs, layout=layout, section_title=subtitle,
                bullets=pre_bullets, paging=PagingConfig(bullets_per_slide=planner.bullets_per_slide, min_slides_per_section=1, max_slides_per_section=1),
                font_pt=layout.bullet_font_min_pt, line_spacing=layout.bullet_line_spacing,
                options=RenderOptions(list_type=list_type, enable_inline_markup=True, emphasize_first_words=0),
                palette=StylePalette()
            )
            
            # Add key terms callout to first slide
            if slides:
                from app.nlp.keyphrase import extract_keyphrases
                section_text = " ".join(chosen)
                key_terms = extract_keyphrases(section_text, top_k=3)
                if key_terms:
                    add_keyterms_callout(slides[0], layout, key_terms)

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
        
        # Title slide already created above
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
from app.models.schema import RenderOptions, StylePalette

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

        # Use robust markdown formatting for the text
        runs = to_runs(text_to_render)
        
        # Render each run with proper formatting
        for txt, style in runs:
            run = p.add_run()
            run.text = txt
            if font_pt:
                run.font.size = Pt(font_pt)
            run.font.bold = style.get("b", False)
            run.font.italic = style.get("i", False)
            run.font.underline = style.get("u", False)
            
            # base color
            run.font.color.rgb = hex_to_rgb(palette.text_primary)

# --- SlideForge: Title, Conclusion, Target Slides (append) ---
from app.models.schema import LayoutConfig, GenerationParams, DocumentType
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

# --- SlideForge: Cleanup and Final Formatting (append) ---

def _is_meaningless(slide):
    """Check if a slide is meaningless (only generic text, no content)."""
    texts = []
    for shp in slide.shapes:
        if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
            txt = " ".join(p.text or "" for p in shp.text_frame.paragraphs).strip().lower()
            if txt:
                texts.append(txt)
    
    if not texts:
        return True
    
    # Check for generic titles
    if len(texts) == 1 and texts[0] in {"report", "other", "untitled"}:
        return True
    
    return False

def _dedupe_adjacent(slides):
    """Remove adjacent duplicate slides."""
    keep = []
    last_sig = None
    
    for s in slides:
        first = ""
        title = ""
        
        for shp in s.shapes:
            if getattr(shp, "text_frame", None) and shp.text_frame and shp.text_frame.paragraphs:
                txt = shp.text_frame.paragraphs[0].text.strip().lower()
                if not title:
                    title = txt
                if not first and len(shp.text_frame.paragraphs) > 1:
                    first = shp.text_frame.paragraphs[1].text.strip().lower()
        
        sig = (title, first)
        if sig != last_sig:
            keep.append(s)
        last_sig = sig
    
    return keep

def _render_markdown_text_to_paragraph(paragraph, md_text: str, font_pt: int):
    """Render markdown text to a paragraph with proper formatting."""
    runs = split_runs_from_markdown(md_text)
    
    for i, (txt, style) in enumerate(runs):
        if i == 0 and paragraph.runs:
            r = paragraph.runs[0]
        else:
            r = paragraph.add_run()
        
        r.text = txt
        try:
            r.font.size = Pt(font_pt)
            r.font.bold = style.get("b", False)
            r.font.italic = style.get("i", False)
            r.font.underline = style.get("u", False)
        except Exception:
            pass

def _clean_and_format_bullets(bullets: list[str], max_words: int = 18) -> list[str]:
    """Clean and format bullet points."""
    cleaned = []
    for bullet in bullets:
        if bullet:
            # Clean the bullet text
            clean_bullet = clean_bullet_text(bullet, max_words)
            if clean_bullet:
                # Split long bullets into multiple if they contain semicolons or commas
                if len(clean_bullet.split()) > max_words and (";" in clean_bullet or "," in clean_bullet):
                    if ";" in clean_bullet:
                        parts = [p.strip() for p in clean_bullet.split(";") if p.strip()]
                    else:
                        parts = [p.strip() for p in clean_bullet.split(",") if p.strip()]
                    
                    # Add each part as a separate bullet if it's reasonable length
                    for part in parts:
                        if len(part.split()) <= max_words and part:
                            cleaned.append(part)
                else:
                    cleaned.append(clean_bullet)
    return cleaned

def _is_meaningless(slide) -> bool:
    """Check if a slide contains only meaningless content."""
    texts = []
    for shp in slide.shapes:
        if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
            txt = " ".join((p.text or "") for p in shp.text_frame.paragraphs).strip().lower()
            if txt:
                texts.append(txt)
    
    return (not texts) or (len(texts) == 1 and texts[0] in {"report", "other", "untitled"})

def _dedupe_adjacent(prs):
    """Remove adjacent duplicate slides."""
    keep = []
    last_sig = None
    
    for s in list(prs.slides):
        first = ""
        title = ""
        
        for shp in s.shapes:
            if getattr(shp, "text_frame", None) and shp.text_frame and shp.text_frame.paragraphs:
                txt = shp.text_frame.paragraphs[0].text.strip().lower()
                if not title:
                    title = txt
                if not first and len(shp.text_frame.paragraphs) > 1:
                    first = shp.text_frame.paragraphs[1].text.strip().lower()
        
        sig = (title, first)
        if sig != last_sig and not _is_meaningless(s):
            keep.append(s)
        last_sig = sig
    
    return keep

def _apply_final_formatting(prs, layout, doc_title: str, sec_map: dict):
    """Apply final formatting: footers, conclusion, cleanup."""
    # Apply footers to all slides
    apply_footer_to_all_slides(prs, layout, doc_title)
    
    # Ensure we have a proper conclusion
    if "CONCLUSION" not in sec_map or not sec_map["CONCLUSION"]:
        conclusion_bullets, key_terms = create_conclusion_slide_content(sec_map)
        sec_map["CONCLUSION"] = conclusion_bullets
        
        # Remove inline key terms and preprocess conclusion bullets (already handled in sanitize_lines)
        conclusion_bullets = [b for b in conclusion_bullets if b]
        pre_conclusion, list_type = preprocess_for_slide(
            raw_lines=conclusion_bullets,
            canon_section="CONCLUSION",
            max_words_per_bullet=18,
            max_bullets=4,
            emphasize_n_words=2,
        )
        
        # Render conclusion slide
        slides = render_section_with_paging(
            prs=prs,
            layout=layout,
            section_title="Conclusion",
            bullets=pre_conclusion,
            paging=PagingConfig(bullets_per_slide=4, min_slides_per_section=1, max_slides_per_section=2),
            font_pt=layout.bullet_font_min_pt,
            line_spacing=layout.bullet_line_spacing,
            options=RenderOptions(list_type=list_type, enable_inline_markup=True, emphasize_first_words=0),
            palette=StylePalette()
        )
        
        # Add key terms callout to conclusion slide
        if slides and key_terms:
            add_keyterms_callout(slides[0], layout, key_terms)
    
    # Note: Slide removal is complex with python-pptx and can cause issues
    # For now, we'll skip automatic slide removal to avoid errors
    # The meaningless slide detection is available for future use
    pass
