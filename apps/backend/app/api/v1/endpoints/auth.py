from __future__ import annotations

from fastapi import APIRouter, Request, Response

from app.api.deps import DbSession
from app.schemas.auth import AuthMeResponse, LoginWithCodeRequest
from app.services.auth_service import get_current_auth, login_with_code, logout

router = APIRouter(prefix="/auth", tags=["auth"])

SESSION_COOKIE = "mlp_session"
DEVICE_COOKIE = "mlp_device"


def _cookie_settings() -> dict:
    return {
        "httponly": True,
        "secure": False,
        "samesite": "lax",
        "path": "/",
    }


@router.post("/login-with-code", response_model=AuthMeResponse)
def login_with_code_endpoint(
    payload: LoginWithCodeRequest,
    request: Request,
    response: Response,
    db: DbSession,
) -> AuthMeResponse:
    result = login_with_code(
        db=db,
        raw_code=payload.code,
        raw_device_token=request.cookies.get(DEVICE_COOKIE),
        display_name=payload.display_name,
        device_name=payload.device_name,
    )

    response.set_cookie(
        key=SESSION_COOKIE,
        value=result["session_token"],
        max_age=60 * 60 * 24 * 30,
        **_cookie_settings(),
    )

    if result["device_token"]:
        response.set_cookie(
            key=DEVICE_COOKIE,
            value=result["device_token"],
            max_age=60 * 60 * 24 * 180,
            **_cookie_settings(),
        )

    return AuthMeResponse(**result["me"])


@router.get("/me", response_model=AuthMeResponse)
def auth_me(request: Request, db: DbSession) -> AuthMeResponse:
    me = get_current_auth(db, request.cookies.get(SESSION_COOKIE))
    return AuthMeResponse(**me)


@router.post("/logout")
def auth_logout(request: Request, response: Response, db: DbSession) -> dict:
    logout(db, request.cookies.get(SESSION_COOKIE))
    response.delete_cookie(SESSION_COOKIE, path="/")
    response.delete_cookie(DEVICE_COOKIE, path="/")
    return {"ok": True}