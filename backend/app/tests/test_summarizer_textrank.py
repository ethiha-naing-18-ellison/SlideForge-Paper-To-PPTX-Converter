"""Unit tests for TextRank summarizer."""

import pytest
from unittest.mock import patch, MagicMock

from app.services.summarizer.textrank import TextRankSummarizer


class TestTextRankSummarizer:
    """Test cases for TextRank summarizer."""
    
    def test_clean_bullet(self):
        """Test bullet point cleaning."""
        summarizer = TextRankSummarizer()
        
        # Test whitespace normalization
        bullet = "  This   has   extra   spaces  "
        cleaned = summarizer.clean_bullet(bullet)
        assert cleaned == "This has extra spaces"
        
        # Test prefix removal
        bullet = "• This is a bullet point"
        cleaned = summarizer.clean_bullet(bullet)
        assert cleaned == "This is a bullet point"
        
        bullet = "- Another bullet point"
        cleaned = summarizer.clean_bullet(bullet)
        assert cleaned == "Another bullet point"
        
        # Test capitalization
        bullet = "this should be capitalized"
        cleaned = summarizer.clean_bullet(bullet)
        assert cleaned == "This should be capitalized"
        
        # Test trailing punctuation removal
        bullet = "This has trailing punctuation."
        cleaned = summarizer.clean_bullet(bullet)
        assert cleaned == "This has trailing punctuation"
    
    def test_truncate_bullet(self):
        """Test bullet truncation."""
        summarizer = TextRankSummarizer()
        
        # Test short bullet (no truncation needed)
        bullet = "This is a short bullet"
        truncated = summarizer.truncate_bullet(bullet, max_words=20)
        assert truncated == bullet
        
        # Test long bullet (truncation needed)
        long_bullet = "This is a very long bullet point that exceeds the maximum word limit and should be truncated"
        truncated = summarizer.truncate_bullet(long_bullet, max_words=10)
        assert len(truncated.split()) <= 10
        assert truncated.endswith("...")
    
    def test_filter_bullets(self):
        """Test bullet filtering."""
        summarizer = TextRankSummarizer()
        
        bullets = [
            "This is a good bullet point",
            "",  # Empty bullet
            "   ",  # Whitespace only
            "Too short",  # Too short
            "This is another good bullet point that should be included",
            "This is a very long bullet point that exceeds the maximum word limit and should be filtered out because it has too many words"
        ]
        
        filtered = summarizer.filter_bullets(bullets, max_bullets=3)
        
        assert len(filtered) <= 3
        assert "This is a good bullet point" in filtered
        assert "This is another good bullet point that should be included" in filtered
        assert "" not in filtered
        assert "   " not in filtered
    
    @patch('app.services.summarizer.textrank.PlaintextParser')
    @patch('app.services.summarizer.textrank.SumyTextRankSummarizer')
    def test_summarize_section_success(self, mock_summarizer_class, mock_parser_class):
        """Test successful section summarization."""
        # Mock the summarizer components
        mock_parser = MagicMock()
        mock_parser_class.from_string.return_value = mock_parser
        
        mock_summarizer = MagicMock()
        mock_summarizer_class.return_value = mock_summarizer
        
        # Mock sentences
        mock_sentences = [
            MagicMock(__str__=lambda self: "First important sentence."),
            MagicMock(__str__=lambda self: "Second important sentence."),
            MagicMock(__str__=lambda self: "Third important sentence.")
        ]
        mock_summarizer.return_value = mock_sentences
        
        summarizer = TextRankSummarizer()
        text = "This is a sample text for summarization. It contains multiple sentences. We want to extract the most important ones."
        
        result = summarizer.summarize_section(text, max_bullets=2)
        
        assert len(result) <= 2
        assert all(len(bullet.split()) <= 20 for bullet in result)
    
    def test_summarize_section_empty_text(self):
        """Test summarization with empty text."""
        summarizer = TextRankSummarizer()
        result = summarizer.summarize_section("", max_bullets=6)
        assert result == []
    
    def test_summarize_section_whitespace_only(self):
        """Test summarization with whitespace-only text."""
        summarizer = TextRankSummarizer()
        result = summarizer.summarize_section("   \n\t   ", max_bullets=6)
        assert result == []
    
    @patch('app.services.summarizer.textrank.PlaintextParser')
    def test_summarize_section_fallback(self, mock_parser_class):
        """Test fallback to simple sentence extraction when TextRank fails."""
        # Make TextRank fail
        mock_parser_class.from_string.side_effect = Exception("TextRank failed")
        
        summarizer = TextRankSummarizer()
        text = "This is the first sentence. This is the second sentence. This is the third sentence."
        
        result = summarizer.summarize_section(text, max_bullets=2)
        
        # Should fall back to simple sentence extraction
        assert len(result) <= 2
        assert all(len(bullet.split()) <= 20 for bullet in result)
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        summarizer = TextRankSummarizer()
        
        text = "This   has   extra   spaces. [Citation] (parenthetical)."
        processed = summarizer._preprocess_text(text)
        
        # Should remove extra whitespace
        assert "   " not in processed
        # Should remove citations
        assert "[Citation]" not in processed
        # Should remove parentheticals
        assert "(parenthetical)" not in processed
    
    def test_sentence_to_bullet(self):
        """Test sentence to bullet conversion."""
        summarizer = TextRankSummarizer()
        
        # Good sentence
        sentence = "This is a good sentence for a bullet point."
        bullet = summarizer._sentence_to_bullet(sentence)
        assert bullet == "is a good sentence for a bullet point."
        
        # Sentence with common prefix
        sentence = "The paper presents a new method."
        bullet = summarizer._sentence_to_bullet(sentence)
        assert bullet == "paper presents a new method."
        
        # Too short sentence
        sentence = "Hi."
        bullet = summarizer._sentence_to_bullet(sentence)
        assert bullet == ""
        
        # Too long sentence (more than 30 words)
        long_sentence = "This is a very long sentence that exceeds the maximum word limit and should be rejected because it has too many words to be a good bullet point and this makes it unacceptable for presentation purposes"
        bullet = summarizer._sentence_to_bullet(long_sentence)
        assert bullet == ""
    
    def test_fallback_summarize(self):
        """Test fallback summarization."""
        summarizer = TextRankSummarizer()
        
        text = "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence."
        
        result = summarizer._fallback_summarize(text, max_bullets=2)
        
        assert len(result) <= 2
        assert all(len(bullet.split()) <= 20 for bullet in result)
