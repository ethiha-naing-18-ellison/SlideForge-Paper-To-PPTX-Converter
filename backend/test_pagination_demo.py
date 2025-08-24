#!/usr/bin/env python3
"""
Demo script to test SlideForge pagination with long content
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.extractor import extract_text_from_pdf
from app.services.sectionizer import split_into_sections
from app.services.summarizer.textrank import TextRankSummarizer
from app.services.ppt.builder import build_presentation
from app.models.schema import PaperMetadata, SummarizedSection, SectionName

def test_pagination_with_long_content():
    """Test pagination with artificially long content."""
    
    print("🧪 Testing SlideForge Pagination with Long Content")
    print("=" * 60)
    
    # Create metadata
    metadata = PaperMetadata(
        title="Comprehensive Analysis of Advanced Machine Learning Techniques",
        authors=["Dr. Jane Smith", "Prof. John Doe", "Dr. Alice Johnson", "Prof. Bob Wilson"],
        venue="International Conference on Artificial Intelligence",
        year=2024,
        doi="10.1234/example.doi",
        url="https://example.com/paper"
    )
    
    # Create sections with very long bullets to test pagination
    sections = [
        SummarizedSection(
            name=SectionName.METHODS,
            bullets=[
                "We implemented a comprehensive multi-stage deep learning pipeline that incorporates convolutional neural networks, recurrent neural networks, and transformer architectures to process complex sequential data with high-dimensional features and temporal dependencies.",
                "Our experimental methodology involved extensive hyperparameter optimization using Bayesian optimization techniques, cross-validation procedures, and ensemble learning approaches to ensure robust and reliable model performance across diverse datasets and evaluation metrics.",
                "The data preprocessing pipeline included advanced techniques such as feature engineering, dimensionality reduction, data augmentation, normalization, and outlier detection to handle various data quality issues and improve model generalization capabilities.",
                "We conducted rigorous statistical analysis including significance testing, confidence interval estimation, effect size calculations, and multiple comparison corrections to ensure the validity and reliability of our experimental results and conclusions.",
                "The implementation utilized state-of-the-art deep learning frameworks and distributed computing infrastructure to handle large-scale datasets and complex model architectures efficiently while maintaining reproducibility and computational efficiency.",
                "Our evaluation methodology incorporated multiple performance metrics, ablation studies, comparative analysis with baseline methods, and comprehensive error analysis to provide thorough insights into model behavior and limitations."
            ]
        ),
        SummarizedSection(
            name=SectionName.RESULTS,
            bullets=[
                "Our experimental results demonstrate significant improvements in performance across all evaluation metrics, with the proposed method achieving state-of-the-art results on benchmark datasets while maintaining computational efficiency and scalability requirements.",
                "The ablation studies reveal the importance of each component in our proposed architecture, with detailed analysis showing how different design choices contribute to overall model performance and robustness across various experimental conditions and dataset characteristics.",
                "Comparative analysis with existing baseline methods shows consistent superiority of our approach, with statistical significance tests confirming the reliability of performance improvements and the effectiveness of our proposed techniques and methodologies.",
                "Error analysis provides valuable insights into model limitations and failure cases, identifying specific scenarios where performance degrades and suggesting potential areas for future improvement and research directions.",
                "The scalability experiments demonstrate the ability of our method to handle large-scale datasets efficiently, with linear scaling behavior and practical computational requirements that make it suitable for real-world applications and deployment scenarios."
            ]
        ),
        SummarizedSection(
            name=SectionName.DISCUSSION,
            bullets=[
                "The superior performance of our proposed method can be attributed to several key factors including the innovative architecture design, effective feature learning mechanisms, robust optimization strategies, and comprehensive evaluation procedures that ensure reliable and reproducible results.",
                "Our findings have important implications for the field, suggesting new research directions and practical applications while highlighting the potential for further improvements and extensions to address current limitations and challenges in the domain.",
                "The limitations of our study include computational resource requirements, dataset-specific performance variations, and the need for further validation across diverse domains and application scenarios to ensure generalizability and practical utility.",
                "Future work should focus on addressing identified limitations, exploring alternative architectures, investigating transfer learning capabilities, and developing more efficient training procedures to improve scalability and applicability to real-world problems.",
                "The practical implications of our research extend beyond academic interest, with potential applications in various industries and domains where accurate and efficient machine learning solutions are required for complex decision-making processes and automated systems."
            ]
        )
    ]
    
    print(f"📊 Created {len(sections)} sections with long content")
    total_bullets = sum(len(section.bullets) for section in sections)
    print(f"📝 Total bullets: {total_bullets}")
    
    # Build presentation with pagination
    print("\n🔨 Building presentation with pagination...")
    output_path = 'pagination_demo.pptx'
    
    try:
        pptx_path, slide_count = build_presentation(
            metadata, 
            sections, 
            'academic', 
            output_path
        )
        
        print(f"✅ Created presentation: {pptx_path}")
        print(f"📊 Total slides: {slide_count}")
        
        # Check if file exists and has reasonable size
        file_size = Path(output_path).stat().st_size
        print(f"📁 File size: {file_size:,} bytes")
        
        if file_size > 1000:
            print("✅ File size looks reasonable")
        else:
            print("⚠️  File size seems small")
            
        print(f"\n🎯 Pagination Results:")
        print(f"   • Input sections: {len(sections)}")
        print(f"   • Total bullets: {total_bullets}")
        print(f"   • Output slides: {slide_count}")
        print(f"   • Average bullets per slide: {total_bullets / slide_count:.1f}")
        
        if slide_count > len(sections):
            print(f"   • Pagination occurred: {slide_count - len(sections)} additional slides created")
        else:
            print(f"   • All content fit on original slides")
            
    except Exception as e:
        print(f"❌ PowerPoint creation failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Pagination demo completed successfully!")
    print(f"📄 Output file: {output_path}")
    print("💡 Open the PowerPoint file to see how long content was paginated.")
    
    return True

if __name__ == "__main__":
    success = test_pagination_with_long_content()
    sys.exit(0 if success else 1)
