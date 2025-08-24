"""Base summarizer interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class SummarizerBase(ABC):
    """Base class for text summarizers."""
    
    @abstractmethod
    def summarize_section(self, text: str, max_bullets: int = 6) -> List[str]:
        """Summarize a section of text into bullet points.
        
        Args:
            text: The text to summarize
            max_bullets: Maximum number of bullet points to generate
            
        Returns:
            List of bullet point strings (each <= 20 words)
        """
        pass
    
    def clean_bullet(self, bullet: str) -> str:
        """Clean and format a bullet point."""
        # Remove extra whitespace
        bullet = " ".join(bullet.split())
        
        # Remove common prefixes
        bullet = bullet.strip()
        if bullet.startswith(("•", "-", "*", "→", "⇒")):
            bullet = bullet[1:].strip()
        
        # Ensure proper capitalization
        if bullet and bullet[0].islower():
            bullet = bullet[0].upper() + bullet[1:]
        
        # Remove trailing punctuation
        bullet = bullet.rstrip(".,;:")
        
        return bullet
    
    def truncate_bullet(self, bullet: str, max_words: int = 20) -> str:
        """Truncate bullet to maximum word count."""
        words = bullet.split()
        if len(words) <= max_words:
            return bullet
        
        # Truncate and add ellipsis
        truncated = " ".join(words[:max_words])
        return truncated.rstrip(".,;:") + "..."
    
    def filter_bullets(self, bullets: List[str], max_bullets: int) -> List[str]:
        """Filter and clean bullet points."""
        cleaned_bullets = []
        
        for bullet in bullets:
            if not bullet.strip():
                continue
                
            cleaned = self.clean_bullet(bullet)
            if len(cleaned.split()) <= 20 and len(cleaned) > 10:
                cleaned_bullets.append(cleaned)
            
            if len(cleaned_bullets) >= max_bullets:
                break
        
        return cleaned_bullets[:max_bullets]
