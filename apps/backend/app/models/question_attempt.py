from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, UUIDTimestampMixin


class QuestionAttempt(UUIDTimestampMixin, Base):
    __tablename__ = "question_attempts"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("practice_sessions.id", ondelete="CASCADE"), index=True)
    module: Mapped[str] = mapped_column(String(64))
    difficulty: Mapped[str] = mapped_column(String(16))
    prompt: Mapped[str] = mapped_column(Text)
    question_kind: Mapped[str] = mapped_column(String(64))
    user_answer: Mapped[str] = mapped_column(Text)
    normalized_user_answer: Mapped[str] = mapped_column(Text)
    expected_answer: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    explanation: Mapped[str] = mapped_column(Text)

    session: Mapped["PracticeSession"] = relationship("PracticeSession", back_populates="attempts")
