from app.schemas.question import QuestionResponse
from app.services.generators.algebra_expressions import generate_algebra_expression_question
from app.services.generators.algebra_formulas import generate_algebra_formula_question
from app.services.generators.integer_operations import generate_integer_question


def generate_question(module: str, difficulty: str) -> QuestionResponse:
    if module == "integer-operations":
        return generate_integer_question(difficulty)
    if module == "algebra-expressions":
        return generate_algebra_expression_question(difficulty)
    if module == "algebra-formulas":
        return generate_algebra_formula_question(difficulty)
    raise ValueError(f"Unsupported module: {module}")
