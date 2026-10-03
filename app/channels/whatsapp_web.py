"""Free WhatsApp Web outreach helper for Hamed.

Opens an individualized message in WhatsApp Web. It never bulk-sends,
bypasses WhatsApp protections, or sends without an explicit permitted-contact
flag.
"""
from __future__ import annotations

import os
import re
import subprocess
import urllib.parse


def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("0") and os.getenv("HAMED_DEFAULT_COUNTRY_CODE"):
        digits = os.getenv("HAMED_DEFAULT_COUNTRY_CODE", "") + digits[1:]
    if len(digits) < 8:
        raise ValueError("Invalid phone number")
    return digits


def build_whatsapp_web_url(phone: str, message: str) -> str:
    number = normalize_phone(phone)
    if not message.strip():
        raise ValueError("Message cannot be empty")
    return "https://web.whatsapp.com/send?phone=" + number + "&text=" + urllib.parse.quote(message)


def open_whatsapp_web(phone: str, message: str) -> str:
    if os.getenv("HAMED_WHATSAPP_WEB_OPEN", "true").lower() != "true":
        raise RuntimeError("WhatsApp Web opening is disabled")
    url = build_whatsapp_web_url(phone, message)
    if os.name == "nt":
        os.startfile(url)
    else:
        subprocess.Popen(["xdg-open", url])
    return url
