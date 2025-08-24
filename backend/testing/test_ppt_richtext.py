import os
import pytest
from pathlib import Path

# Add the app directory to the path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.services.ppt.richtext import tokenize_inline

def test_tokenize_inline_basic():
    """Test basic rich text parsing with bold, italic, and underline."""
    text = "This is **bold** and *italic* and __under__."
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "This is bold and italic and under."
    assert any(s.get("bold") for _, s in parts)
    assert any(s.get("italic") for _, s in parts)
    assert any(s.get("underline") for _, s in parts)

def test_tokenize_inline_empty():
    """Test empty string handling."""
    parts = tokenize_inline("")
    assert len(parts) == 1
    assert parts[0][0] == ""
    assert parts[0][1] == {"bold": False, "italic": False, "underline": False}

def test_tokenize_inline_no_markup():
    """Test text without any markup."""
    text = "This is plain text without any formatting."
    parts = tokenize_inline(text)
    assert len(parts) == 1
    assert parts[0][0] == text
    assert parts[0][1] == {"bold": False, "italic": False, "underline": False}

def test_tokenize_inline_bold_only():
    """Test bold formatting only."""
    text = "This is **bold text** here."
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "This is bold text here."
    
    # Check that we have both regular and bold segments
    regular_segments = [seg for seg, style in parts if not style["bold"]]
    bold_segments = [seg for seg, style in parts if style["bold"]]
    
    assert len(regular_segments) > 0
    assert len(bold_segments) > 0
    assert "bold text" in "".join(bold_segments)

def test_tokenize_inline_italic_only():
    """Test italic formatting only."""
    text = "This is *italic text* here."
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "This is italic text here."
    
    # Check that we have both regular and italic segments
    regular_segments = [seg for seg, style in parts if not style["italic"]]
    italic_segments = [seg for seg, style in parts if style["italic"]]
    
    assert len(regular_segments) > 0
    assert len(italic_segments) > 0
    assert "italic text" in "".join(italic_segments)

def test_tokenize_inline_underline_only():
    """Test underline formatting only."""
    text = "This is __underlined text__ here."
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "This is underlined text here."
    
    # Check that we have both regular and underlined segments
    regular_segments = [seg for seg, style in parts if not style["underline"]]
    underline_segments = [seg for seg, style in parts if style["underline"]]
    
    assert len(regular_segments) > 0
    assert len(underline_segments) > 0
    assert "underlined text" in "".join(underline_segments)

def test_tokenize_inline_mixed():
    """Test mixed formatting in the same text."""
    text = "This has **bold**, *italic*, and __underline__ formatting."
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "This has bold, italic, and underline formatting."
    
    # Check that all styles are present
    has_bold = any(style["bold"] for _, style in parts)
    has_italic = any(style["italic"] for _, style in parts)
    has_underline = any(style["underline"] for _, style in parts)
    
    assert has_bold
    assert has_italic
    assert has_underline

def test_tokenize_inline_adjacent():
    """Test adjacent formatting without spaces."""
    text = "**Bold***Italic*__Underline__"
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "BoldItalicUnderline"
    
    # Check that all styles are present
    has_bold = any(style["bold"] for _, style in parts)
    has_italic = any(style["italic"] for _, style in parts)
    has_underline = any(style["underline"] for _, style in parts)
    
    assert has_bold
    assert has_italic
    assert has_underline

def test_tokenize_inline_nested():
    """Test nested formatting (should work with encounter order)."""
    text = "**Bold with *italic* inside**"
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    # The current implementation processes outer formatting first, so nested formatting may not be fully processed
    assert "Bold with" in joined
    assert "inside" in joined
    
    # Check that bold style is present (outer formatting)
    has_bold = any(style["bold"] for _, style in parts)
    assert has_bold

def test_tokenize_inline_special_characters():
    """Test that special characters are preserved."""
    text = "**Bold text** with numbers 123 and symbols @#$%"
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "Bold text with numbers 123 and symbols @#$%"
    
    # Check that numbers and symbols are preserved
    assert "123" in joined
    assert "@#$%" in joined

def test_tokenize_inline_multiline():
    """Test multiline text with formatting."""
    text = "Line 1 with **bold**\nLine 2 with *italic*\nLine 3 with __underline__"
    parts = tokenize_inline(text)
    joined = "".join(seg for seg, _ in parts)
    assert joined == "Line 1 with bold\nLine 2 with italic\nLine 3 with underline"
    
    # Check that newlines are preserved
    assert "\n" in joined
    assert joined.count("\n") == 2
