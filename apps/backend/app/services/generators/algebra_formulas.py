from __future__ import annotations

from random import choice, randint
from uuid import uuid4

from sympy import Symbol, expand

from app.core.security import sign_question_payload
from app.schemas.question import ChoiceOption, QuestionResponse
from app.services.explanations.explanation_builder import algebra_formula_explanation
from app.utils.algebra import display_expression
from app.utils.randomness import shuffled_choices

x = Symbol("x")

FORMULA_LABELS = {
    "square_of_sum": "(a+b)^2 = a^2 + 2ab + b^2",
    "square_of_difference": "(a-b)^2 = a^2 - 2ab + b^2",
    "difference_of_squares": "(a+b)(a-b) = a^2 - b^2",
}


def _near_base(base_choices: list[int]) -> tuple[int, int, int]:
    base = choice(base_choices)
    offset = randint(1, 9)
    sign = choice([-1, 1])
    value = base + (sign * offset)
    return base, offset, value


def _build_identify_formula_question() -> tuple[str, str]:
    template = choice(
        [
            "generic_square_sum",
            "generic_square_difference",
            "generic_difference_squares",
            "concrete_square_sum",
            "concrete_square_difference",
            "concrete_difference_squares",
        ]
    )

    if template == "generic_square_sum":
        return (
            "Which formula is used to expand (a + b)^2 ?",
            "square_of_sum",
        )

    if template == "generic_square_difference":
        return (
            "Which formula is used to expand (a - b)^2 ?",
            "square_of_difference",
        )

    if template == "generic_difference_squares":
        return (
            "Which formula is used to simplify (a + b)(a - b) ?",
            "difference_of_squares",
        )

    if template == "concrete_square_sum":
        coeff = choice([1, 2, 3, 4])
        number = randint(1, 9)
        if coeff == 1:
            expr = f"(x + {number})^2"
        else:
            expr = f"({coeff}x + {number})^2"
        return (
            f"Which formula is most suitable to expand {expr} ?",
            "square_of_sum",
        )

    if template == "concrete_square_difference":
        coeff = choice([1, 2, 3, 4])
        number = randint(1, 9)
        if coeff == 1:
            expr = f"(x - {number})^2"
        else:
            expr = f"({coeff}x - {number})^2"
        return (
            f"Which formula is most suitable to expand {expr} ?",
            "square_of_difference",
        )

    coeff = choice([1, 2, 3, 4])
    number = randint(1, 9)
    if coeff == 1:
        expr = f"(x + {number})(x - {number})"
    else:
        expr = f"({coeff}x + {number})({coeff}x - {number})"
    return (
        f"Which formula is most suitable to simplify {expr} ?",
        "difference_of_squares",
    )


def _build_medium_question() -> tuple[str, object, str, str]:
    template = choice(
        [
            "expand_square_sum_basic",
            "expand_square_difference_basic",
            "simplify_difference_squares_basic",
            "expand_square_sum_with_coeff",
            "expand_square_difference_with_coeff",
            "simplify_difference_squares_with_coeff",
        ]
    )

    if template == "expand_square_sum_basic":
        number = randint(1, 12)
        expr = (x + number) ** 2
        prompt = f"Expand using a formula: (x + {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "expand_square_difference_basic":
        number = randint(1, 12)
        expr = (x - number) ** 2
        prompt = f"Expand using a formula: (x - {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "simplify_difference_squares_basic":
        number = randint(1, 12)
        expr = (x + number) * (x - number)
        prompt = f"Simplify using a formula: (x + {number})(x - {number})"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "expand_square_sum_with_coeff":
        coeff = randint(2, 5)
        number = randint(1, 9)
        expr = (coeff * x + number) ** 2
        prompt = f"Expand using a formula: ({coeff}x + {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "expand_square_difference_with_coeff":
        coeff = randint(2, 5)
        number = randint(1, 9)
        expr = (coeff * x - number) ** 2
        prompt = f"Expand using a formula: ({coeff}x - {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    coeff = randint(2, 5)
    number = randint(1, 9)
    expr = (coeff * x + number) * (coeff * x - number)
    prompt = f"Simplify using a formula: ({coeff}x + {number})({coeff}x - {number})"
    expected = expand(expr)
    return prompt, expected, "apply_formula_expand", "expression"


