
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.question_attempt import QuestionAttempt


class StatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def session_summary(self, session_id: str) -> dict[str, int | float | str]:
        attempts = (
            self.db.query(
                func.count(QuestionAttempt.id).label("attempts"),
                func.sum(case((QuestionAttempt.is_correct.is_(True), 1), else_=0)).label("correct_attempts"),
            )
            .filter(QuestionAttempt.session_id == session_id)
            .one()
        )

        total_attempts = int(attempts.attempts or 0)
        correct_attempts = int(attempts.correct_attempts or 0)
        accuracy = round((correct_attempts / total_attempts) * 100, 1) if total_attempts else 0.0

        return {
            "session_id": session_id,
            "attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "accuracy": accuracy,
        }
