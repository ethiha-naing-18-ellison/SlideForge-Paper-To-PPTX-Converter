#!/usr/bin/env python3
"""
Script to create a sample PDF for testing SlideForge
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pathlib import Path

def create_sample_pdf():
    """Create a sample PDF from the text file"""
    
    # Read the sample text
    text_file = Path("app/tests/samples/sample_paper.txt")
    output_file = Path("app/tests/samples/sample_paper.pdf")
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(str(output_file), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Split content into sections
    sections = content.split('\n\n')
    
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            if len(lines) == 1 and not lines[0].startswith(' '):
                # This is a title or heading
                if 'Title:' in lines[0]:
                    title = lines[0].replace('Title:', '').strip()
                    story.append(Paragraph(title, title_style))
                elif 'Authors:' in lines[0]:
                    authors = lines[0].replace('Authors:', '').strip()
                    story.append(Paragraph(f"<b>Authors:</b> {authors}", normal_style))
                else:
                    story.append(Paragraph(lines[0], heading_style))
            else:
                # This is content
                text = ' '.join(lines)
                story.append(Paragraph(text, normal_style))
            
            story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"Sample PDF created: {output_file}")

if __name__ == "__main__":
    create_sample_pdf()
