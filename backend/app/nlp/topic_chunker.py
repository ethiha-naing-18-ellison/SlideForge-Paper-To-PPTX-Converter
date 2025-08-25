from __future__ import annotations
from typing import List, Tuple, Dict
from collections import defaultdict
from .embeddings import tfidf_matrix, cosine

def cluster_sentences(sentences: List[str], desired_clusters: int) -> List[List[int]]:
    """
    Lightweight k-medoids-ish clustering on TF-IDF cosine.
    Returns clusters as lists of sentence indices.
    """
    if not sentences:
        return []
    desired = max(1, min(desired_clusters, len(sentences)))
    vecs = tfidf_matrix(sentences)

    # pick seeds by greedy farthest-first
    seeds = []
    remaining = set(range(len(sentences)))
    # first seed: longest sentence index
    seeds.append(max(remaining, key=lambda i: len(sentences[i])))
    remaining.remove(seeds[0])

    while len(seeds) < desired and remaining:
        def dist_to_seeds(i):
            return min(1 - cosine(vecs[i], vecs[s]) for s in seeds)
        nxt = max(remaining, key=dist_to_seeds)
        seeds.append(nxt)
        remaining.remove(nxt)

    # assign to closest seed by cosine
    clusters = defaultdict(list)
    for i,v in enumerate(vecs):
        best = max(range(len(seeds)), key=lambda k: cosine(v, vecs[seeds[k]]))
        clusters[best].append(i)

    # sort sentences inside each cluster by original order
    return [sorted(idxs) for _,idxs in sorted(clusters.items(), key=lambda kv: kv[0])]

def topic_subtitles(sentences: List[str], clusters: List[List[int]], max_len: int = 6) -> List[str]:
    """
    Heuristic topic labels from leading key terms in each cluster (first sentence few words).
    """
    subs = []
    for ids in clusters:
        if not ids:
            subs.append("Topic")
            continue
        first = sentences[ids[0]].strip().split()[:max_len]
        subs.append(" ".join(w.strip(",.;:") for w in first).title())
    return subs
