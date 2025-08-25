"""Conclusion synthesis utilities for generating meaningful conclusions."""

from __future__ import annotations
from typing import List, Dict
from ..nlp.keyphrase import extract_keyphrases

def synthesize_conclusion(sec_map: Dict[str, List[str]]) -> List[str]:
    """
    Synthesize a strong conclusion from existing sections.
    Creates 3-4 bullets combining objectives, methods, results, and limitations.
    """
    intro = sec_map.get("INTRODUCTION", [])[:1]
    meth = sec_map.get("METHODS", [])[:1]
    res = sec_map.get("RESULTS", [])[:2]
    lim = sec_map.get("LIMITATIONS", [])[:1]
    
    bullets = []
    
    # Objective from introduction
    if intro:
        bullets.append(f"**Objective:** {intro[0]}")
    
    # Approach from methods
    if meth:
        bullets.append(f"**Approach:** {meth[0]}")
    
    # Key findings from results
    if res:
        bullets.append(f"**Findings:** {res[0]}")
        if len(res) > 1:
            bullets.append(f"**Impact:** {res[1]}")
    
    # Limitations
    if lim and len(bullets) < 4:
        bullets.append(f"**Limitations:** {lim[0]}")
    
    # Ensure we have at least 2 bullets by synthesizing from available content
    if len(bullets) < 2:
        # Try to extract more content from other sections
        for section_name, section_bullets in sec_map.items():
            if section_name not in ["INTRODUCTION", "METHODS", "RESULTS", "LIMITATIONS"] and section_bullets:
                bullets.append(f"**{section_name.title()}:** {section_bullets[0]}")
                break
        
        # If still not enough, create a summary from the most important section
        if len(bullets) < 2:
            most_important = max(sec_map.items(), key=lambda x: len(x[1])) if sec_map else None
            if most_important:
                bullets.append(f"**Summary:** {most_important[1][0]}")
    
    return bullets[:4]

def extract_conclusion_keyphrases(sec_map: Dict[str, List[str]]) -> List[str]:
    """Extract key phrases from all sections for conclusion callout."""
    all_text = " ".join([
        " ".join(bullets) for bullets in sec_map.values()
    ])
    return extract_keyphrases(all_text, top_k=5)

def create_conclusion_slide_content(sec_map: Dict[str, List[str]]) -> tuple[List[str], List[str]]:
    """Create conclusion slide content and key terms."""
    conclusion_bullets = synthesize_conclusion(sec_map)
    key_terms = extract_conclusion_keyphrases(sec_map)
    return conclusion_bullets, key_terms
