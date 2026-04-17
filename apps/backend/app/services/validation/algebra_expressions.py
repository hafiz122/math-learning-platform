from app.utils.algebra import expressions_are_equivalent, normalize_expression


def validate_expression_answer(user_answer: str, expected_answer: str) -> tuple[bool, str]:
    normalized = normalize_expression(user_answer)
    return expressions_are_equivalent(user_answer, expected_answer), normalized
