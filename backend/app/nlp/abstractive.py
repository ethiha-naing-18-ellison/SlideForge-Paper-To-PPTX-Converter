from __future__ import annotations
from typing import List

def compress_sentence_simple(text: str, max_words: int = 35) -> str:
    words = text.split()
    if len(words) <= max_words: return text.strip()
    # Return complete words without ellipsis
    return " ".join(words[:max_words])

def abstractive_summarize(sentences: List[str], model_name: str | None, max_words: int) -> List[str]:
    """
    Optional hook: if HF transformers is available and model_name set, run T5/BART on concatenated text
    and split result into short points. Otherwise fallback to per-sentence compression.
    """
    try:
        if model_name:
            from transformers import pipeline
            pipe = pipeline("summarization", model=model_name, truncation=True)
            joined = " ".join(sentences)[:3000]
            out = pipe(joined, max_length=max_words*2, min_length=max_words, do_sample=False)
            txt = out[0]["summary_text"]
            parts = [p.strip() for p in txt.replace("•",";").split(";") if p.strip()]
            return [compress_sentence_simple(p, max_words) for p in parts][:6]
    except Exception:
        pass
    return [compress_sentence_simple(s, max_words) for s in sentences]
