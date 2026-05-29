from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    source: str
    country: str
    published_date: date
    content_summary: str
    content_type: str = "news"
    tier: str | None = None
    korean_summary: tuple[str, str, str] | None = None


COUNTRY_EMOJI = {
    "USA": "🇺🇸",
    "EU": "🇪🇺",
    "Japan": "🇯🇵",
    "Korea": "🇰🇷",
    "Australia": "🇦🇺",
    "Academic": "📚",
}
