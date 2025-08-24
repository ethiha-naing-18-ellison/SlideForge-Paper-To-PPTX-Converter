"""TextRank summarizer implementation."""

from __future__ import annotations

import re
from typing import List

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as SumyTextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from .base import SummarizerBase


class TextRankSummarizer(SummarizerBase):
    """TextRank-based summarizer using sumy library."""
    
    def __init__(self, language: str = "english", sentences_count: int = 10):
        """Initialize TextRank summarizer.
        
        Args:
            language: Language for tokenization and stemming
            sentences_count: Number of sentences to extract (will be filtered later)
        """
        self.language = language
        self.sentences_count = sentences_count
        self.stemmer = Stemmer(language)
        self.stop_words = get_stop_words(language)
    
    def summarize_section(self, text: str, max_bullets: int = 6) -> List[str]:
        """Summarize text using TextRank algorithm."""
        if not text.strip():
            return []
        
        # Clean and prepare text
        cleaned_text = self._preprocess_text(text)
        if not cleaned_text:
            return []
        
        try:
            # Parse text
            parser = PlaintextParser.from_string(cleaned_text, Tokenizer(self.language))
            
            # Create summarizer
            summarizer = SumyTextRankSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words
            
            # Extract sentences
            sentences = summarizer(parser.document, self.sentences_count)
            
            # Convert to bullet points
            bullets = []
            for sentence in sentences:
                bullet = self._sentence_to_bullet(str(sentence))
                if bullet:
                    bullets.append(bullet)
            
            # Filter and return
            return self.filter_bullets(bullets, max_bullets)
            
        except Exception as e:
            # Fallback to simple sentence extraction
            return self._fallback_summarize(text, max_bullets)
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for summarization."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common academic artifacts
        text = re.sub(r'\[[^\]]*\]', '', text)  # Remove citations
        text = re.sub(r'\([^)]*\)', '', text)   # Remove parentheticals
        
        # Ensure proper sentence endings
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    def _sentence_to_bullet(self, sentence: str) -> str:
        """Convert a sentence to a bullet point."""
        # Clean the sentence
        bullet = sentence.strip()
        
        # Remove common academic prefixes
        bullet = re.sub(r'^(The|This|These|It|They)\s+', '', bullet)
        
        # Ensure it's not too short or too long
        if len(bullet.split()) < 3 or len(bullet.split()) > 30:
            return ""
        
        return bullet
    
    def _fallback_summarize(self, text: str, max_bullets: int) -> List[str]:
        """Fallback summarization using simple sentence extraction."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Filter and clean sentences
        bullets = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) >= 5 and len(sentence.split()) <= 25:
                bullet = self._sentence_to_bullet(sentence)
                if bullet:
                    bullets.append(bullet)
            
            if len(bullets) >= max_bullets * 2:  # Get more than needed for filtering
                break
        
        return self.filter_bullets(bullets, max_bullets)
