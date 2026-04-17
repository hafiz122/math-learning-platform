from typing import Literal

from pydantic import Field

from app.schemas.common import BaseSchema


class ChoiceOption(BaseSchema):
    key: str
    label: str


class QuestionResponse(BaseSchema):
    question_id: str
    module: Literal["integer-operations", "algebra-expressions", "algebra-formulas"]
    difficulty: Literal["easy", "medium", "hard"]
    prompt: str
    input_type: Literal["text", "multiple_choice"]
    question_kind: str
    placeholder: str | None = None
    choices: list[ChoiceOption] | None = None
    validation_token: str


class GenerateQuestionQuery(BaseSchema):
    module: Literal["integer-operations", "algebra-expressions", "algebra-formulas"]
    difficulty: Literal["easy", "medium", "hard"]
