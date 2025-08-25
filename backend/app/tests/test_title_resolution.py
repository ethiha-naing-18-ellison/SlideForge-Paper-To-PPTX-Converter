from app.services.extractor import resolve_title

def test_resolve_title_prefers_user():
    t = resolve_title("foo", meta_title="Research Paper", user_title="My Project Report")
    assert t == "My Project Report"

def test_resolve_title_infers_from_text():
    raw = "A Practical Approach to Slide Generation\nJohn Doe\nAbstract\nWe..."
    t = resolve_title(raw, None, None)
    assert "Approach" in t

def test_resolve_title_handles_generic_titles():
    t = resolve_title("foo", meta_title="Research Paper", user_title=None)
    assert t != "Research Paper"

def test_resolve_title_fallback_to_first_line():
    raw = "This is a real title\nAbstract\nIntroduction"
    t = resolve_title(raw, None, None)
    assert t == "This is a real title"

def test_resolve_title_ignores_heading_keywords():
    raw = "Abstract\nIntroduction\nMethods\nThis is the real title"
    t = resolve_title(raw, None, None)
    assert t == "This is the real title"

def test_resolve_title_returns_untitled_for_empty():
    t = resolve_title("", None, None)
    assert t == "Untitled"
