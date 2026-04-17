from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.practice_session_repository import PracticeSessionRepository

settings = get_settings()


class PracticeSessionService:
    def create_session(self, db: Session | None = None) -> str:
        if settings.session_persistence_enabled and db is not None:
            return PracticeSessionRepository(db).create().id
        return str(uuid4())
