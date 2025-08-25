# -*- coding: utf-8 -*-
"""Debug script to analyze PDF sections."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.extractor import extract_text_from_pdf

def analyze_pdf_sections():
    """Analyze the PDF to find actual section headers."""
    pdf_path = "uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf"
    
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    # Clean the text
    text_clean = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    print(f"\nTotal text length: {len(text_clean)}")
    print(f"First 1000 characters:")
    print(text_clean[:1000])
    print("\n" + "="*80)
    
    # Look for section headers
    lines = text_clean.split('\n')
    print("\nAnalyzing lines for section headers...")
    
    section_headers = []
    for i, line in enumerate(lines[:100]):  # Check first 100 lines
        line_clean = line.strip()
        if line_clean:
            # Look for patterns that might be section headers
            if any(keyword in line_clean.upper() for keyword in [
                "ABSTRACT", "INTRODUCTION", "LITERATURE", "METHOD", "RESULT", 
                "DISCUSSION", "CONCLUSION", "REFERENCES", "BIBLIOGRAPHY"
            ]):
                section_headers.append((i, line_clean))
                print(f"Line {i}: {line_clean}")
    
    print(f"\nFound {len(section_headers)} potential section headers")
    
    # Also look for numbered sections
    print("\nLooking for numbered sections...")
    for i, line in enumerate(lines[:100]):
        line_clean = line.strip()
        if line_clean and any(line_clean.startswith(f"{j}.") for j in range(1, 10)):
            print(f"Line {i}: {line_clean}")
    
    return text_clean

if __name__ == "__main__":
    analyze_pdf_sections()
