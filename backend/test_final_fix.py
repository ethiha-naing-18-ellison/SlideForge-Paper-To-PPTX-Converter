# -*- coding: utf-8 -*-
"""Test script to verify the final fixes."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.extractor import extract_text_from_pdf
from app.services.ppt.simple_sections import map_sections_by_content
from app.services.ppt.cleantext import normalize_text
from app.nlp.abstractive import compress_sentence_simple

def test_fixes():
    """Test the fixes for ellipsis and grammar issues."""
    
    # Test the abstractive compression
    test_text = "The culture of cloud computing is increasing day by day because onsite education requires a huge amount of infrastructure and most education institutes are unable to bear the cost of such resources"
    compressed = compress_sentence_simple(test_text, 35)
    print(f"Original: {test_text}")
    print(f"Compressed: {compressed}")
    print(f"Ends with ellipsis: {compressed.endswith('…')}")
    print()
    
    # Test grammar fixes
    test_grammar = "LITERATURE REVIEWThe culture of cloud computing is increasing day by day because onsite education requires a huge amount of infrastructure"
    fixed = normalize_text(test_grammar)
    print(f"Original grammar: {test_grammar}")
    print(f"Fixed grammar: {fixed}")
    print()
    
    # Test more grammar fixes
    test_grammar2 = "Due tothe nature of the flexible environment of cloud computing for business"
    fixed2 = normalize_text(test_grammar2)
    print(f"Original grammar2: {test_grammar2}")
    print(f"Fixed grammar2: {fixed2}")
    print()
    
    # Test PDF extraction and section mapping
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    print("Mapping sections...")
    sections = map_sections_by_content(text)
    
    print(f"\nFound {len(sections)} sections:")
    for section_name, content in sections.items():
        print(f"\n{section_name}:")
        print(f"  Content length: {len(content)} characters")
        # Test a sample of the content
        sample = content[:200]
        fixed_sample = normalize_text(sample)
        print(f"  Sample (original): {sample}")
        print(f"  Sample (fixed): {fixed_sample}")
    
    return sections

if __name__ == "__main__":
    test_fixes()
