from sqlalchemy.orm import Session

from app.models.question_attempt import QuestionAttempt


class QuestionAttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        session_id: str,
        module: str,
        difficulty: str,
        prompt: str,
        question_kind: str,
        user_answer: str,
        normalized_user_answer: str,
        expected_answer: str,
        is_correct: bool,
        explanation: str,
    ) -> QuestionAttempt:
        attempt = QuestionAttempt(
            session_id=session_id,
            module=module,
            difficulty=difficulty,
            prompt=prompt,
            question_kind=question_kind,
            user_answer=user_answer,
            normalized_user_answer=normalized_user_answer,
            expected_answer=expected_answer,
            is_correct=is_correct,
            explanation=explanation,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def list_by_session(self, session_id: str) -> list[QuestionAttempt]:
        return (
            self.db.query(QuestionAttempt)
            .filter(QuestionAttempt.session_id == session_id)
            .order_by(QuestionAttempt.created_at.asc())
            .all()
        )
