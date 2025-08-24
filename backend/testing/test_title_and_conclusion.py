import pytest
from pathlib import Path
import sys

# Add the app directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.services.extractor import infer_title
from app.models.schema import GenerationParams, DocumentType, PaperMetadata, SummarizedSection, SectionName
from app.services.ppt.builder import build_presentation


def test_infer_title_prefers_metadata():
    """Test that infer_title prefers metadata title when available."""
    txt = "foo\nbar"
    result = infer_title(txt, meta_title="An Interesting Report")
    assert result == "An Interesting Report"


def test_infer_title_from_text():
    """Test that infer_title can extract title from text when no metadata."""
    txt = "A Powerful Approach to Widgets\nJohn Doe\nAbstract\nThis work..."
    result = infer_title(txt, None)
    assert "Approach to Widgets" in result


def test_infer_title_rejects_generic_titles():
    """Test that infer_title rejects generic titles."""
    txt = "Some content here"
    result = infer_title(txt, meta_title="Research Paper")
    assert result != "Research Paper"
    assert "Some content" in result


def test_infer_title_handles_empty_input():
    """Test that infer_title handles empty input gracefully."""
    result = infer_title("", None)
    assert result is None


def test_document_type_enum():
    """Test DocumentType enum values."""
    assert DocumentType.RESEARCH_PAPER.value == "Research Paper"
    assert DocumentType.USER_MANUAL.value == "User Manual"
    assert DocumentType.PROJECT_REPORT.value == "Project Report"


def test_generation_params_defaults():
    """Test GenerationParams default values."""
    params = GenerationParams()
    assert params.doc_type == DocumentType.GENERAL_REPORT
    assert params.title_override is None
    assert params.target_slide_count == 20


def test_generation_params_custom():
    """Test GenerationParams with custom values."""
    params = GenerationParams(
        doc_type=DocumentType.USER_MANUAL,
        title_override="My Custom Title",
        target_slide_count=15
    )
    assert params.doc_type == DocumentType.USER_MANUAL
    assert params.title_override == "My Custom Title"
    assert params.target_slide_count == 15


def test_build_presentation_with_params():
    """Test that build_presentation accepts GenerationParams."""
    metadata = PaperMetadata(
        title="Test Document",
        authors=["John Doe"],
        venue="Test Conference",
        year=2024
    )
    
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=["This is a test abstract."]
        ),
        SummarizedSection(
            name=SectionName.INTRODUCTION,
            bullets=["This is an introduction."]
        )
    ]
    
    params = GenerationParams(
        doc_type=DocumentType.USER_MANUAL,
        title_override="Custom Title",
        target_slide_count=10
    )
    
    # This should not raise an exception
    try:
        output_path = "test_output_with_params.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path, params
        )
        assert slide_count >= 1  # Should have at least title slide
    except Exception as e:
        pytest.fail(f"build_presentation failed: {e}")


def test_build_presentation_without_params():
    """Test that build_presentation works without params (backward compatibility)."""
    metadata = PaperMetadata(
        title="Test Document",
        authors=["John Doe"],
        venue="Test Conference",
        year=2024
    )
    
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=["This is a test abstract."]
        )
    ]
    
    # This should not raise an exception
    try:
        output_path = "test_output_without_params.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path
        )
        assert slide_count >= 1  # Should have at least title slide
    except Exception as e:
        pytest.fail(f"build_presentation failed: {e}")


def test_conclusion_slide_creation():
    """Test that a conclusion slide is created when missing."""
    metadata = PaperMetadata(
        title="Test Document",
        authors=["John Doe"]
    )
    
    # Create sections without a conclusion
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=["Abstract point 1", "Abstract point 2"]
        ),
        SummarizedSection(
            name=SectionName.INTRODUCTION,
            bullets=["Intro point 1", "Intro point 2"]
        )
    ]
    
    params = GenerationParams(target_slide_count=5)
    
    try:
        output_path = "test_conclusion.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path, params
        )
        # Should have title + agenda + 2 sections + conclusion = 5 slides minimum
        # (No references slide since metadata has no DOI/URL)
        assert slide_count >= 5
    except Exception as e:
        pytest.fail(f"build_presentation with conclusion failed: {e}")


def test_title_override_functionality():
    """Test that title override works correctly."""
    metadata = PaperMetadata(
        title="Original Title",
        authors=["John Doe"]
    )
    
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=["Test content"]
        )
    ]
    
    params = GenerationParams(
        title_override="Overridden Title",
        doc_type=DocumentType.PROJECT_REPORT
    )
    
    try:
        output_path = "test_title_override.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path, params
        )
        assert slide_count >= 1
    except Exception as e:
        pytest.fail(f"build_presentation with title override failed: {e}")


def test_document_type_display():
    """Test that document type is properly displayed."""
    metadata = PaperMetadata(
        title="Test Document",
        authors=["John Doe"]
    )
    
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=["Test content"]
        )
    ]
    
    params = GenerationParams(
        doc_type=DocumentType.USER_MANUAL
    )
    
    try:
        output_path = "test_doc_type.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path, params
        )
        assert slide_count >= 1
    except Exception as e:
        pytest.fail(f"build_presentation with document type failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
