from __future__ import annotations

from datetime import date

from water_newsletter.models import COUNTRY_EMOJI, Article
from water_newsletter.sources import MONTHLY_SECTION_KEYWORDS


def _emoji(country: str) -> str:
    return COUNTRY_EMOJI.get(country, "🌐")


def _section_for_article(article: Article) -> str:
    blob = f"{article.title} {article.content_summary}".lower()
    for section, keywords in MONTHLY_SECTION_KEYWORDS.items():
        if any(keyword.lower() in blob for keyword in keywords):
            return section
    return "기타 주요 동향"


def format_weekly(
    articles: list[Article],
    *,
    issue_number: int,
    start_date: date,
    end_date: date,
    total_reviewed: int,
) -> str:
    tier1 = [item for item in articles if item.tier == "tier1"]
    tier2 = [item for item in articles if item.tier == "tier2"]
    header = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌊 글로벌 물환경 동향 뉴스레터 (주간)\n"
        f"   {end_date:%Y}년 {end_date:%m}월 {end_date:%d}일 | 제{issue_number}호\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    if not tier1 and not tier2:
        return (
            f"{header}\n\n"
            "이번 주 특이 동향 없음\n"
            f"수집 기간({start_date:%Y-%m-%d}~{end_date:%Y-%m-%d}) 동안\n"
            "주요 물환경 관련 새로운 동향이 확인되지 않았습니다.\n"
            "모니터링은 계속됩니다.\n"
            f"검토 자료: {total_reviewed}건\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    lines = [header, "", "──────────────────────────────────", f"🔴 주요 동향  [{len(tier1)}건]", "──────────────────────────────────"]
    for item in tier1:
        summary = item.korean_summary or (item.content_summary[:80], item.content_summary[80:160], "")
        lines.extend(
            [
                f"{_emoji(item.country)} {item.title}",
                summary[0],
                summary[1],
                summary[2],
                f"🔗 원문: {item.url}",
                "",
            ]
        )

    lines.extend(["──────────────────────────────────", f"📎 참고 자료  [{len(tier2)}건]", "──────────────────────────────────"])
    for item in tier2:
        lines.append(f"• {item.title} ({item.source}, {_emoji(item.country)}) → {item.url}")

    lines.extend(
        [
            "──────────────────────────────────",
            "📊 이번 주 모니터링 현황",
            f"검토 {total_reviewed}건  |  주요 동향 {len(tier1)}건  |  참고 자료 {len(tier2)}건",
            f"수집 기간: {start_date:%Y-%m-%d} ~ {end_date:%Y-%m-%d}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ]
    )
    return "\n".join(lines)


def format_monthly(
    articles: list[Article],
    *,
    start_date: date,
    end_date: date,
    total_reviewed: int,
) -> str:
    tier1 = [item for item in articles if item.tier == "tier1"]
    tier2 = [item for item in articles if item.tier == "tier2"]
    header = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌊 글로벌 물환경 동향 뉴스레터 (월간)\n"
        f"   {end_date:%Y}년 {end_date:%m}월호\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    if not tier1 and not tier2:
        return (
            f"{header}\n\n"
            "이번 달 특이 동향 없음\n"
            f"수집 기간({start_date:%Y-%m-%d}~{end_date:%Y-%m-%d}) 동안\n"
            "주요 물환경 관련 새로운 동향이 확인되지 않았습니다.\n"
            f"검토 자료: {total_reviewed}건\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    keywords = _top_keywords(tier1)
    lines = [header, "", f"📌 이달의 키워드: {keywords}"]

    sections: dict[str, list[Article]] = {}
    for item in tier1:
        sections.setdefault(_section_for_article(item), []).append(item)

    for section, items in sections.items():
        lines.extend(["", "──────────────────────────────────", f"🔴 {section}", "──────────────────────────────────"])
        for item in items:
            summary = item.korean_summary or (item.content_summary[:80], item.content_summary[80:160], "")
            lines.extend(
                [
                    f"{_emoji(item.country)} {item.title}",
                    summary[0],
                    summary[1],
                    summary[2],
                    f"🔗 원문: {item.url}",
                    "",
                ]
            )

    lines.extend(["──────────────────────────────────", f"📎 참고 자료 목록 [{len(tier2)}건]", "──────────────────────────────────"])
    for item in tier2:
        lines.append(f"• {item.title} ({item.source}, {_emoji(item.country)}) → {item.url}")

    lines.extend(
        [
            "──────────────────────────────────",
            "📊 이달 모니터링 현황",
            f"검토 {total_reviewed}건  |  주요 동향 {len(tier1)}건  |  참고 자료 {len(tier2)}건",
            f"수집 기간: {start_date:%Y-%m-%d} ~ {end_date:%Y-%m-%d}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ]
    )
    return "\n".join(lines)


def _top_keywords(tier1: list[Article]) -> str:
    counts: dict[str, int] = {}
    for item in tier1:
        for token in ("PFAS", "수질", "유역", "수생태", "microplastic", "regulation"):
            if token.lower() in f"{item.title} {item.content_summary}".lower():
                counts[token] = counts.get(token, 0) + 1
    if not counts:
        return "물환경 | 모니터링 | 정책"
    ranked = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:3]
    return " | ".join(name for name, _ in ranked)
