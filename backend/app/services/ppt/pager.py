# backend/app/services/ppt/pager.py
from __future__ import annotations
from typing import List

def chunk_bullets(
    bullets: List[str],
    bullets_per_slide: int,
    min_slides: int,
    max_slides: int
) -> List[List[str]]:
    """
    Split bullets into pages (slides) with an upper limit per slide.
    Guarantees at least min_slides (duplicating or rebalancing if needed),
    and at most max_slides.
    """
    bullets = [b for b in bullets if (b or "").strip()]
    if not bullets:
        bullets = ["(No content detected)"]

    # primary chunking
    pages = [bullets[i:i+bullets_per_slide] for i in range(0, len(bullets), bullets_per_slide)]

    # enforce max
    if len(pages) > max_slides:
        # merge tail into last page(s) without exceeding bullets_per_slide too much
        merged = []
        for pg in pages[:max_slides-1]:
            merged.append(pg)
        rest = [b for pg in pages[max_slides-1:] for b in pg]
        merged.append(rest)
        pages = merged

    # enforce min
    while len(pages) < min_slides:
        # duplicate last or rebalance
        last = pages[-1] if pages else bullets[:bullets_per_slide]
        pages.append(list(last))

    return pages
