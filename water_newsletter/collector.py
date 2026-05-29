from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from time import struct_time
from urllib.parse import urlparse

import feedparser

from water_newsletter.models import Article
from water_newsletter.sources import EXCLUDE_KEYWORDS, FEED_SOURCES, INCLUDE_KEYWORDS, TIER1_DOMAINS


def _parse_entry_date(entry: feedparser.FeedParserDict) -> date | None:
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if isinstance(parsed, struct_time):
            return datetime(*parsed[:6]).date()
    return None


def _clean_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", text).strip()


def _matches_keywords(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def classify_tier(article: Article) -> str | None:
    blob = f"{article.title} {article.content_summary} {article.url}".lower()
    if _matches_keywords(blob, EXCLUDE_KEYWORDS):
        return None
    if not _matches_keywords(blob, INCLUDE_KEYWORDS):
        return None
    host = urlparse(article.url).netloc.lower()
    if any(domain in host for domain in TIER1_DOMAINS):
        return "tier1"
    return "tier2"


def collect_articles(
    *,
    lookback_days: int,
    now: datetime | None = None,
) -> tuple[list[Article], int]:
    end = now or datetime.now()
    start = end.date() - timedelta(days=lookback_days)
    seen_urls: set[str] = set()
    articles: list[Article] = []
    reviewed_count = 0

    for source in FEED_SOURCES:
        feed = feedparser.parse(source.url)
        for entry in feed.entries:
            url = str(entry.get("link", "")).strip()
            if not url or url in seen_urls:
                continue
            published = _parse_entry_date(entry)
            if published is None or published < start or published > end.date():
                continue

            reviewed_count += 1
            title = _clean_text(str(entry.get("title", "")))
            summary = _clean_text(str(entry.get("summary", ""))) or title
            article = Article(
                title=title,
                url=url,
                source=source.source,
                country=source.country,
                published_date=published,
                content_summary=summary[:500],
            )
            tier = classify_tier(article)
            if tier is None:
                continue
            seen_urls.add(url)
            articles.append(
                Article(
                    title=article.title,
                    url=article.url,
                    source=article.source,
                    country=article.country,
                    published_date=article.published_date,
                    content_summary=article.content_summary,
                    tier=tier,
                )
            )

    articles.sort(key=lambda item: (item.published_date, item.title), reverse=True)
    return articles, reviewed_count
