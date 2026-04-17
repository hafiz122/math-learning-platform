from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.questions import router as questions_router
from app.api.v1.endpoints.sessions import router as sessions_router
from app.api.v1.endpoints.validate import router as validate_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(questions_router)
api_router.include_router(validate_router)
api_router.include_router(sessions_router)
api_router.include_router(auth_router)