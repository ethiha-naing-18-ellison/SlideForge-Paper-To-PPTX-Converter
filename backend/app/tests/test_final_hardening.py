"""Tests for final hardening features."""

from app.services.ppt.bullets_preprocess import preprocess_for_slide
from app.services.ppt.labels import strip_label_prefix
from app.services.ppt.sections import canonicalize, get_section_display_name

def test_preprocess_limits_and_numbers():
    """Test that preprocessing limits bullets and numbers methods correctly."""
    raw = ["Title: We propose a method; it improves accuracy by 10% on dataset A. Then we evaluate extensively."]
    bullets, list_type = preprocess_for_slide(raw, "METHODS", 18, 5, 2)
    assert 1 <= len(bullets) <= 5
    assert list_type == "numbered"
    assert all(len(b.split()) <= 19 for b in bullets)
    assert bullets[0].startswith("**")

def test_strip_labels():
    """Test that label prefixes are properly stripped."""
    assert strip_label_prefix("Title: Hello World") == "Hello World"
    assert strip_label_prefix("1. INTRODUCTION") == "INTRODUCTION"
    assert strip_label_prefix("Keywords: machine learning") == "machine learning"

def test_canonical_sections():
    """Test that section names are properly canonicalized."""
    assert canonicalize("METHODOLOGY") == "METHODS"
    assert canonicalize("RESULTS & DISCUSSION") == "RESULTS"
    assert canonicalize("INTRODUCTION") == "INTRODUCTION"
    assert get_section_display_name("METHODS") == "Methods"
