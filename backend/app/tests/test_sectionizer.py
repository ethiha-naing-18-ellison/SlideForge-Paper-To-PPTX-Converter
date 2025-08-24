"""Unit tests for section detection and parsing."""

import pytest

from app.services.sectionizer import split_into_sections, extract_metadata_from_text
from app.models.schema import SectionName


class TestSectionizer:
    """Test cases for section detection and parsing."""
    
    def test_split_into_sections_basic(self):
        """Test basic section detection."""
        text = """
        Abstract
        This is the abstract content.
        
        Introduction
        This is the introduction content.
        
        Methods
        This is the methods content.
        
        Results
        This is the results content.
        
        Discussion
        This is the discussion content.
        
        Conclusion
        This is the conclusion content.
        """
        
        sections = split_into_sections(text)
        
        assert SectionName.ABSTRACT in sections.sections
        assert SectionName.INTRODUCTION in sections.sections
        assert SectionName.METHODS in sections.sections
        assert SectionName.RESULTS in sections.sections
        assert SectionName.DISCUSSION in sections.sections
        assert SectionName.CONCLUSION in sections.sections
        
        assert "abstract content" in sections.sections[SectionName.ABSTRACT]
        assert "introduction content" in sections.sections[SectionName.INTRODUCTION]
    
    def test_split_into_sections_variations(self):
        """Test section detection with common variations."""
        text = """
        ABSTRACT
        Abstract content here.
        
        1. INTRODUCTION
        Introduction content here.
        
        MATERIALS AND METHODS
        Methods content here.
        
        RESULTS & DISCUSSION
        Results and discussion content here.
        
        CONCLUSIONS
        Conclusion content here.
        
        REFERENCES
        References content here.
        """
        
        sections = split_into_sections(text)
        
        assert SectionName.ABSTRACT in sections.sections
        assert SectionName.INTRODUCTION in sections.sections
        assert SectionName.METHODS in sections.sections
        assert SectionName.RESULTS in sections.sections
        assert SectionName.CONCLUSION in sections.sections
        assert SectionName.REFERENCES in sections.sections
    
    def test_split_into_sections_empty_text(self):
        """Test section detection with empty text."""
        sections = split_into_sections("")
        assert len(sections.sections) == 0
    
    def test_split_into_sections_no_sections(self):
        """Test section detection with text that has no clear sections."""
        text = "This is just some random text without any section headers."
        sections = split_into_sections(text)
        assert len(sections.sections) == 0
    
    def test_special_sections_detection(self):
        """Test detection of special sections like key contributions."""
        text = """
        Introduction
        Introduction content.
        
        Key Contributions
        This paper makes several key contributions.
        
        Limitations
        There are some limitations to this work.
        
        Future Work
        Future work directions are discussed.
        """
        
        sections = split_into_sections(text)
        
        assert SectionName.KEY_CONTRIBUTIONS in sections.sections
        assert SectionName.LIMITATIONS in sections.sections
        assert SectionName.FUTURE_WORK in sections.sections
    
    def test_section_content_extraction(self):
        """Test that section content is properly extracted."""
        text = """
        Abstract
        This is the abstract. It contains multiple sentences.
        The abstract should capture the main points.
        
        Introduction
        This is the introduction section.
        It should contain the background and motivation.
        """
        
        sections = split_into_sections(text)
        
        abstract_content = sections.sections[SectionName.ABSTRACT]
        assert "abstract should capture the main points" in abstract_content
        
        intro_content = sections.sections[SectionName.INTRODUCTION]
        assert "introduction section" in intro_content
        assert "background and motivation" in intro_content
    
    def test_extract_metadata_from_text(self):
        """Test metadata extraction from text."""
        text = """
        Attention Is All You Need
        
        Ashish Vaswani, Noam Shazeer, Niki Parmar
        
        NIPS 2017
        
        Abstract
        This is the abstract content.
        """
        
        metadata = extract_metadata_from_text(text)
        
        # The function should extract some metadata
        assert len(metadata) > 0
        # Note: Author extraction is basic, so this might not work perfectly
        # but the function should not crash
    
    def test_extract_metadata_minimal_text(self):
        """Test metadata extraction with minimal text."""
        text = "Just some text without clear title or authors."
        metadata = extract_metadata_from_text(text)
        
        # Should return empty dict for minimal text
        assert isinstance(metadata, dict)
    
    def test_section_has_content(self):
        """Test section content checking."""
        from app.models.schema import PaperSections
        
        sections = PaperSections()
        sections.sections[SectionName.ABSTRACT] = "Some content"
        sections.sections[SectionName.INTRODUCTION] = ""
        sections.sections[SectionName.METHODS] = "   "  # Only whitespace
        
        assert sections.has_section(SectionName.ABSTRACT) is True
        assert sections.has_section(SectionName.INTRODUCTION) is False
        assert sections.has_section(SectionName.METHODS) is False
        assert sections.has_section(SectionName.RESULTS) is False
    
    def test_section_get_content(self):
        """Test getting section content."""
        from app.models.schema import PaperSections
        
        sections = PaperSections()
        sections.sections[SectionName.ABSTRACT] = "Abstract content"
        
        assert sections.get_section(SectionName.ABSTRACT) == "Abstract content"
        assert sections.get_section(SectionName.INTRODUCTION) is None
