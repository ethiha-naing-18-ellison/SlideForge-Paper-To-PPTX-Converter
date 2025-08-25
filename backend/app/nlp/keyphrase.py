from __future__ import annotations
import re
from typing import List, Tuple
from collections import Counter

WORD = re.compile(r"[A-Za-z][A-Za-z\-']+")
STOP = set("""a an the of to in and for is are was were be being been on with by from this that these those as at it its into about than then such through per via using use used based we our you your they he she etc et al fig table""".split())

def noun_phrases(text: str, max_len: int = 4) -> List[str]:
    words = [w.lower() for w in WORD.findall(text)]
    phrases = []
    for i in range(len(words)):
        for L in range(2, max_len+1):
            if i+L <= len(words):
                chunk = words[i:i+L]
                if any(w in STOP for w in chunk): continue
                phrases.append(" ".join(chunk))
    return phrases

def extract_keyphrases(text: str, top_k: int = 6) -> List[str]:
    c = Counter(noun_phrases(text))
    return [p for p,_ in c.most_common(top_k)]
