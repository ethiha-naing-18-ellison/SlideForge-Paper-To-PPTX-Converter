from __future__ import annotations
from typing import List
import math

# Lightweight fallback: TF-IDF-like scoring (no external models)
def tfidf_matrix(docs: List[str]) -> List[dict]:
    import math
    terms = {}
    for d in docs:
        for w in set(d.lower().split()):
            terms[w] = terms.get(w, 0) + 1
    N = len(docs)
    mats = []
    for d in docs:
        tf = {}
        words = d.lower().split()
        for w in words:
            tf[w] = tf.get(w,0)+1
        vec = {}
        for w, f in tf.items():
            idf = math.log((N+1)/(1+terms.get(w,1))) + 1
            vec[w] = (f/len(words))*idf
        mats.append(vec)
    return mats

def cosine(a: dict, b: dict) -> float:
    if not a or not b: return 0.0
    num = sum(a.get(k,0)*b.get(k,0) for k in set(a)|set(b))
    da = math.sqrt(sum(v*v for v in a.values()))
    db = math.sqrt(sum(v*v for v in b.values()))
    if da==0 or db==0: return 0.0
    return num/(da*db)
