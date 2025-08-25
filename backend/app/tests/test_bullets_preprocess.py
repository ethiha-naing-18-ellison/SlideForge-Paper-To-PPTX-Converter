"""Tests for bullet preprocessing functionality."""

from app.services.ppt.bullets_preprocess import preprocess_for_slide

def test_preprocess_for_slide_compacts_and_numbers():
    raw = [
        "We collected a dataset of 10k samples, cleaned it, and trained a model; evaluation used accuracy and F1.",
        "Then we tuned hyperparameters: learning rate, batch size, and epochs."
    ]
    bullets, list_type = preprocess_for_slide(
        raw_lines=raw, canon_section="METHODS",
        max_words_per_bullet=18, max_bullets=5, emphasize_n_words=2
    )
    assert 1 <= len(bullets) <= 5
    assert list_type == "numbered"
    # first words bolded using markdown markers
    assert bullets[0].startswith("**")
    # all bullets reasonably short
    assert all(len(b.split()) <= 19 for b in bullets)

def test_preprocess_for_slide_uses_bullets_for_intro():
    raw = [
        "This research addresses the problem of hand gesture recognition.",
        "We propose a novel approach using computer vision."
    ]
    bullets, list_type = preprocess_for_slide(
        raw_lines=raw, canon_section="INTRODUCTION",
        max_words_per_bullet=18, max_bullets=5, emphasize_n_words=2
    )
    assert list_type == "bullets"
    assert len(bullets) <= 5
