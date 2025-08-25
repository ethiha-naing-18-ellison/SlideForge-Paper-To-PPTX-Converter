from __future__ import annotations
from typing import List, Tuple
from .embeddings import tfidf_matrix, cosine

def rank_sentences_by_mmr(sentences: List[str], lambda_div: float = 0.65, top_k: int = 5) -> List[int]:
    """MMR: balance relevance (centroid) and diversity."""
    if not sentences: return []
    vecs = tfidf_matrix(sentences)
    # centroid
    centroid = {}
    for v in vecs:
        for k,val in v.items():
            centroid[k] = centroid.get(k,0)+val
    # normalize centroid
    nz = sum(val*val for val in centroid.values()) ** 0.5 or 1
    for k in list(centroid.keys()):
        centroid[k] /= nz

    selected: List[int] = []
    candidates = list(range(len(sentences)))
    while candidates and len(selected) < top_k:
        best_i, best_score = None, -1e9
        for i in candidates:
            rel = cosine(vecs[i], centroid)
            div = 0.0
            if selected:
                div = min(cosine(vecs[i], vecs[j]) for j in selected)  # penalize redundancy
            score = (1 - lambda_div) * rel + lambda_div * (1 - div)
            if score > best_score:
                best_i, best_score = i, score
        selected.append(best_i)
        candidates.remove(best_i)
    return selected
