"""Unit tests for PowerPoint builder."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.ppt.builder import build_presentation, BuildError
from app.models.schema import PaperMetadata, SummarizedSection, SectionName


class TestPPtBuilder:
    """Test cases for PowerPoint builder."""
    
    def test_build_presentation_basic(self, tmp_path):
        """Test basic presentation building."""
        # Create test data
        metadata = PaperMetadata(
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            venue="Test Conference",
            year=2023,
            doi="10.1234/test.2023",
            url=None,
            abstract="Test abstract"
        )
        
        sections = [
            SummarizedSection(
                name=SectionName.ABSTRACT,
                bullets=["This is the first bullet", "This is the second bullet"]
            ),
            SummarizedSection(
                name=SectionName.INTRODUCTION,
                bullets=["Introduction bullet 1", "Introduction bullet 2"]
            )
        ]
        
        output_path = tmp_path / "test_presentation.pptx"
        
        # Build presentation
        result_path, slide_count = build_presentation(
            metadata, sections, "academic", str(output_path)
        )
        
        # Verify results
        assert Path(result_path).exists()
        assert slide_count > 0
        assert slide_count >= 3  # Title + Agenda + at least one section
    
    def test_build_presentation_empty_sections(self, tmp_path):
        """Test presentation building with empty sections."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=[],
            venue=None,
            year=None,
            doi=None,
            url=None,
            abstract=None
        )
        
        sections = []
        output_path = tmp_path / "test_presentation.pptx"
        
        # Should still create title and agenda slides
        result_path, slide_count = build_presentation(
            metadata, sections, "academic", str(output_path)
        )
        
        assert Path(result_path).exists()
        assert slide_count >= 2  # At least title and agenda slides
    
    def test_build_presentation_different_themes(self, tmp_path):
        """Test presentation building with different themes."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=["Author 1"],
            venue="Test Conference",
            year=2023,
            doi=None,
            url=None,
            abstract=None
        )
        
        sections = [
            SummarizedSection(
                name=SectionName.ABSTRACT,
                bullets=["Test bullet"]
            )
        ]
        
        themes = ["academic", "minimal", "corporate"]
        
        for theme in themes:
            output_path = tmp_path / f"test_{theme}.pptx"
            result_path, slide_count = build_presentation(
                metadata, sections, theme, str(output_path)
            )
            
            assert Path(result_path).exists()
            assert slide_count > 0
    
    def test_build_presentation_invalid_theme(self, tmp_path):
        """Test presentation building with invalid theme."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=[],
            venue=None,
            year=None,
            doi=None,
            url=None,
            abstract=None
        )
        
        sections = []
        output_path = tmp_path / "test_presentation.pptx"
        
        # Should use default theme (academic)
        result_path, slide_count = build_presentation(
            metadata, sections, "invalid_theme", str(output_path)
        )
        
        assert Path(result_path).exists()
        assert slide_count > 0
    
    def test_build_presentation_with_references(self, tmp_path):
        """Test presentation building with DOI/URL for references slide."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=["Author 1"],
            venue="Test Conference",
            year=2023,
            doi="10.1234/test.2023",
            url="https://example.com/paper",
            abstract=None
        )
        
        sections = [
            SummarizedSection(
                name=SectionName.ABSTRACT,
                bullets=["Test bullet"]
            )
        ]
        
        output_path = tmp_path / "test_presentation.pptx"
        result_path, slide_count = build_presentation(
            metadata, sections, "academic", str(output_path)
        )
        
        assert Path(result_path).exists()
        # Should have more slides due to references slide
        assert slide_count >= 4  # Title + Agenda + Section + References
    
    def test_build_presentation_error_handling(self, tmp_path):
        """Test error handling in presentation building."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=[],
            venue=None,
            year=None,
            doi=None,
            url=None,
            abstract=None
        )
        
        sections = []
        output_path = tmp_path / "nonexistent" / "test_presentation.pptx"
        
        # Should raise BuildError for invalid path
        with pytest.raises(BuildError):
            build_presentation(metadata, sections, "academic", str(output_path))
    
    @patch('app.services.ppt.builder.Presentation')
    def test_apply_theme(self, mock_presentation_class):
        """Test theme application."""
        from app.services.ppt.builder import _apply_theme
        
        mock_prs = MagicMock()
        mock_presentation_class.return_value = mock_prs
        
        # Test different themes
        themes = ["academic", "minimal", "corporate"]
        
        for theme in themes:
            _apply_theme(mock_prs, theme)
            
            # Verify slide size is set
            assert mock_prs.slide_width is not None
            assert mock_prs.slide_height is not None
    
    def test_format_title(self):
        """Test title formatting."""
        from app.services.ppt.builder import _format_title
        
        # Mock title shape
        mock_title = MagicMock()
        mock_title.text_frame.paragraphs = [MagicMock()]
        
        _format_title(mock_title, "academic")
        
        # Verify formatting is applied
        paragraph = mock_title.text_frame.paragraphs[0]
        assert paragraph.font.size is not None
        assert paragraph.font.bold is True
    
    def test_format_subtitle(self):
        """Test subtitle formatting."""
        from app.services.ppt.builder import _format_subtitle
        
        # Mock subtitle shape
        mock_subtitle = MagicMock()
        mock_subtitle.text_frame.paragraphs = [MagicMock()]
        
        _format_subtitle(mock_subtitle, "academic")
        
        # Verify formatting is applied
        paragraph = mock_subtitle.text_frame.paragraphs[0]
        assert paragraph.font.size is not None
        assert paragraph.font.italic is True
    
    def test_format_content(self):
        """Test content formatting."""
        from app.services.ppt.builder import _format_content
        
        # Mock content shape
        mock_content = MagicMock()
        mock_content.text_frame.paragraphs = [MagicMock()]
        
        _format_content(mock_content, "academic")
        
        # Verify formatting is applied
        paragraph = mock_content.text_frame.paragraphs[0]
        assert paragraph.font.size is not None
    
    def test_create_title_slide(self):
        """Test title slide creation."""
        from app.services.ppt.builder import _create_title_slide
        
        # Mock presentation
        mock_prs = MagicMock()
        mock_slide = MagicMock()
        mock_prs.slides.add_slide.return_value = mock_slide
        
        # Mock slide layout
        mock_layout = MagicMock()
        mock_prs.slide_layouts = [mock_layout]
        
        # Mock shapes
        mock_title = MagicMock()
        mock_subtitle = MagicMock()
        mock_slide.shapes.title = mock_title
        mock_slide.placeholders = [None, mock_subtitle]
        
        metadata = PaperMetadata(
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            venue="Test Conference",
            year=2023,
            doi=None,
            url=None,
            abstract=None
        )
        
        slide_count = _create_title_slide(mock_prs, metadata, "academic")
        
        assert slide_count == 1
        assert mock_title.text == "Test Paper"
        assert "Author 1, Author 2" in mock_subtitle.text
        assert "Test Conference" in mock_subtitle.text
        assert "2023" in mock_subtitle.text
