# -*- coding: utf-8 -*-
"""Test script for the enhanced content generator with detailed content."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.nlp.simple_content_generator import SimpleContentGenerator

def test_enhanced_content_generator():
    """Test the enhanced content generator with detailed content."""
    
    # Sample text with more implementation details
    sample_text = """
    The culture of cloud computing is increasing day by day because onsite education requires a huge amount of infrastructure, and most education institutes are unable to bear the cost of such resources. Due to the nature of the flexible environment of cloud computing for business, Information Technology and the availability of other required resources like automated systems and open-source software to push the users to adapt this environment. Due to its flexible infrastructure, a user can access his/her information when and where required because the working environment is not limited at home or the office. In the current era the significance of cloud computing environment is habitual as well as addict the user to use the cloud services, due to its comfortable nature and user can assess his data when and where required. The implementation process involves several key steps including system design, technology selection, development, testing, and deployment. Operating System Compatibility was a crucial consideration given that our development environment runs on Windows 11. The system architecture consists of multiple components including the frontend interface, backend processing engine, database management system, and cloud integration layer. We utilized modern development tools and frameworks such as Python for backend development, React for frontend interface, and AWS for cloud infrastructure. The data collection process involved gathering requirements from educational institutions, analyzing existing systems, and identifying key performance indicators. The algorithm design incorporates machine learning techniques for gesture recognition and real-time processing capabilities. Performance optimization was achieved through efficient data structures, caching mechanisms, and parallel processing techniques. Security measures include encryption, authentication, and access control mechanisms to ensure data protection and system reliability.
    """
    
    # Initialize the content generator
    generator = SimpleContentGenerator()
    
    print("Testing Enhanced Content Generator with Detailed Information")
    print("=" * 70)
    
    # Test different sections
    sections = ["ABSTRACT", "INTRODUCTION", "LITERATURE", "METHODS", "RESULTS", "DISCUSSION", "CONCLUSION"]
    
    for section in sections:
        print(f"\n{section} Section:")
        print("-" * 40)
        
        bullets = generator.generate_section_content(
            section_name=section,
            raw_text=sample_text,
            target_bullets=8  # Increased target for more content
        )
        
        for i, bullet in enumerate(bullets, 1):
            print(f"{i}. {bullet}")
            print(f"   Length: {len(bullet.split())} words")
            print()
    
    print("\n" + "=" * 70)
    print("Enhanced content generation test completed!")

if __name__ == "__main__":
    test_enhanced_content_generator()
