from __future__ import annotations

import re

from water_newsletter.models import Article


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?。])\s+|\n+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def summarize_article(article: Article, *, api_key: str | None = None) -> tuple[str, str, str]:
    if api_key:
        try:
            return _summarize_with_anthropic(article, api_key)
        except Exception:
            pass
    return _summarize_heuristic(article)


def _summarize_heuristic(article: Article) -> tuple[str, str, str]:
    sentences = _split_sentences(article.content_summary) or [article.title]
    line1 = sentences[0][:80]
    line2 = sentences[1][:80] if len(sentences) > 1 else f"{article.source}({article.country}) 자료를 확인할 필요가 있다."
    line3 = sentences[2][:80] if len(sentences) > 2 else "국내 물환경 정책·관리에 참고할 수 있는 동향이다."
    return line1, line2, line3


def _summarize_with_anthropic(article: Article, api_key: str) -> tuple[str, str, str]:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        "아래 물환경 자료를 협회 뉴스레터용 3줄 한국어 요약으로 작성하세요. "
        "각 줄은 30~50자 내외의 완결된 문장이어야 합니다. "
        "번호 없이 줄만 3개 출력하세요.\n\n"
        f"제목: {article.title}\n"
        f"기관: {article.source}\n"
        f"국가: {article.country}\n"
        f"내용: {article.content_summary}\n"
        f"URL: {article.url}"
    )
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    lines = [line.lstrip("1234567890.-) ").strip() for line in text.splitlines() if line.strip()]
    while len(lines) < 3:
        lines.append("관련 후속 동향을 계속 모니터링할 예정이다.")
    return lines[0], lines[1], lines[2]


def enrich_tier1_summaries(
    articles: list[Article], *, api_key: str | None = None
) -> list[Article]:
    enriched: list[Article] = []
    for article in articles:
        if article.tier != "tier1":
            enriched.append(article)
            continue
        summary = summarize_article(article, api_key=api_key)
        enriched.append(
            Article(
                title=article.title,
                url=article.url,
                source=article.source,
                country=article.country,
                published_date=article.published_date,
                content_summary=article.content_summary,
                content_type=article.content_type,
                tier=article.tier,
                korean_summary=summary,
            )
        )
    return enriched
