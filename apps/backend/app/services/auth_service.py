from __future__ import annotations

from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.auth_codes import generate_token, stable_hash, utc_now
from app.models.access_code import AccessCode
from app.models.auth_device import AuthDevice
from app.models.auth_session import AuthSession


SESSION_DAYS = 30


def _normalize_code(raw_code: str) -> str:
    return raw_code.strip().upper()


def _active_device_count(db: Session, access_code_id: str) -> int:
    stmt = (
        select(func.count(AuthDevice.id))
        .where(AuthDevice.access_code_id == access_code_id)
        .where(AuthDevice.revoked_at.is_(None))
    )
    return int(db.scalar(stmt) or 0)


def _get_access_code_by_raw_code(db: Session, raw_code: str) -> AccessCode | None:
    code_hash = stable_hash(_normalize_code(raw_code))
    stmt = select(AccessCode).where(AccessCode.code_hash == code_hash)
    return db.scalar(stmt)


def _resolve_device(db: Session, access_code: AccessCode, raw_device_token: str | None) -> AuthDevice | None:
    if not raw_device_token:
        return None

    token_hash = stable_hash(raw_device_token)
    stmt = (
        select(AuthDevice)
        .where(AuthDevice.access_code_id == access_code.id)
        .where(AuthDevice.device_token_hash == token_hash)
        .where(AuthDevice.revoked_at.is_(None))
    )
    return db.scalar(stmt)


def login_with_code(
    db: Session,
    raw_code: str,
    raw_device_token: str | None,
    display_name: str | None,
    device_name: str | None,
) -> dict:
    access_code = _get_access_code_by_raw_code(db, raw_code)

    if not access_code or access_code.status != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access code.")

    if access_code.expires_at <= utc_now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access code has expired.")

    device = _resolve_device(db, access_code, raw_device_token)
    new_device_token: str | None = None

    if device is None:
        devices_used = _active_device_count(db, access_code.id)
        if devices_used >= access_code.max_devices:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Device limit reached. Please log out from another device first.",
            )

        new_device_token = generate_token()
        device = AuthDevice(
            access_code_id=access_code.id,
            device_token_hash=stable_hash(new_device_token),
            device_name=device_name,
        )
        db.add(device)
        db.flush()

    session_token = generate_token()
    session_expiry = min(access_code.expires_at, utc_now() + timedelta(days=SESSION_DAYS))

    auth_session = AuthSession(
        access_code_id=access_code.id,
        auth_device_id=device.id,
        session_token_hash=stable_hash(session_token),
        expires_at=session_expiry,
    )
    db.add(auth_session)

    device.last_seen_at = utc_now()

    if display_name and not access_code.display_name:
        access_code.display_name = display_name.strip()

    db.commit()

    devices_used = _active_device_count(db, access_code.id)

    return {
        "session_token": session_token,
        "device_token": new_device_token,
        "me": {
            "authenticated": True,
            "display_name": access_code.display_name,
            "customer_name": access_code.customer_name,
            "expires_at": access_code.expires_at,
            "max_devices": access_code.max_devices,
            "devices_used": devices_used,
        },
    }


def get_current_auth(db: Session, raw_session_token: str | None) -> dict:
    if not raw_session_token:
        return {"authenticated": False}

    token_hash = stable_hash(raw_session_token)
    stmt = (
        select(AuthSession)
        .where(AuthSession.session_token_hash == token_hash)
        .where(AuthSession.revoked_at.is_(None))
    )
    auth_session = db.scalar(stmt)

    if not auth_session:
        return {"authenticated": False}

    if auth_session.expires_at <= utc_now():
        auth_session.revoked_at = utc_now()
        db.commit()
        return {"authenticated": False}

    access_code = auth_session.access_code
    device = auth_session.device

    if access_code.status != "active" or access_code.expires_at <= utc_now():
        auth_session.revoked_at = utc_now()
        db.commit()
        return {"authenticated": False}

    auth_session.last_seen_at = utc_now()
    device.last_seen_at = utc_now()
    db.commit()

    devices_used = _active_device_count(db, access_code.id)

    return {
        "authenticated": True,
        "display_name": access_code.display_name,
        "customer_name": access_code.customer_name,
        "expires_at": access_code.expires_at,
        "max_devices": access_code.max_devices,
        "devices_used": devices_used,
    }


def logout(db: Session, raw_session_token: str | None) -> None:
    if not raw_session_token:
        return

    token_hash = stable_hash(raw_session_token)
    stmt = select(AuthSession).where(AuthSession.session_token_hash == token_hash)
    auth_session = db.scalar(stmt)

    if auth_session and auth_session.revoked_at is None:
        auth_session.revoked_at = utc_now()
        db.commit()