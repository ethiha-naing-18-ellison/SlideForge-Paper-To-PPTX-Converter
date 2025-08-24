"""Academic paper section detection and parsing."""

from __future__ import annotations

import re
from typing import Dict

from ..models.schema import PaperSections, SectionName


def split_into_sections(raw_text: str) -> PaperSections:
    """Split raw text into academic paper sections."""
    sections = PaperSections()
    
    # Define section patterns with common variations
    section_patterns = {
        SectionName.ABSTRACT: [
            r'abstract',
            r'abstract\s*:',
            r'abstract\s*\n',
        ],
        SectionName.INTRODUCTION: [
            r'introduction',
            r'introduction\s*:',
            r'introduction\s*\n',
            r'1\s*\.?\s*introduction',
        ],
        SectionName.METHODS: [
            r'methods',
            r'methods\s*:',
            r'methods\s*\n',
            r'methodology',
            r'materials?\s+and\s+methods',
            r'experimental',
            r'experiment',
            r'2\s*\.?\s*methods',
        ],
        SectionName.RESULTS: [
            r'results',
            r'results\s*:',
            r'results\s*\n',
            r'results?\s*&\s*discussion',
            r'3\s*\.?\s*results',
        ],
        SectionName.DISCUSSION: [
            r'discussion',
            r'discussion\s*:',
            r'discussion\s*\n',
            r'4\s*\.?\s*discussion',
        ],
        SectionName.CONCLUSION: [
            r'conclusion',
            r'conclusion\s*:',
            r'conclusion\s*\n',
            r'conclusions',
            r'summary',
            r'5\s*\.?\s*conclusion',
        ],
        SectionName.REFERENCES: [
            r'references',
            r'references\s*:',
            r'references\s*\n',
            r'reference',
            r'literature\s+cited',
            r'bibliography',
        ],
        SectionName.ACKNOWLEDGEMENTS: [
            r'acknowledgments?',
            r'acknowledgments?\s*:',
            r'acknowledgments?\s*\n',
            r'acknowledgement',
            r'thanks',
        ],
    }
    
    # Find section boundaries
    section_boundaries = _find_section_boundaries(raw_text, section_patterns)
    
    # Extract section content
    for section_name, (start_pos, end_pos) in section_boundaries.items():
        if start_pos is not None and end_pos is not None:
            content = raw_text[start_pos:end_pos].strip()
            if content:
                sections.sections[section_name] = content
    
    # Handle special cases
    _handle_special_sections(raw_text, sections)
    
    return sections


def _find_section_boundaries(
    text: str, 
    patterns: Dict[SectionName, list[str]]
) -> Dict[SectionName, tuple[int | None, int | None]]:
    """Find start and end positions for each section."""
    boundaries = {}
    text_lower = text.lower()
    
    # Find all section starts
    section_starts = []
    for section_name, pattern_list in patterns.items():
        for pattern in pattern_list:
            matches = list(re.finditer(pattern, text_lower, re.IGNORECASE))
            for match in matches:
                section_starts.append((match.start(), section_name))
    
    # Sort by position
    section_starts.sort(key=lambda x: x[0])
    
    # Determine boundaries
    for i, (start_pos, section_name) in enumerate(section_starts):
        # Find end position (next section start or end of text)
        if i + 1 < len(section_starts):
            end_pos = section_starts[i + 1][0]
        else:
            end_pos = len(text)
        
        boundaries[section_name] = (start_pos, end_pos)
    
    return boundaries


def _handle_special_sections(text: str, sections: PaperSections) -> None:
    """Handle special sections like key contributions, limitations, future work."""
    text_lower = text.lower()
    
    # Key contributions
    contribution_patterns = [
        r'key\s+contributions?',
        r'main\s+contributions?',
        r'contributions?',
        r'novelty',
    ]
    
    for pattern in contribution_patterns:
        if re.search(pattern, text_lower):
            content = _extract_section_content(text, pattern)
            if content:
                sections.sections[SectionName.KEY_CONTRIBUTIONS] = content
            break
    
    # Limitations
    limitation_patterns = [
        r'limitations?',
        r'limitations?\s*:',
        r'drawbacks',
        r'weaknesses',
    ]
    
    for pattern in limitation_patterns:
        if re.search(pattern, text_lower):
            content = _extract_section_content(text, pattern)
            if content:
                sections.sections[SectionName.LIMITATIONS] = content
            break
    
    # Future work
    future_patterns = [
        r'future\s+work',
        r'future\s+research',
        r'conclusion\s+and\s+future\s+work',
        r'outlook',
    ]
    
    for pattern in future_patterns:
        if re.search(pattern, text_lower):
            content = _extract_section_content(text, pattern)
            if content:
                sections.sections[SectionName.FUTURE_WORK] = content
            break


def _extract_section_content(text: str, pattern: str) -> str:
    """Extract content for a section based on pattern."""
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return ""
    
    start_pos = match.end()
    
    # Find next section or end of text
    # Look for common section headers
    next_section_pattern = r'\n\s*(?:abstract|introduction|methods|results|discussion|conclusion|references|acknowledgments?)\s*:?\s*\n'
    next_match = re.search(next_section_pattern, text[start_pos:], re.IGNORECASE)
    
    if next_match:
        end_pos = start_pos + next_match.start()
    else:
        end_pos = len(text)
    
    content = text[start_pos:end_pos].strip()
    return content


def extract_metadata_from_text(text: str) -> Dict[str, str]:
    """Extract basic metadata from text (title, authors, etc.)."""
    lines = text.split('\n')
    metadata = {}
    
    # Look for title in first few lines
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        if line and len(line) > 10 and len(line) < 200:
            # Check if line contains "Title:" prefix
            if line.lower().startswith('title:'):
                title = line[6:].strip()  # Remove "Title:" prefix
                if title:
                    metadata['title'] = title
                    break
            # Simple heuristic: title is usually longer than author names
            # and doesn't contain typical author patterns
            elif not re.search(r'[a-z]\s+[a-z]', line.lower()):  # No lowercase words
                metadata['title'] = line
                break
    
    # Look for authors (usually after title)
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
            # Simple heuristic for author lines
            elif re.search(r'[A-Z][a-z]+\s+[A-Z]', line):
                authors.append(line)
    
    if authors:
        metadata['authors'] = authors
    
    return metadata
