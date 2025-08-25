# -*- coding: utf-8 -*-
"""Test script for the simple content generator."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.nlp.simple_content_generator import SimpleContentGenerator

def test_simple_content_generator():
    """Test the simple content generator with sample text."""
    
    # Sample text from the Literature Review section
    sample_text = """
    The culture of cloud computing is increasing day by day because onsite education requires a huge amount of infrastructure, and most education institutes are unable to bear the cost of such resources. Due to the nature of the flexible environment of cloud computing for business, Information Technology and the availability of other required resources like automated systems and open-source software to push the users to adapt this environment. Due to its flexible infrastructure, a user can access his/her information when and where required because the working environment is not limited at home or the office. In the current era the significance of cloud computing environment is habitual as well as addict the user to use the cloud services, due to its comfortable nature and user can assess his data when and where required.
    """
    
    # Initialize the content generator
    generator = SimpleContentGenerator()
    
    print("Testing Simple Content Generator")
    print("=" * 50)
    
    # Test different sections
    sections = ["ABSTRACT", "INTRODUCTION", "LITERATURE", "METHODS", "RESULTS", "DISCUSSION", "CONCLUSION"]
    
    for section in sections:
        print(f"\n{section} Section:")
        print("-" * 30)
        
        bullets = generator.generate_section_content(
            section_name=section,
            raw_text=sample_text,
            target_bullets=4
        )
        
        for i, bullet in enumerate(bullets, 1):
            print(f"{i}. {bullet}")
    
    print("\n" + "=" * 50)
    print("Content generation test completed!")

if __name__ == "__main__":
    test_simple_content_generator()
