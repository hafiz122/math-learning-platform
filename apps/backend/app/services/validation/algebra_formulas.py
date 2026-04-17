from app.services.validation.algebra_expressions import validate_expression_answer
from app.services.validation.integer_operations import validate_integer_answer


def validate_formula_answer(answer_type: str, user_answer: str, expected_answer: str) -> tuple[bool, str]:
    if answer_type == "multiple_choice":
        normalized = user_answer.strip().upper()
        return normalized == expected_answer.strip().upper(), normalized
    if answer_type == "expression":
        return validate_expression_answer(user_answer, expected_answer)
    return validate_integer_answer(user_answer, expected_answer)
