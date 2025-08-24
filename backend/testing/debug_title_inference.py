#!/usr/bin/env python3
"""
Debug script to test title inference with sample paper content.
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import infer_title

def test_title_inference():
    """Test title inference with sample content."""
    
    # Read the sample paper content
    sample_file = Path("app/tests/samples/sample_paper.txt")
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_text = f.read()
    else:
        # Fallback sample text
        sample_text = """
        Title: Machine Learning Approaches for Natural Language Processing
        
        Authors: John Smith, Jane Doe, Robert Johnson
        
        Abstract
        This paper presents a comprehensive study of machine learning approaches...
        """
    
    print("Testing Title Inference")
    print("=" * 50)
    print(f"Sample text (first 200 chars): {sample_text[:200]}...")
    print()
    
    # Test 1: With metadata title
    print("1. Testing with metadata title:")
    result = infer_title(sample_text, meta_title="An Interesting Report")
    print(f"   Result: {result}")
    print()
    
    # Test 2: Without metadata title
    print("2. Testing without metadata title:")
    result = infer_title(sample_text, meta_title=None)
    print(f"   Result: {result}")
    print()
    
    # Test 3: With generic metadata title (should be rejected)
    print("3. Testing with generic metadata title:")
    result = infer_title(sample_text, meta_title="Research Paper")
    print(f"   Result: {result}")
    print()
    
    # Test 4: With empty text
    print("4. Testing with empty text:")
    result = infer_title("", meta_title=None)
    print(f"   Result: {result}")
    print()
    
    # Test 5: Check if "Title:" prefix is handled
    print("5. Checking if 'Title:' prefix is handled:")
    lines = sample_text.split('\n')
    for i, line in enumerate(lines[:5]):
        print(f"   Line {i+1}: {line}")
        if line.strip().lower().startswith('title:'):
            print(f"   Found 'Title:' prefix in line {i+1}")
            break

if __name__ == "__main__":
    test_title_inference()
