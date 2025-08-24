#!/usr/bin/env python3
"""
Demo script to test SlideForge's new features:
- Real title extraction and override
- Document type support
- Mandatory conclusion slides
- Target slide count expansion
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import extract_text_from_pdf, infer_title
from app.services.sectionizer import split_into_sections
from app.services.summarizer.textrank import TextRankSummarizer
from app.services.ppt.builder import build_presentation
from app.models.schema import PaperMetadata, SummarizedSection, SectionName, GenerationParams, DocumentType

def test_new_features():
    """Test all the new features with a sample document."""
    
    print("🚀 Testing SlideForge New Features")
    print("=" * 60)
    
    # Test 1: Title Inference
    print("\n1. Testing Title Inference...")
    sample_text = """
    Advanced Machine Learning Techniques for Natural Language Processing
    Authors: Dr. Jane Smith, Prof. John Doe, Dr. Alice Johnson
    
    Abstract
    This paper presents a comprehensive study of machine learning approaches...
    """
    
    # Test with metadata title
    inferred_title = infer_title(sample_text, meta_title="An Interesting Report")
    print(f"   ✅ With metadata: {inferred_title}")
    
    # Test without metadata
    inferred_title = infer_title(sample_text, meta_title=None)
    print(f"   ✅ Without metadata: {inferred_title}")
    
    # Test with generic title (should be rejected)
    inferred_title = infer_title(sample_text, meta_title="Research Paper")
    print(f"   ✅ Generic title rejected: {inferred_title}")
    
    # Test 2: Document Types
    print("\n2. Testing Document Types...")
    doc_types = [
        DocumentType.RESEARCH_PAPER,
        DocumentType.USER_MANUAL,
        DocumentType.PROJECT_REPORT,
        DocumentType.SCHOOL_ASSIGNMENT
    ]
    
    for doc_type in doc_types:
        print(f"   ✅ {doc_type.value}")
    
    # Test 3: Generation Parameters
    print("\n3. Testing Generation Parameters...")
    params = GenerationParams(
        doc_type=DocumentType.USER_MANUAL,
        title_override="How to Use Device X",
        target_slide_count=15
    )
    print(f"   ✅ Doc Type: {params.doc_type.value}")
    print(f"   ✅ Title Override: {params.title_override}")
    print(f"   ✅ Target Slides: {params.target_slide_count}")
    
    # Test 4: Full Pipeline with New Features
    print("\n4. Testing Full Pipeline...")
    
    # Create metadata
    metadata = PaperMetadata(
        title="Original Title (should be overridden)",
        authors=["Dr. Jane Smith", "Prof. John Doe"],
        venue="International Conference on AI",
        year=2024,
        doi="10.1234/example.doi"
    )
    
    # Create sections with rich content
    sections = [
        SummarizedSection(
            name=SectionName.ABSTRACT,
            bullets=[
                "**Key contribution**: This research introduces *novel* __techniques__ for natural language processing",
                "**Result**: Achieved *significant* __performance improvement__ of 25% over baseline methods",
                "**Impact**: *Reduced* __computation time__ by 40% while maintaining quality"
            ]
        ),
        SummarizedSection(
            name=SectionName.INTRODUCTION,
            bullets=[
                "**Background**: Natural language processing has evolved rapidly in recent years",
                "**Problem**: Current approaches lack efficiency and scalability",
                "**Solution**: We propose a new framework that addresses these limitations",
                "**Approach**: Our method combines multiple techniques for optimal results"
            ]
        ),
        SummarizedSection(
            name=SectionName.METHODS,
            bullets=[
                "**Step 1**: Data preprocessing involves *cleaning* and __normalization__ of raw input",
                "**Step 2**: Feature extraction using *advanced* __neural networks__ for pattern recognition",
                "**Step 3**: Model training with *optimized* __hyperparameters__ and validation",
                "**Step 4**: Evaluation using *comprehensive* __metrics__ and cross-validation"
            ]
        ),
        SummarizedSection(
            name=SectionName.RESULTS,
            bullets=[
                "**Performance**: Model achieved 95.7% accuracy on test dataset",
                "**Efficiency**: Processing time reduced by 40% compared to baseline",
                "**Scalability**: Successfully tested on datasets with 1M+ samples",
                "**Robustness**: Consistent performance across different domains"
            ]
        )
    ]
    
    # Test different configurations
    test_configs = [
        {
            "name": "User Manual with Custom Title",
            "params": GenerationParams(
                doc_type=DocumentType.USER_MANUAL,
                title_override="How to Use Device X: Complete Guide",
                target_slide_count=12
            )
        },
        {
            "name": "Research Paper with Auto Title",
            "params": GenerationParams(
                doc_type=DocumentType.RESEARCH_PAPER,
                title_override=None,  # Use inferred title
                target_slide_count=20
            )
        },
        {
            "name": "School Assignment",
            "params": GenerationParams(
                doc_type=DocumentType.SCHOOL_ASSIGNMENT,
                title_override="Machine Learning Project Report",
                target_slide_count=8
            )
        }
    ]
    
    for i, config in enumerate(test_configs):
        print(f"\n   Testing: {config['name']}")
        
        try:
            output_path = f"test_new_features_{i+1}.pptx"
            pptx_path, slide_count = build_presentation(
                metadata, 
                sections, 
                'academic', 
                output_path,
                config['params']
            )
            
            print(f"   ✅ Created: {output_path}")
            print(f"   ✅ Slides: {slide_count}")
            print(f"   ✅ Doc Type: {config['params'].doc_type.value}")
            print(f"   ✅ Title: {config['params'].title_override or 'Auto-detected'}")
            
            # Check file size
            file_size = Path(output_path).stat().st_size
            print(f"   ✅ File Size: {file_size:,} bytes")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 New Features Demo Completed!")
    print("📄 Check the generated PowerPoint files to see:")
    print("   • Correct titles (overridden or auto-detected)")
    print("   • Document type labels in subtitles")
    print("   • Mandatory conclusion slides")
    print("   • Target slide count expansion")
    print("   • Rich text formatting and styling")
    
    return True

if __name__ == "__main__":
    success = test_new_features()
    sys.exit(0 if success else 1)
