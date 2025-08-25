#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.extractor import extract_text_from_pdf, resolve_title
from app.services.ppt.builder import init_presentation
from app.services.ppt.titleblock import create_clean_title_slide
from app.models.schema import LayoutConfig

def test_title_slide():
    """Test title slide creation."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    try:
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        
        # Resolve title
        title = resolve_title(text)
        print(f"Resolved title: '{title}'")
        
        # Create presentation
        layout = LayoutConfig()
        prs, layout = init_presentation(layout)
        
        # Create title slide
        print("Creating title slide...")
        slide = create_clean_title_slide(prs, layout, title, "Research Paper", authors=None)
        
        # Check what's on the slide
        print("Checking slide content...")
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame') and shape.text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    text_content = paragraph.text.strip()
                    if text_content:
                        print(f"Found text: '{text_content}'")
        
        # Save for inspection
        prs.save("test_title_slide.pptx")
        print("Saved test_title_slide.pptx for inspection")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_title_slide()
