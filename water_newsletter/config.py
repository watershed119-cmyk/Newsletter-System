from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    recipients: tuple[str, ...]
    sender_name: str
    system_name: str
    smtp_host: str
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_sender: str | None = None
    smtp_use_tls: bool = True
    anthropic_api_key: str | None = None
    config_path: Path = field(default_factory=lambda: Path("config.json"))
    state_file: Path = field(default_factory=lambda: Path(".state/newsletter.json"))

    @property
    def sender(self) -> str:
        if self.smtp_sender:
            return f"{self.sender_name} <{self.smtp_sender}>"
        if self.smtp_username:
            return f"{self.sender_name} <{self.smtp_username}>"
        return self.sender_name


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> AppConfig:
    config_path = Path(os.getenv("NEWSLETTER_CONFIG", "config.json"))
    data = json.loads(config_path.read_text(encoding="utf-8"))

    recipients = _split_csv(os.getenv("EMAIL_TO", "")) or tuple(data.get("recipients", []))
    smtp_host = os.getenv("SMTP_HOST", "").strip()

    missing = []
    if not recipients:
        missing.append("recipients (config.json or EMAIL_TO)")
    if not smtp_host:
        missing.append("SMTP_HOST")
    if missing:
        raise ValueError(f"Missing required settings: {', '.join(missing)}")

    return AppConfig(
        recipients=recipients,
        sender_name=str(data.get("sender_name", "글로벌 물환경 동향 모니터링팀")),
        system_name=str(data.get("system_name", "글로벌 물환경 동향 뉴스레터 시스템")),
        smtp_host=smtp_host,
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME") or None,
        smtp_password=os.getenv("SMTP_PASSWORD") or None,
        smtp_sender=os.getenv("SMTP_SENDER") or None,
        smtp_use_tls=_bool_env("SMTP_USE_TLS", True),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
        config_path=config_path,
        state_file=Path(os.getenv("STATE_FILE", ".state/newsletter.json")),
    )
