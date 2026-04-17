from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any

from app.core.config import get_settings


class TokenError(ValueError):
    pass


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


def sign_question_payload(payload: dict[str, Any]) -> str:
    secret = get_settings().question_token_secret.encode("utf-8")
    serialized = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    signature = hmac.new(secret, serialized, hashlib.sha256).digest()
    return f"{_b64encode(serialized)}.{_b64encode(signature)}"


def verify_question_payload(token: str) -> dict[str, Any]:
    try:
      raw_payload, raw_signature = token.split(".", 1)
    except ValueError as exc:
      raise TokenError("Malformed token") from exc

    serialized = _b64decode(raw_payload)
    received_signature = _b64decode(raw_signature)
    secret = get_settings().question_token_secret.encode("utf-8")
    expected_signature = hmac.new(secret, serialized, hashlib.sha256).digest()

    if not hmac.compare_digest(received_signature, expected_signature):
        raise TokenError("Invalid token signature")

    try:
        payload = json.loads(serialized.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise TokenError("Invalid token payload") from exc

    if not isinstance(payload, dict):
        raise TokenError("Invalid token content")
    return payload
