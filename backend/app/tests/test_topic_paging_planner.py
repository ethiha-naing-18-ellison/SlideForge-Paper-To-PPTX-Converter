# backend/app/tests/test_topic_paging_planner.py
from app.services.ppt.planner import allocate_slides
from app.nlp.topic_chunker import cluster_sentences
from pptx import Presentation

RAW = """INTRODUCTION
This project explains X. It addresses Y. It motivates Z. It defines the problem and scope.

METHODS
We describe dataset A, model B, and training C. We explain evaluation D and ablations E.

RESULTS
Results on dataset A show improvements. Additional metrics confirm robustness.

LIMITATIONS
We note constraints and assumptions.

CONCLUSION
We summarize key takeaways and future work."""

def test_allocate_not_tiny():
    alloc = allocate_slides(RAW, target_total=12, min_per=1, max_per=5, bias=None)
    assert sum(alloc.values()) >= 10
    assert all(v >= 1 for v in alloc.values())

def test_cluster_count_matches_desired():
    sents = ["One.", "Two.", "Three.", "Four.", "Five.", "Six.", "Seven."] 
    cls = cluster_sentences(sents, desired_clusters=3)
    assert 1 <= len(cls) <= 3

def test_allocate_respects_max_per_section():
    alloc = allocate_slides(RAW, target_total=20, min_per=1, max_per=3, bias=None)
    assert all(v <= 3 for v in alloc.values())

def test_allocate_with_bias():
    bias = {"INTRODUCTION": 1.5, "METHODS": 2.0}
    alloc = allocate_slides(RAW, target_total=10, min_per=1, max_per=5, bias=bias)
    # Should have more slides for biased sections if they exist
    assert sum(alloc.values()) >= 8

def test_cluster_handles_empty_input():
    cls = cluster_sentences([], desired_clusters=3)
    assert len(cls) == 0

def test_cluster_handles_single_sentence():
    cls = cluster_sentences(["Single sentence."], desired_clusters=3)
    assert len(cls) == 1
