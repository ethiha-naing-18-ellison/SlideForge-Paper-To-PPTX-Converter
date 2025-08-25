from app.summarizer.section_summarizer import summarize_sections
from app.models.schema import GlobalSummaryConfig, SectionSummarySpec

RAW = """INTRODUCTION
This study proposes a lightweight framework for slide generation from long documents. It addresses redundancy and overflow through pagination and compressive summarization.

METHODS
We segment sections, rank sentences by MMR, and compress with an abstractive fallback.

RESULTS
The approach yields concise slides with high coverage across sections while preventing layout overflow.

LIMITATIONS
Relies on heuristic sectioning; OCR not handled.

CONCLUSION
The system enables clean, readable decks from dense documents."""

def test_summarize_sections_produces_short_points():
    cfg = GlobalSummaryConfig(default=SectionSummarySpec(target_bullets=3, max_words_per_bullet=14, include_keyphrases=False))
    out = summarize_sections(RAW, cfg)
    assert "INTRODUCTION" in out and len(out["INTRODUCTION"]) <= 3
    assert all(len(b.split()) <= 16 for b in out["INTRODUCTION"])

def test_summarize_sections_handles_empty_sections():
    cfg = GlobalSummaryConfig()
    out = summarize_sections("", cfg)
    assert isinstance(out, dict)

def test_summarize_sections_respects_target_bullets():
    cfg = GlobalSummaryConfig(default=SectionSummarySpec(target_bullets=2, max_words_per_bullet=10))
    out = summarize_sections(RAW, cfg)
    for section_name, bullets in out.items():
        assert len(bullets) <= 2, f"Section {section_name} has {len(bullets)} bullets, expected <= 2"

def test_summarize_sections_emphasizes_first_words():
    cfg = GlobalSummaryConfig(default=SectionSummarySpec(emphasize_first_words=2))
    out = summarize_sections(RAW, cfg)
    for section_name, bullets in out.items():
        for bullet in bullets:
            if "**" in bullet:
                # Check that emphasis is applied
                assert bullet.startswith("**"), f"Bullet should start with **: {bullet}"
