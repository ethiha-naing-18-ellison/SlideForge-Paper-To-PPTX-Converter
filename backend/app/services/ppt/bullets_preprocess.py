# backend/app/services/ppt/bullets_preprocess.py
from __future__ import annotations
import re
from typing import Iterable, List, Tuple
from .labels import strip_label_prefix
from .cleantext import normalize_text

MAX_WORDS_PER_BULLET_DEFAULT = 18
MAX_BULLETS_PER_SLIDE_DEFAULT = 5

# Light sentence split (avoid breaking on abbreviations)
_SENT_SPLIT = re.compile(
    r"(?<=[.!?])\s+(?=[A-Z0-9])"
)

# Basic clause split when sentences are too long
_CLAUSE_SPLIT = re.compile(r"[;:—–-]|\s,\s")

_MULTI_SPACE = re.compile(r"\s{2,}")

def normalize_whitespace(text: str) -> str:
    text = text.replace(" ( ", " (").replace(" )", ")")
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)     # no space before punctuation
    text = _MULTI_SPACE.sub(" ", text)
    text = text.replace("..", "…").replace("… …", "…")
    return text.strip()

def count_words(text: str) -> int:
    return len(text.strip().split())

def truncate_words(text: str, max_words: int) -> str:
    words = text.strip().split()
    if len(words) <= max_words:
        return text.strip()
    return " ".join(words[:max_words]) + "…"

def split_into_sentences(text: str) -> List[str]:
    text = normalize_whitespace(text)
    parts = _SENT_SPLIT.split(text)
    sentences = [p.strip() for p in parts if p and p.strip()]
    
    # Post-process to avoid breaking on common abbreviations
    final_sentences = []
    for sentence in sentences:
        # Skip very short sentences that might be abbreviations
        if len(sentence) < 3:
            continue
        final_sentences.append(sentence)
    
    return final_sentences

def split_long_sentence_into_clauses(sentence: str) -> List[str]:
    # split on major clause separators; keep short and meaningful
    chunks = _CLAUSE_SPLIT.split(sentence)
    return [normalize_whitespace(c) for c in chunks if c and c.strip()]

def sanitize_lines(raw_lines: Iterable[str]) -> List[str]:
    """Clean and sanitize raw lines by stripping labels and normalizing text."""
    out = []
    for line in raw_lines:
        if not line:
            continue
        # Remove inline key terms
        if " — Key terms:" in line:
            line = line.split(" — Key terms:")[0]
        # Strip label prefixes
        line = strip_label_prefix(line)
        # Normalize text
        line = normalize_text(line)
        # Skip meaningless content
        if line and line.lower() not in {"report", "other", "untitled"}:
            out.append(line)
    return out

def clean_and_split_paragraphs(paragraphs: Iterable[str]) -> List[str]:
    """Turn paragraphs into small bullet-ready sentences/clauses."""
    out: List[str] = []
    for para in paragraphs:
        if not para or not para.strip():
            continue
        for sent in split_into_sentences(para):
            out.append(sent)
    return out

def to_compact_bullets(
    raw_lines: Iterable[str],
    max_words_per_bullet: int = MAX_WORDS_PER_BULLET_DEFAULT,
    max_bullets: int = MAX_BULLETS_PER_SLIDE_DEFAULT,
) -> List[str]:
    """
    1) split into sentences
    2) for long sentences: split into clauses
    3) truncate to <= max_words_per_bullet
    4) keep up to max_bullets
    """
    sentences = clean_and_split_paragraphs(raw_lines)
    compact: List[str] = []

    for s in sentences:
        if count_words(s) > max_words_per_bullet + 6:  # clearly long → split clauses
            for c in split_long_sentence_into_clauses(s):
                if not c:
                    continue
                compact.append(truncate_words(c, max_words_per_bullet))
        else:
            compact.append(truncate_words(s, max_words_per_bullet))

        if len(compact) >= max_bullets:
            break

    # final hygiene & dedupe while keeping order
    seen = set()
    deduped: List[str] = []
    for b in compact:
        key = b.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(b)

    return deduped[:max_bullets]

def emphasize_first_n(bullets: List[str], n_words: int = 2) -> List[str]:
    """Bold the first N words (markdown-style; your renderer will convert to real bold)."""
    styled = []
    for b in bullets:
        parts = b.split()
        if len(parts) > n_words:
            head = " ".join(parts[:n_words])
            tail = " ".join(parts[n_words:])
            styled.append(f"**{head}** {tail}")
        else:
            styled.append(f"**{b}**")
    return styled

def choose_list_type_for_section(canon_section: str) -> str:
    """Return 'numbered' for Methods/Procedure-like sections; otherwise 'bullets'."""
    canon = (canon_section or "").upper()
    if any(k in canon for k in ("METHOD", "METHODOLOGY", "PROCEDURE", "EXPERIMENT")):
        return "numbered"
    return "bullets"

def preprocess_for_slide(
    raw_lines: Iterable[str],
    canon_section: str,
    max_words_per_bullet: int = MAX_WORDS_PER_BULLET_DEFAULT,
    max_bullets: int = MAX_BULLETS_PER_SLIDE_DEFAULT,
    emphasize_n_words: int = 2,
) -> Tuple[List[str], str]:
    """
    Returns (bullets, list_type)
      - bullets: compact, truncated, deduped, with **bold** on first N words
      - list_type: 'numbered' for methods-like sections, else 'bullets'
    """
    # Sanitize lines first
    raw_lines = sanitize_lines(raw_lines)
    
    bullets = to_compact_bullets(
        raw_lines,
        max_words_per_bullet=max_words_per_bullet,
        max_bullets=max_bullets,
    )
    bullets = emphasize_first_n(bullets, emphasize_n_words)
    list_type = choose_list_type_for_section(canon_section)
    return bullets, list_type
