from __future__ import annotations

import smtplib
from datetime import date
from email.message import EmailMessage

from water_newsletter.config import AppConfig


def build_email(config: AppConfig, *, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.sender
    message["To"] = ", ".join(config.recipients)
    message.set_content(body)
    return message


def subject_for(newsletter_type: str, end_date: date) -> str:
    if newsletter_type == "monthly":
        return f"[월간] 글로벌 물환경 동향 | {end_date:%Y}년 {end_date:%m}월호"
    return f"[주간] 글로벌 물환경 동향 | {end_date:%Y}년 {end_date:%m}월 {end_date:%d}일"


def send_email(config: AppConfig, message: EmailMessage) -> None:
    with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as smtp:
        if config.smtp_use_tls:
            smtp.starttls()
        if config.smtp_username and config.smtp_password:
            smtp.login(config.smtp_username, config.smtp_password)
        smtp.send_message(message)
