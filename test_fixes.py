#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script to verify formatting fixes."""

from app.services.ppt.sections import canonicalize, clean_section_title, get_section_display_name
from app.services.ppt.cleantext import normalize_text, remove_raw_markdown
from app.services.ppt.bullets_preprocess import sanitize_lines

def test_section_cleaning():
    """Test section title cleaning."""
    print("Testing section title cleaning...")
    
    # Test problematic titles
    test_titles = [
        "Other — Introduction",
        "Additional Information — Methods",
        "**Bold Title**",
        "*Italic Title*",
        "__Underlined Title__",
        "Methods — Key terms: algorithm, data",
    ]
    
    for title in test_titles:
        cleaned = clean_section_title(title)
        print(f"  '{title}' -> '{cleaned}'")
    
    print()

def test_text_normalization():
    """Test text normalization."""
    print("Testing text normalization...")
    
    test_texts = [
        "This is **bold** text",
        "This has *italic* formatting",
        "This contains __underline__",
        "Text with  extra   spaces",
        "Text with — Key terms: term1, term2",
    ]
    
    for text in test_texts:
        normalized = normalize_text(text)
        print(f"  '{text}' -> '{normalized}'")
    
    print()

def test_bullet_sanitization():
    """Test bullet sanitization."""
    print("Testing bullet sanitization...")
    
    test_bullets = [
        "This is a normal bullet point",
        "This bullet has — Key terms: term1, term2",
        "Title: This is a labeled bullet",
        "1. This is a numbered bullet",
        "**Bold** bullet with markdown",
    ]
    
    sanitized = sanitize_lines(test_bullets)
    for i, bullet in enumerate(sanitized):
        print(f"  '{test_bullets[i]}' -> '{bullet}'")
    
    print()

if __name__ == "__main__":
    test_section_cleaning()
    test_text_normalization()
    test_bullet_sanitization()
    print("✅ All tests completed!")
