#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.extractor import extract_text_from_pdf, resolve_title

def test_title_resolution():
    """Test title resolution."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    try:
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        
        # Test title resolution
        print("\nTesting title resolution...")
        title = resolve_title(text)
        print(f"Resolved title: '{title}'")
        
        # Check if the actual title is in the text
        actual_title = "A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System"
        if actual_title in text:
            print(f"✓ Actual title found in text")
        else:
            print(f"✗ Actual title NOT found in text")
            
        # Check first 500 characters
        print(f"\nFirst 500 characters:")
        print(text[:500])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_title_resolution()
