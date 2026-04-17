from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LoginWithCodeRequest(BaseModel):
    code: str = Field(min_length=8, max_length=32)
    display_name: str | None = Field(default=None, min_length=2, max_length=40)
    device_name: str | None = Field(default=None, min_length=2, max_length=80)


class AuthMeResponse(BaseModel):
    authenticated: bool
    display_name: str | None = None
    customer_name: str | None = None
    expires_at: datetime | None = None
    max_devices: int | None = None
    devices_used: int | None = None