#!/usr/bin/env python3
"""
End-to-end test script for SlideForge
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import extract_text_from_pdf
from app.services.sectionizer import split_into_sections
from app.services.summarizer.textrank import TextRankSummarizer
from app.services.ppt.builder import build_presentation
from app.models.schema import PaperMetadata, SummarizedSection

def test_end_to_end():
    """Test the complete pipeline from PDF to PowerPoint."""
    
    print("🚀 Testing SlideForge End-to-End Pipeline")
    print("=" * 50)
    
    # Step 1: Extract text from PDF
    print("1. Extracting text from PDF...")
    try:
        text = extract_text_from_pdf('app/tests/samples/sample_paper.pdf')
        print(f"   ✅ Extracted {len(text)} characters")
        print(f"   📄 First 200 chars: {text[:200]}...")
    except Exception as e:
        print(f"   ❌ Text extraction failed: {e}")
        return False
    
    # Step 2: Split into sections
    print("\n2. Splitting text into sections...")
    try:
        sections = split_into_sections(text)
        print(f"   ✅ Found {len(sections.sections)} sections:")
        for name, content in sections.sections.items():
            print(f"      - {name.value}: {len(content)} chars")
    except Exception as e:
        print(f"   ❌ Section splitting failed: {e}")
        return False
    
    # Step 3: Summarize sections
    print("\n3. Summarizing sections...")
    try:
        summarizer = TextRankSummarizer()
        summarized_sections = []
        
        for name, content in sections.sections.items():
            bullets = summarizer.summarize_section(content, max_bullets=6)
            if bullets:
                summarized_sections.append(SummarizedSection(name=name, bullets=bullets))
                print(f"   ✅ {name.value}: {len(bullets)} bullets")
            else:
                print(f"   ⚠️  {name.value}: No bullets generated")
        
        print(f"   📊 Total summarized sections: {len(summarized_sections)}")
    except Exception as e:
        print(f"   ❌ Summarization failed: {e}")
        return False
    
    # Step 4: Create metadata
    print("\n4. Creating presentation metadata...")
    try:
        metadata = PaperMetadata(
            title="Machine Learning Approaches for Natural Language Processing",
            authors=["John Smith", "Jane Doe", "Robert Johnson"],
            venue="International Conference on AI",
            year=2024,
            doi="10.1234/example.doi",
            url="https://example.com/paper"
        )
        print(f"   ✅ Created metadata for: {metadata.title}")
    except Exception as e:
        print(f"   ❌ Metadata creation failed: {e}")
        return False
    
    # Step 5: Build PowerPoint
    print("\n5. Building PowerPoint presentation...")
    try:
        output_path = 'test_output.pptx'
        pptx_path, slide_count = build_presentation(
            metadata, 
            summarized_sections, 
            'academic', 
            output_path
        )
        print(f"   ✅ Created presentation: {pptx_path}")
        print(f"   📊 Total slides: {slide_count}")
        
        # Check if file exists and has reasonable size
        file_size = Path(output_path).stat().st_size
        print(f"   📁 File size: {file_size:,} bytes")
        
        if file_size > 1000:  # Should be at least 1KB
            print("   ✅ File size looks reasonable")
        else:
            print("   ⚠️  File size seems small")
            
    except Exception as e:
        print(f"   ❌ PowerPoint creation failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 End-to-end test completed successfully!")
    print(f"📄 Output file: {output_path}")
    print("💡 You can now open the PowerPoint file to verify the results.")
    
    return True

if __name__ == "__main__":
    success = test_end_to_end()
    sys.exit(0 if success else 1)
