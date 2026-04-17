from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base, UUIDTimestampMixin


class PracticeSession(UUIDTimestampMixin, Base):
    __tablename__ = "practice_sessions"

    attempts: Mapped[list["QuestionAttempt"]] = relationship(
        "QuestionAttempt",
        back_populates="session",
        cascade="all, delete-orphan",
    )
