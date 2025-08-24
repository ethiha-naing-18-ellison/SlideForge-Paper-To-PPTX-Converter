#!/usr/bin/env python3
"""
Debug script to test conclusion slide creation.
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.schema import PaperMetadata, SummarizedSection, SectionName, GenerationParams
from app.services.ppt.builder import build_presentation

def test_conclusion_creation():
    """Test conclusion slide creation."""
    
    print("Testing Conclusion Slide Creation")
    print("=" * 50)
    
    # Create metadata
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
    
    print(f"Metadata: {metadata.title}")
    print(f"Sections: {[s.name.value for s in sections]}")
    print(f"Target slides: {params.target_slide_count}")
    print()
    
    try:
        output_path = "debug_conclusion.pptx"
        pptx_path, slide_count = build_presentation(
            metadata, sections, "academic", output_path, params
        )
        
        print(f"✅ Created presentation: {pptx_path}")
        print(f"📊 Total slides: {slide_count}")
        
        # Check if file exists and has reasonable size
        file_size = Path(output_path).stat().st_size
        print(f"📁 File size: {file_size:,} bytes")
        
        # List expected slides
        expected_slides = [
            "Title slide",
            "Agenda slide", 
            "Abstract slide",
            "Introduction slide",
            "Conclusion slide (synthesized)",
            "References slide (if metadata has DOI/URL)"
        ]
        
        print(f"\nExpected slides: {len(expected_slides)}")
        for i, slide_name in enumerate(expected_slides, 1):
            print(f"  {i}. {slide_name}")
        
        print(f"\nActual slides created: {slide_count}")
        
        if slide_count >= 5:
            print("✅ Conclusion slide creation working!")
        else:
            print("❌ Conclusion slide creation not working as expected")
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conclusion_creation()
