#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.extractor import extract_text_from_pdf
from app.services.ppt.simple_sections import map_sections_by_content

def test_section_mapping():
    """Test the simple section mapper."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    try:
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(text)} characters")
        
        # Test section mapping
        print("\nMapping sections...")
        sections = map_sections_by_content(text)
        
        print(f"\nFound {len(sections)} sections:")
        for section_name, section_text in sections.items():
            print(f"\n{section_name}:")
            print(f"  Length: {len(section_text)} characters")
            print(f"  Preview: {section_text[:200]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_section_mapping()
