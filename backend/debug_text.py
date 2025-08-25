#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.extractor import extract_text_from_pdf

def debug_text():
    """Debug the extracted text to find section headers."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    try:
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        
        # Look for section headers
        lines = text.splitlines()
        print(f"\nTotal lines: {len(lines)}")
        
        print("\nLooking for section headers...")
        for i, line in enumerate(lines[:100]):  # Check first 100 lines
            line_stripped = line.strip()
            if line_stripped:
                # Look for potential section headers
                if (line_stripped.isupper() and len(line_stripped) > 3) or \
                   line_stripped.endswith(':') or \
                   line_stripped.startswith(('1.', '2.', '3.', '4.', '5.')) or \
                   any(keyword in line_stripped.upper() for keyword in ['INTRODUCTION', 'METHOD', 'RESULT', 'CONCLUSION', 'ABSTRACT']):
                    print(f"Line {i+1}: '{line_stripped}'")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_text()
