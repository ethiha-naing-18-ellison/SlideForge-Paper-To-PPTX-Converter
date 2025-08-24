"""Hugging Face transformer summarizer implementation."""

from __future__ import annotations

import re
from typing import List, Optional

from .base import SummarizerBase


class HFTransformerSummarizer(SummarizerBase):
    """Hugging Face transformer-based summarizer."""
    
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-12-6"):
        """Initialize HF transformer summarizer.
        
        Args:
            model_name: Hugging Face model name for summarization
        """
        self.model_name = model_name
        self._model = None
        self._tokenizer = None
        self._device = None
    
    def summarize_section(self, text: str, max_bullets: int = 6) -> List[str]:
        """Summarize text using Hugging Face transformers."""
        if not text.strip():
            return []
        
        try:
            # Lazy load model
            if self._model is None:
                self._load_model()
            
            # Preprocess text
            cleaned_text = self._preprocess_text(text)
            if not cleaned_text:
                return []
            
            # Generate summary
            summary = self._generate_summary(cleaned_text)
            
            # Convert to bullet points
            bullets = self._summary_to_bullets(summary, max_bullets)
            
            return self.filter_bullets(bullets, max_bullets)
            
        except Exception as e:
            # Fallback to simple sentence extraction
            return self._fallback_summarize(text, max_bullets)
    
    def _load_model(self) -> None:
        """Load the Hugging Face model and tokenizer."""
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            import torch
            
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self._model.to(self._device)
            
        except ImportError:
            raise ImportError(
                "Transformers library not installed. "
                "Install with: pip install transformers torch"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model {self.model_name}: {str(e)}")
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for summarization."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove citations and references
        text = re.sub(r'\[[^\]]*\]', '', text)
        text = re.sub(r'\([^)]*\)', '', text)
        
        # Truncate if too long (most models have input limits)
        max_length = 1024
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text.strip()
    
    def _generate_summary(self, text: str) -> str:
        """Generate summary using the loaded model."""
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("Model not loaded")
        
        # Tokenize input
        inputs = self._tokenizer(
            text,
            max_length=1024,
            truncation=True,
            padding=True,
            return_tensors="pt"
        ).to(self._device)
        
        # Generate summary
        with torch.no_grad():
            summary_ids = self._model.generate(
                inputs["input_ids"],
                max_length=150,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
        
        # Decode summary
        summary = self._tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    def _summary_to_bullets(self, summary: str, max_bullets: int) -> List[str]:
        """Convert summary text to bullet points."""
        # Split summary into sentences
        sentences = re.split(r'[.!?]+', summary)
        
        bullets = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) >= 3 and len(sentence.split()) <= 25:
                bullet = self._sentence_to_bullet(sentence)
                if bullet:
                    bullets.append(bullet)
            
            if len(bullets) >= max_bullets:
                break
        
        return bullets
    
    def _sentence_to_bullet(self, sentence: str) -> str:
        """Convert a sentence to a bullet point."""
        # Clean the sentence
        bullet = sentence.strip()
        
        # Remove common prefixes
        bullet = re.sub(r'^(The|This|These|It|They)\s+', '', bullet)
        
        # Ensure proper length
        if len(bullet.split()) < 3 or len(bullet.split()) > 25:
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
            
            if len(bullets) >= max_bullets * 2:
                break
        
        return self.filter_bullets(bullets, max_bullets)
