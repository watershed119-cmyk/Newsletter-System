from datetime import date

from water_newsletter.collector import classify_tier
from water_newsletter.formatter import format_weekly
from water_newsletter.main import is_last_day_of_month
from water_newsletter.models import Article


def sample_article(**overrides) -> Article:
    base = {
        "title": "EPA updates PFAS drinking water standard",
        "url": "https://www.epa.gov/news/pfas-standard",
        "source": "US EPA",
        "country": "USA",
        "published_date": date(2026, 5, 28),
        "content_summary": "EPA finalized PFAS limits for drinking water quality.",
        "tier": "tier1",
    }
    base.update(overrides)
    return Article(**base)


def test_classify_tier_marks_epa_as_tier1():
    article = sample_article(tier=None)
    assert classify_tier(article) == "tier1"


def test_classify_tier_excludes_marine_only_content():
    article = sample_article(
        title="Pacific ocean plastic gyre grows",
        url="https://example.org/marine",
        content_summary="Marine debris island in the Pacific Ocean.",
        tier=None,
    )
    assert classify_tier(article) is None


def test_format_weekly_includes_issue_number():
    body = format_weekly(
        [sample_article()],
        issue_number=2,
        start_date=date(2026, 5, 23),
        end_date=date(2026, 5, 30),
        total_reviewed=10,
    )
    assert "제2호" in body
    assert "PFAS" in body or "EPA" in body


def test_is_last_day_of_month():
    assert is_last_day_of_month(date(2026, 5, 31)) is True
    assert is_last_day_of_month(date(2026, 5, 30)) is False
