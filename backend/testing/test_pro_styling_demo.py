#!/usr/bin/env python3
"""
Demo script to showcase SlideForge Pro Styling features
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import extract_text_from_pdf
from app.services.sectionizer import split_into_sections
from app.services.summarizer.textrank import TextRankSummarizer
from app.services.ppt.builder import build_presentation
from app.models.schema import PaperMetadata, SummarizedSection, SectionName, RenderOptions, StylePalette

def test_pro_styling_features():
    """Test pro styling features with rich text and different list types."""
    
    print("🎨 Testing SlideForge Pro Styling Features")
    print("=" * 60)
    
    # Create metadata
    metadata = PaperMetadata(
        title="Advanced Machine Learning Techniques with Rich Text Formatting",
        authors=["Dr. Jane Smith", "Prof. John Doe", "Dr. Alice Johnson"],
        venue="International Conference on Artificial Intelligence",
        year=2024,
        doi="10.1234/example.doi",
        url="https://example.com/paper"
    )
    
    # Create sections with rich text formatting to showcase features
    sections = [
        SummarizedSection(
            name=SectionName.METHODS,
            bullets=[
                "**Step 1**: Data preprocessing involves *cleaning* and __normalization__ of raw input data",
                "**Step 2**: Feature extraction using *advanced* __neural networks__ for pattern recognition",
                "**Step 3**: Model training with *optimized* __hyperparameters__ and validation techniques",
                "**Step 4**: Evaluation using *comprehensive* __metrics__ and cross-validation procedures"
            ]
        ),
        SummarizedSection(
            name=SectionName.RESULTS,
            bullets=[
                "**Key contribution**: Achieved *significant* __performance improvement__ of 25% over baseline",
                "**Result**: Model accuracy reached *outstanding* __95.7%__ on test dataset",
                "**Impact**: *Reduced* __computation time__ by 40% while maintaining quality",
                "**Limitation**: *Current* __approach__ requires substantial computational resources"
            ]
        ),
        SummarizedSection(
            name=SectionName.DISCUSSION,
            bullets=[
                "The *superior* __performance__ can be attributed to **innovative** architecture design",
                "**Future work** should focus on *scaling* __efficiency__ and **optimization** techniques",
                "**Key contribution** of this research lies in *novel* __methodology__ and **practical** applications",
                "**Limitation** includes *resource* __requirements__ and **complexity** of implementation"
            ]
        ),
        SummarizedSection(
            name=SectionName.CONCLUSION,
            bullets=[
                "**Summary**: *Comprehensive* __analysis__ demonstrates **significant** improvements",
                "**Impact**: *Practical* __applications__ show **promising** results for real-world deployment",
                "**Future work**: *Further* __research__ needed for **scalability** and **efficiency** optimization"
            ]
        )
    ]
    
    print(f"📊 Created {len(sections)} sections with rich text formatting")
    total_bullets = sum(len(section.bullets) for section in sections)
    print(f"📝 Total bullets: {total_bullets}")
    
    # Build presentation with pro styling
    print("\n🔨 Building presentation with pro styling features...")
    output_path = 'pro_styling_demo.pptx'
    
    try:
        pptx_path, slide_count = build_presentation(
            metadata, 
            sections, 
            'academic', 
            output_path
        )
        
        print(f"✅ Created presentation: {pptx_path}")
        print(f"📊 Total slides: {slide_count}")
        
        # Check if file exists and has reasonable size
        file_size = Path(output_path).stat().st_size
        print(f"📁 File size: {file_size:,} bytes")
        
        if file_size > 1000:
            print("✅ File size looks reasonable")
        else:
            print("⚠️  File size seems small")
            
        print(f"\n🎨 Pro Styling Features Applied:")
        print(f"   • Methods section: Numbered lists with emphasized first words")
        print(f"   • Results section: Bullet points with keyword highlighting")
        print(f"   • Rich text formatting: **bold**, *italic*, __underline__")
        print(f"   • Color-coded keywords: Blue for key terms")
        print(f"   • Auto-pagination: Content split across slides if needed")
        print(f"   • Placeholder-free: No 'Click to add' text")
        
        if slide_count > len(sections):
            print(f"   • Pagination occurred: {slide_count - len(sections)} additional slides created")
        else:
            print(f"   • All content fit on original slides")
            
    except Exception as e:
        print(f"❌ PowerPoint creation failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Pro styling demo completed successfully!")
    print(f"📄 Output file: {output_path}")
    print("💡 Open the PowerPoint file to see the rich text formatting and styling.")
    print("   • Methods should have numbered lists with bold first words")
    print("   • Results should have bullet points with colored keywords")
    print("   • All text should have proper formatting (bold, italic, underline)")
    
    return True

if __name__ == "__main__":
    success = test_pro_styling_features()
    sys.exit(0 if success else 1)