def _build_hard_question() -> tuple[str, object, str, str]:
    template = choice(
        [
            "expand_square_sum_hard",
            "expand_square_difference_hard",
            "simplify_difference_squares_hard",
            "evaluate_structured_square_sum",
            "evaluate_structured_square_difference",
            "evaluate_difference_of_squares_product",
            "evaluate_difference_of_squares_subtraction",
            "evaluate_near_base_product",
        ]
    )

    if template == "expand_square_sum_hard":
        coeff = randint(3, 7)
        number = randint(2, 12)
        expr = (coeff * x + number) ** 2
        prompt = f"Expand fully using a formula: ({coeff}x + {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "expand_square_difference_hard":
        coeff = randint(3, 7)
        number = randint(2, 12)
        expr = (coeff * x - number) ** 2
        prompt = f"Expand fully using a formula: ({coeff}x - {number})^2"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "simplify_difference_squares_hard":
        coeff = randint(2, 6)
        number = randint(2, 15)
        expr = (coeff * x + number) * (coeff * x - number)
        prompt = f"Simplify fully using a formula: ({coeff}x + {number})({coeff}x - {number})"
        expected = expand(expr)
        return prompt, expected, "apply_formula_expand", "expression"

    if template == "evaluate_structured_square_sum":
        base = choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        offset = randint(1, 9)
        prompt = f"Evaluate using a formula: ({base} + {offset})^2"
        expected = (base + offset) ** 2
        return prompt, expected, "apply_formula_evaluate", "integer"

    if template == "evaluate_structured_square_difference":
        base = choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        offset = randint(1, 9)
        prompt = f"Evaluate using a formula: ({base} - {offset})^2"
        expected = (base - offset) ** 2
        return prompt, expected, "apply_formula_evaluate", "integer"

    if template == "evaluate_difference_of_squares_product":
        base = choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        offset = randint(1, 9)
        prompt = f"Evaluate using a formula: ({base} + {offset})({base} - {offset})"
        expected = (base + offset) * (base - offset)
        return prompt, expected, "apply_formula_evaluate", "integer"

    if template == "evaluate_difference_of_squares_subtraction":
        base = choice([30, 40, 50, 60, 70, 80, 90, 100])
        offset = randint(1, 9)
        a = base + offset
        b = base - offset
        prompt = f"Evaluate using a formula: {a}^2 - {b}^2"
        expected = (a**2) - (b**2)
        return prompt, expected, "apply_formula_evaluate", "integer"

    base = choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
    offset = randint(1, 9)
    a = base + offset
    b = base - offset
    prompt = f"Evaluate using a formula: {a} × {b}"
    expected = a * b
    return prompt, expected, "apply_formula_evaluate", "integer"


def generate_algebra_formula_question(difficulty: str) -> QuestionResponse:
    if difficulty == "easy":
        prompt, formula_key = _build_identify_formula_question()
        distractors = [label for key, label in FORMULA_LABELS.items() if key != formula_key]
        choices = shuffled_choices(FORMULA_LABELS[formula_key], distractors)
        correct_letter = next(letter for letter, label in choices if label == FORMULA_LABELS[formula_key])

        payload = {
            "question_id": str(uuid4()),
            "module": "algebra-formulas",
            "difficulty": difficulty,
            "prompt": prompt,
            "question_kind": "identify_formula",
            "input_type": "multiple_choice",
            "choices": [{"key": key, "label": label} for key, label in choices],
            "answer_type": "multiple_choice",
            "expected_answer": correct_letter,
            "correct_answer_display": correct_letter,
            "explanation": algebra_formula_explanation("identify_formula", correct_letter),
        }

        return QuestionResponse(
            question_id=payload["question_id"],
            module="algebra-formulas",
            difficulty=difficulty,
            prompt=prompt,
            input_type="multiple_choice",
            question_kind="identify_formula",
            choices=[ChoiceOption(**item) for item in payload["choices"]],
            validation_token=sign_question_payload(payload),
        )

    if difficulty == "medium":
        prompt, expected, question_kind, answer_type = _build_medium_question()
    else:
        prompt, expected, question_kind, answer_type = _build_hard_question()

    if answer_type == "expression":
        correct_display = display_expression(str(expected))
        placeholder = "Example: x^2 + 6x + 9"
    else:
        correct_display = str(expected)
        placeholder = "Example: 396"

    payload = {
        "question_id": str(uuid4()),
        "module": "algebra-formulas",
        "difficulty": difficulty,
        "prompt": prompt,
        "question_kind": question_kind,
        "input_type": "text",
        "answer_type": answer_type,
        "expected_answer": str(expected),
        "correct_answer_display": correct_display,
        "explanation": algebra_formula_explanation(question_kind, str(expected)),
    }

    return QuestionResponse(
        question_id=payload["question_id"],
        module="algebra-formulas",
        difficulty=difficulty,
        prompt=prompt,
        input_type="text",
        question_kind=question_kind,
        placeholder=placeholder,
        validation_token=sign_question_payload(payload),
    )