from app.core.security import verify_question_payload
from app.services.generators.registry import generate_question
from app.services.validation.registry import validate_answer


def test_integer_generator_and_validation():
    question = generate_question("integer-operations", "easy")
    payload = verify_question_payload(question.validation_token)
    is_correct, normalized = validate_answer(
        "integer-operations",
        payload["answer_type"],
        payload["expected_answer"],
        payload["expected_answer"],
    )
    assert is_correct is True
    assert normalized == payload["expected_answer"]


def test_algebra_expression_equivalence():
    question = generate_question("algebra-expressions", "medium")
    payload = verify_question_payload(question.validation_token)

    if payload["answer_type"] == "expression":
        is_correct, _ = validate_answer(
            "algebra-expressions",
            "expression",
            payload["expected_answer"],
            payload["expected_answer"],
        )
        assert is_correct is True


def test_formula_identification_question_choices():
    question = generate_question("algebra-formulas", "easy")
    assert question.input_type == "multiple_choice"
    payload = verify_question_payload(question.validation_token)
    is_correct, normalized = validate_answer(
        "algebra-formulas",
        "multiple_choice",
        payload["expected_answer"],
        payload["expected_answer"],
    )
    assert is_correct is True
    assert normalized in {"A", "B", "C", "D"}
