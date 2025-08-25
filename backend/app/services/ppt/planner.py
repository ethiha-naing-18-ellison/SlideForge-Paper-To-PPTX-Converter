from __future__ import annotations
from typing import Dict
from app.nlp.segmenter import split_to_sections
from .sections import canonicalize

def section_char_lengths(raw_text: str) -> Dict[str, int]:
    S = split_to_sections(raw_text)
    L = {}
    for h, t in S.items():
        L[canonicalize(h)] = max(L.get(canonicalize(h), 0), len(t))
    return L

def allocate_slides(raw_text: str, target_total: int, min_per: int, max_per: int, bias: dict | None = None) -> Dict[str, int]:
    """
    Distribute target_total slides across canonical sections proportional to length, with bias multipliers.
    """
    lengths = section_char_lengths(raw_text)
    if not lengths:
        return {"OTHER": target_total}
    bias = bias or {}
    weighted = {k: lengths[k] * float(bias.get(k, 1.0)) for k in lengths}
    Z = sum(weighted.values()) or 1.0
    alloc = {k: max(min_per, int(round((weighted[k] / Z) * target_total))) for k in weighted}
    # cap per-section maximum and re-normalize if needed
    over = {k: max(0, alloc[k] - max_per) for k in alloc}
    overflow = sum(over.values())
    for k,v in over.items():
        if v > 0: alloc[k] -= v
    remaining = max(0, target_total - sum(alloc.values()))
    # distribute remaining to sections under max_per by descending need
    for k in sorted(weighted, key=lambda kk: weighted[kk], reverse=True):
        if remaining <= 0: break
        space = max_per - alloc[k]
        take = min(space, remaining)
        alloc[k] += take
        remaining -= take
    return alloc
