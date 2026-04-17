from fastapi import APIRouter, HTTPException, status

from app.api.deps import DbSession
from app.core.config import get_settings
from app.core.security import TokenError, verify_question_payload
from app.repositories.question_attempt_repository import QuestionAttemptRepository
from app.repositories.practice_session_repository import PracticeSessionRepository
from app.repositories.stats_repository import StatsRepository
from app.schemas.session import SessionSummary
from app.schemas.validation import SubmitAnswerRequest, ValidationResult
from app.services.validation.registry import validate_answer

router = APIRouter()
settings = get_settings()


@router.post("/answers/validate", response_model=ValidationResult)
def validate_submission(payload: SubmitAnswerRequest, db: DbSession) -> ValidationResult:
    try:
        token_payload = verify_question_payload(payload.validation_token)
    except TokenError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if token_payload.get("question_id") != payload.question_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question ID mismatch")

    if token_payload.get("module") != payload.module or token_payload.get("difficulty") != payload.difficulty:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question context mismatch")

    is_correct, normalized_user_answer = validate_answer(
        module=payload.module,
        answer_type=token_payload["answer_type"],
        user_answer=payload.user_answer,
        expected_answer=token_payload["expected_answer"],
    )

    attempt_id = None
    session_summary = None
    session_id = payload.session_id

    if settings.session_persistence_enabled and session_id:
        practice_session = PracticeSessionRepository(db).get(session_id)
        if practice_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        attempt = QuestionAttemptRepository(db).create(
            session_id=session_id,
            module=payload.module,
            difficulty=payload.difficulty,
            prompt=token_payload["prompt"],
            question_kind=token_payload["question_kind"],
            user_answer=payload.user_answer.strip(),
            normalized_user_answer=normalized_user_answer,
            expected_answer=token_payload["correct_answer_display"],
            is_correct=is_correct,
            explanation=token_payload["explanation"],
        )
        attempt_id = attempt.id
        session_summary = SessionSummary(**StatsRepository(db).session_summary(session_id))
    elif session_id:
        session_summary = SessionSummary(session_id=session_id, attempts=0, correct_attempts=0, accuracy=0.0)

    return ValidationResult(
        attempt_id=attempt_id,
        session_id=session_id,
        is_correct=is_correct,
        normalized_user_answer=normalized_user_answer,
        correct_answer=token_payload["correct_answer_display"],
        explanation=token_payload["explanation"],
        session_summary=session_summary,
    )
