from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings


_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def stable_hash(value: str) -> str:
    secret = get_settings().question_token_secret
    return hashlib.sha256(f"{secret}:{value}".encode("utf-8")).hexdigest()


def generate_access_code() -> str:
    parts = []
    for _ in range(3):
        part = "".join(secrets.choice(_ALPHABET) for _ in range(4))
        parts.append(part)
    return "MLP-" + "-".join(parts)


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def days_from_now(days: int) -> datetime:
    return utc_now() + timedelta(days=days)