from __future__ import annotations

from random import choice
from uuid import uuid4

from app.core.security import sign_question_payload
from app.schemas.question import QuestionResponse
from app.services.explanations.explanation_builder import integer_explanation
from app.utils.randomness import mixed_sign_pair, non_zero_int


def generate_integer_question(difficulty: str) -> QuestionResponse:
    if difficulty == "easy":
        a, b = mixed_sign_pair(12)
        operator = choice(["+", "-"])
        prompt = f"Calculate: {a} {operator} ({b})"
        expected = a + b if operator == "+" else a - b
    elif difficulty == "medium":
        a, b = mixed_sign_pair(12)
        c = non_zero_int(-9, 9)
        operator = choice(["+", "-", "×"])
        if operator == "×":
            prompt = f"Calculate: ({a}) × ({b}) + ({c})"
            expected = (a * b) + c
        elif operator == "+":
            prompt = f"Calculate: ({a}) + ({b}) - ({c})"
            expected = a + b - c
        else:
            prompt = f"Calculate: ({a}) - ({b}) + ({c})"
            expected = a - b + c
    else:
        divisor = choice([2, 3, 4, 5, 6])
        quotient = non_zero_int(-8, 8)
        dividend = divisor * quotient
        c, d = mixed_sign_pair(10)
        prompt = f"Calculate: ({dividend} ÷ {divisor}) + ({c}) × ({d})"
        expected = (dividend // divisor) + (c * d)

    payload = {
        "question_id": str(uuid4()),
        "module": "integer-operations",
        "difficulty": difficulty,
        "prompt": prompt,
        "question_kind": "integer_operation",
        "input_type": "text",
        "answer_type": "integer",
        "expected_answer": str(expected),
        "correct_answer_display": str(expected),
        "explanation": integer_explanation(prompt, str(expected)),
    }

    return QuestionResponse(
        question_id=payload["question_id"],
        module="integer-operations",
        difficulty=difficulty,
        prompt=prompt,
        input_type="text",
        question_kind="integer_operation",
        placeholder="Example: -7",
        validation_token=sign_question_payload(payload),
    )
