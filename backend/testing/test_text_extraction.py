#!/usr/bin/env python3
"""
Test script to check text extraction from sample PDF.
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import extract_text_from_pdf, infer_title

def test_text_extraction():
    """Test text extraction from sample PDF."""
    
    pdf_path = "app/tests/samples/sample_paper.pdf"
    
    if not Path(pdf_path).exists():
        print(f"PDF file not found: {pdf_path}")
        return
    
    print("Testing Text Extraction")
    print("=" * 50)
    
    # Extract text
    print("1. Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    print(f"   Text length: {len(text)} characters")
    print(f"   First 500 characters:")
    print(f"   {text[:500]}...")
    print()
    
    # Test title inference
    print("2. Testing title inference...")
    title = infer_title(text)
    print(f"   Inferred title: {title}")
    print()
    
    # Check for "Title:" prefix
    print("3. Checking for 'Title:' prefix...")
    lines = text.split('\n')
    for i, line in enumerate(lines[:10]):
        print(f"   Line {i+1}: {line}")
        if line.strip().lower().startswith('title:'):
            print(f"   Found 'Title:' prefix in line {i+1}")
            break

if __name__ == "__main__":
    test_text_extraction()
