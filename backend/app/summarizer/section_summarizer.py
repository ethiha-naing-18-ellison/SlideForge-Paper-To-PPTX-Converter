from __future__ import annotations
from typing import Dict, List
from ..nlp.segmenter import split_to_sections, sentences
from ..services.ppt.sections import canonicalize
from ..nlp.keyphrase import extract_keyphrases
from ..nlp.importance import rank_sentences_by_mmr
from ..nlp.abstractive import abstractive_summarize
from ..models.schema import GlobalSummaryConfig, SectionSummarySpec

def summarize_sections(raw_text: str, cfg: GlobalSummaryConfig) -> Dict[str, List[str]]:
    sections = split_to_sections(raw_text)
    out: Dict[str, List[str]] = {}

    for raw_name, text in sections.items():
        canon = canonicalize(raw_name)
        spec: SectionSummarySpec = cfg.per_section.get(canon, cfg.default)
        sents = sentences(text)[: max(5, cfg.max_section_sentences)]

        # pick diverse, salient sentences
        top_idx = rank_sentences_by_mmr(sents, lambda_div=cfg.diversity_lambda, top_k=spec.target_bullets * 2)
        picked = [sents[i] for i in top_idx]

        # optional abstractive compression (or fallback)
        compressed = abstractive_summarize(picked, cfg.abstractive_model_name if cfg.abstractive else None, spec.max_words_per_bullet)

        # limit bullets & optionally append keyphrases
        bullets = compressed[:spec.target_bullets]
        if spec.include_keyphrases:
            kps = extract_keyphrases(text)[:3]
            if kps:
                bullets[-1] += f" — Key terms: " + ", ".join(kps[:3])

        # style helpers (inline emphasis on first N words)
        if spec.emphasize_first_words > 0:
            styled = []
            for b in bullets:
                parts = b.split()
                if len(parts) > spec.emphasize_first_words:
                    head = " ".join(parts[:spec.emphasize_first_words])
                    tail = " ".join(parts[spec.emphasize_first_words:])
                    styled.append(f"**{head}** {tail}")
                else:
                    styled.append(f"**{b}**")
            bullets = styled

        out[canon] = bullets
    return out

# --- SlideForge: variable bullet budget (append) ---
def summarize_section_with_budget(text: str, cfg: GlobalSummaryConfig, target_bullets: int, max_words: int) -> List[str]:
    # reuse summarize_sections() logic for one section: rank → compress → limit
    sents = sentences(text)[: max(5, cfg.max_section_sentences)]
    top_idx = rank_sentences_by_mmr(sents, lambda_div=cfg.diversity_lambda, top_k=min(len(sents), target_bullets * 2))
    picked = [sents[i] for i in top_idx]
    compressed = abstractive_summarize(picked, cfg.abstractive_model_name if cfg.abstractive else None, max_words)
    return compressed[:target_bullets]
