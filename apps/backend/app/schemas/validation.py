from typing import Literal

from pydantic import Field

from app.schemas.common import BaseSchema
from app.schemas.session import SessionSummary


class SubmitAnswerRequest(BaseSchema):
    session_id: str | None = None
    module: Literal["integer-operations", "algebra-expressions", "algebra-formulas"]
    difficulty: Literal["easy", "medium", "hard"]
    question_id: str
    validation_token: str = Field(min_length=20)
    user_answer: str = Field(min_length=1)


class ValidationResult(BaseSchema):
    attempt_id: str | None = None
    session_id: str | None = None
    is_correct: bool
    normalized_user_answer: str
    correct_answer: str
    explanation: str
    session_summary: SessionSummary | None = None
