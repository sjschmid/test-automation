#!/usr/bin/env python3
"""Email the newest weather report. Needs GMAIL_USER and GMAIL_APP_PASSWORD env vars."""
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

TO = "sjschmid@gmail.com"


def main() -> int:
    user = os.environ.get("GMAIL_USER")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not user or not password:
        print("GMAIL_USER / GMAIL_APP_PASSWORD not set - skipping email.")
        return 0

    files = sorted(Path(__file__).parent.glob("weather/weather-in-stuttgart_*.txt"))
    if not files:
        print("No weather file found.", file=sys.stderr)
        return 1
    latest = files[-1]

    msg = EmailMessage()
    msg["Subject"] = f"Weather in Stuttgart ({latest.stem.split('_', 1)[1]} UTC)"
    msg["From"] = user
    msg["To"] = TO
    body = latest.read_text(encoding="utf-8")
    page_url = os.environ.get("PAGE_URL")
    if page_url:
        body += f"\nVisual report: {page_url}\n"
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)
    print(f"Sent {latest.name} to {TO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
