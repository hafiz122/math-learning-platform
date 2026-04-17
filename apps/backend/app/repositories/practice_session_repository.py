from sqlalchemy.orm import Session

from app.models.practice_session import PracticeSession


class PracticeSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self) -> PracticeSession:
        session = PracticeSession()
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get(self, session_id: str) -> PracticeSession | None:
        return self.db.get(PracticeSession, session_id)
