from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta

from water_newsletter.collector import collect_articles
from water_newsletter.config import load_config
from water_newsletter.emailer import build_email, send_email, subject_for
from water_newsletter.formatter import format_monthly, format_weekly
from water_newsletter.state import load_state, save_state
from water_newsletter.summarizer import enrich_tier1_summaries


def is_last_day_of_month(day: date) -> bool:
    return (day + timedelta(days=1)).month != day.month


def run_newsletter(
    newsletter_type: str,
    *,
    dry_run: bool = False,
    now: datetime | None = None,
    force: bool = False,
) -> int:
    current = now or datetime.now()
    today = current.date()

    if newsletter_type == "monthly" and not force and not is_last_day_of_month(today):
        print("Not the last day of month; skipping monthly newsletter.")
        return 0

    lookback_days = 7 if newsletter_type == "weekly" else 30
    end_date = today
    start_date = end_date - timedelta(days=lookback_days)

    config = load_config()
    config_data = json.loads(config.config_path.read_text(encoding="utf-8"))
    state = load_state(
        config.state_file,
        default_issue_number=int(config_data.get("last_issue_number", 0)),
    )
    issue_number = int(state.get("last_issue_number", 0)) + 1

    articles, total_reviewed = collect_articles(lookback_days=lookback_days, now=current)
    articles = enrich_tier1_summaries(articles, api_key=config.anthropic_api_key)

    if newsletter_type == "weekly":
        body = format_weekly(
            articles,
            issue_number=issue_number,
            start_date=start_date,
            end_date=end_date,
            total_reviewed=total_reviewed,
        )
    else:
        body = format_monthly(
            articles,
            start_date=start_date,
            end_date=end_date,
            total_reviewed=total_reviewed,
        )

    tier1_count = sum(1 for item in articles if item.tier == "tier1")
    tier2_count = sum(1 for item in articles if item.tier == "tier2")

    if not tier1_count and not tier2_count:
        print("No relevant articles; email skipped")
        return 0

    message = build_email(
        config,
        subject=subject_for(newsletter_type, end_date),
        body=body,
    )

    if dry_run:
        print(message.get_content())
        return 0

    send_email(config, message)
    if newsletter_type == "weekly":
        state["last_issue_number"] = issue_number
        save_state(config.state_file, state)

    print(
        f"Sent {newsletter_type} newsletter to {', '.join(config.recipients)} "
        f"(tier1={tier1_count}, tier2={tier2_count})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Send automated water environment newsletter.")
    parser.add_argument(
        "newsletter_type",
        choices=["weekly", "monthly"],
        help="Newsletter schedule type",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print newsletter without sending.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run monthly newsletter even when today is not the last day of month.",
    )
    args = parser.parse_args(argv)

    try:
        return run_newsletter(
            args.newsletter_type,
            dry_run=args.dry_run,
            force=args.force,
        )
    except Exception as exc:
        print(f"water-newsletter failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
