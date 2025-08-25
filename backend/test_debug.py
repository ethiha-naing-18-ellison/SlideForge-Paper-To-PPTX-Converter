#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.models.schema import GlobalSummaryConfig, SectionSummarySpec

def test_config():
    """Test the GlobalSummaryConfig creation."""
    try:
        # Create a basic config
        cfg = GlobalSummaryConfig()
        print(f"Config created successfully: {type(cfg)}")
        print(f"max_section_sentences: {cfg.max_section_sentences}")
        
        # Test with custom values
        cfg2 = GlobalSummaryConfig(
            default=SectionSummarySpec(target_bullets=4, max_words_per_bullet=18),
            abstractive=False,
            diversity_lambda=0.65,
            coverage_weight=0.35
        )
        print(f"Config2 created successfully: {type(cfg2)}")
        print(f"max_section_sentences: {cfg2.max_section_sentences}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_config()
