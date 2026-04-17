from app.services.validation.algebra_expressions import validate_expression_answer
from app.services.validation.algebra_formulas import validate_formula_answer
from app.services.validation.integer_operations import validate_integer_answer


def validate_answer(module: str, answer_type: str, user_answer: str, expected_answer: str) -> tuple[bool, str]:
    if module == "integer-operations":
        return validate_integer_answer(user_answer, expected_answer)
    if module == "algebra-expressions":
        if answer_type == "integer":
            return validate_integer_answer(user_answer, expected_answer)
        return validate_expression_answer(user_answer, expected_answer)
    if module == "algebra-formulas":
        return validate_formula_answer(answer_type, user_answer, expected_answer)
    raise ValueError(f"Unsupported module: {module}")
