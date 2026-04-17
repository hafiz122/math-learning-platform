from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.stats_repository import StatsRepository

settings = get_settings()


class StatsService:
    def get_summary(self, session_id: str, db: Session | None = None) -> dict[str, int | float | str]:
        if settings.session_persistence_enabled and db is not None:
            return StatsRepository(db).session_summary(session_id)
        return {
            "session_id": session_id,
            "attempts": 0,
            "correct_attempts": 0,
            "accuracy": 0.0,
        }
