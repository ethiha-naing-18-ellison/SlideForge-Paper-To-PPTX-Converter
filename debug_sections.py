#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.services.extractor import extract_text_from_pdf

# Extract text
text = extract_text_from_pdf('../backend/uploads/A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf')

# Find section headers
lines = text.splitlines()
section_headers = []

for i, line in enumerate(lines):
    if any(keyword in line.upper() for keyword in ['INTRODUCTION', 'METHODOLOGY', 'RESULTS', 'CONCLUSION', 'LITERATURE']):
        print(f"Line {i+1}: \"{line}\"")
        section_headers.append((i+1, line))

print(f"\nFound {len(section_headers)} potential section headers")
