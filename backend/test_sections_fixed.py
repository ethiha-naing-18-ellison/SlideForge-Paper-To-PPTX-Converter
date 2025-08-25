# -*- coding: utf-8 -*-
"""Test script to verify the fixed section mapping."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.extractor import extract_text_from_pdf
from app.services.ppt.simple_sections import map_sections_by_content

def test_section_mapping():
    """Test the section mapping with the actual PDF."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    print("Mapping sections...")
    sections = map_sections_by_content(text)
    
    print(f"\nFound {len(sections)} sections:")
    for section_name, content in sections.items():
        print(f"\n{section_name}:")
        print(f"  Content length: {len(content)} characters")
        print(f"  First 200 chars: {content[:200]}...")
    
    return sections

if __name__ == "__main__":
    test_section_mapping()
