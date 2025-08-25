# -*- coding: utf-8 -*-
"""Simple test script to verify the fixes."""

import re

def normalize_text_simple(s: str) -> str:
    """Simple version of normalize_text without pptx dependency."""
    if not s:
        return ""
    s = s.strip()
    
    # Remove weird Unicode characters
    s = re.sub(r"[\u200b-\u200f\u202a-\u202e]", "", s)
    
    # Fix common grammar issues
    s = re.sub(r"(\w)([A-Z][a-z])", r"\1 \2", s)  # Add space between camelCase
    s = re.sub(r"(\w)(\d)", r"\1 \2", s)  # Add space between word and number
    s = re.sub(r"(\d)([A-Za-z])", r"\1 \2", s)  # Add space between number and word
    
    # Fix specific issues from the PDF
    s = s.replace("Proposed ModelHRbSBM", "Proposed Model HRbSBM")
    s = s.replace("This proposedmodel", "This proposed model")
    s = s.replace("Hand Recognition Based", "Hand Recognition-Based")
    
    # Fix more specific spacing issues found in the output
    s = s.replace("LITERATURE REVIEWThe", "LITERATURE REVIEW The")
    s = s.replace("Due tothe", "Due to the")
    s = s.replace("Due toits", "Due to its")
    s = s.replace("In thecurrent", "In the current")
    s = s.replace("thecurrent", "the current")
    s = s.replace("toits", "to its")
    s = s.replace("tothe", "to the")
    
    return s

def compress_sentence_simple(text: str, max_words: int = 35) -> str:
    words = text.split()
    if len(words) <= max_words: 
        return text.strip()
    # Return complete words without ellipsis
    return " ".join(words[:max_words])

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
    fixed = normalize_text_simple(test_grammar)
    print(f"Original grammar: {test_grammar}")
    print(f"Fixed grammar: {fixed}")
    print()
    
    # Test more grammar fixes
    test_grammar2 = "Due tothe nature of the flexible environment of cloud computing for business"
    fixed2 = normalize_text_simple(test_grammar2)
    print(f"Original grammar2: {test_grammar2}")
    print(f"Fixed grammar2: {fixed2}")
    print()
    
    # Test more examples from the image
    test_grammar3 = "Due toits flexible infrastructure, a user can access his/her information when and where required because the"
    fixed3 = normalize_text_simple(test_grammar3)
    print(f"Original grammar3: {test_grammar3}")
    print(f"Fixed grammar3: {fixed3}")
    print()
    
    test_grammar4 = "In thecurrent era the significance of cloud computing environment is habitual as well as addict the"
    fixed4 = normalize_text_simple(test_grammar4)
    print(f"Original grammar4: {test_grammar4}")
    print(f"Fixed grammar4: {fixed4}")
    print()

if __name__ == "__main__":
    test_fixes()
