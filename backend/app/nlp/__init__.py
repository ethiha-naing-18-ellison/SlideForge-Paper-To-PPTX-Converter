"""NLP modules for SlideForge."""

from .segmenter import split_to_sections, sentences
from .keyphrase import extract_keyphrases
from .embeddings import tfidf_matrix, cosine
from .importance import rank_sentences_by_mmr
from .abstractive import compress_sentence_simple, abstractive_summarize

__all__ = [
    "split_to_sections",
    "sentences", 
    "extract_keyphrases",
    "tfidf_matrix",
    "cosine",
    "rank_sentences_by_mmr",
    "compress_sentence_simple",
    "abstractive_summarize"
]
