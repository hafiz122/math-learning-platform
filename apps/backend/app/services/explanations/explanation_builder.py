from app.utils.algebra import display_expression


def integer_explanation(expression: str, result: str) -> str:
    return f"Evaluate the integer expression carefully using order of operations. The simplified result is {result}."

def algebra_expression_explanation(kind: str, prompt: str, correct_answer: str) -> str:
    if kind == "evaluate_expression":
        return f"Substitute the given value into the expression, simplify step by step, and you get {correct_answer}."
    return f"Combine like terms or expand and simplify the expression. A correct simplified form is {display_expression(correct_answer)}."

def algebra_formula_explanation(kind: str, correct_answer: str) -> str:
    if kind == "identify_formula":
        return f"Match the structure of the expression to the standard identity. The correct choice is {correct_answer}."
    return f"Apply the relevant algebra formula carefully. A correct final answer is {display_expression(correct_answer)}."
