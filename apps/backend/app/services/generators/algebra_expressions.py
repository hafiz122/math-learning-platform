from __future__ import annotations

from random import choice, randint
from uuid import uuid4

from sympy import Symbol, expand, simplify

from app.core.security import sign_question_payload
from app.schemas.question import QuestionResponse
from app.services.explanations.explanation_builder import algebra_expression_explanation
from app.utils.algebra import display_expression

x = Symbol("x")


def _x_term(coeff: int) -> str:
    if coeff == 1:
        return "x"
    if coeff == -1:
        return "-x"
    return f"{coeff}x"


def _expected_display(expr) -> str:
    return display_expression(str(simplify(expand(expr))))


def _is_good_simplify_prompt(prompt_body: str, expr) -> bool:
    simplified = _expected_display(expr)
    return prompt_body.replace(" ", "") != simplified.replace(" ", "")


def _build_easy_simplify() -> tuple[str, object]:
    for _ in range(100):
        template = choice(["like_terms", "one_bracket", "mixed_terms"])

        if template == "like_terms":
            a = randint(2, 8)
            b = randint(2, 8)
            c = randint(1, 9)
            prompt_body = f"{_x_term(a)} + {_x_term(b)} - {c}"
            expr = a * x + b * x - c

        elif template == "one_bracket":
            a = randint(2, 5)
            b = randint(1, 7)
            c = randint(1, 7)
            inner_sign = choice(["+", "-"])
            outer_sign = choice(["+", "-"])

            if inner_sign == "+":
                inner_expr = x + b
                prompt_body = f"{a}(x + {b})"
            else:
                inner_expr = x - b
                prompt_body = f"{a}(x - {b})"

            if outer_sign == "+":
                expr = a * inner_expr + c
                prompt_body = f"{prompt_body} + {c}"
            else:
                expr = a * inner_expr - c
                prompt_body = f"{prompt_body} - {c}"

        else:
            a = randint(3, 8)
            b = randint(1, 5)
            c = randint(1, 5)
            d = randint(1, 9)
            expr = a * x - b * x + c * x - d
            prompt_body = f"{_x_term(a)} - {_x_term(b)} + {_x_term(c)} - {d}"

        if _is_good_simplify_prompt(prompt_body, expr):
            return prompt_body, expr

    fallback_expr = 2 * x + 5 * x - 3
    return "2x + 5x - 3", fallback_expr


def _build_medium_simplify() -> tuple[str, object]:
    for _ in range(120):
        template = choice(["two_brackets", "bracket_and_terms", "difference_brackets"])

        if template == "two_brackets":
            a = randint(2, 5)
            b = randint(2, 5)
            p = randint(1, 7)
            q = randint(1, 7)
            sign1 = choice(["+", "-"])
            sign2 = choice(["+", "-"])

            left_expr = x + p if sign1 == "+" else x - p
            right_expr = x + q if sign2 == "+" else x - q

            expr = a * left_expr + b * right_expr
            prompt_body = f"{a}(x {sign1} {p}) + {b}(x {sign2} {q})"

        elif template == "bracket_and_terms":
            a = randint(2, 6)
            b = randint(2, 6)
            c = randint(1, 6)
            d = randint(1, 8)
            expr = a * (x + c) - b * x + d
            prompt_body = f"{a}(x + {c}) - {_x_term(b)} + {d}"

        else:
            a = randint(2, 5)
            b = randint(2, 5)
            p = randint(1, 7)
            q = randint(1, 7)
            c = randint(1, 8)
            expr = a * (x + p) - b * (x - q) + c
            prompt_body = f"{a}(x + {p}) - {b}(x - {q}) + {c}"

        if _is_good_simplify_prompt(prompt_body, expr):
            return prompt_body, expr

    fallback_expr = 3 * (x + 4) - 2 * (x - 1) + 5
    return "3(x + 4) - 2(x - 1) + 5", fallback_expr


def _build_hard_simplify() -> tuple[str, object]:
    for _ in range(150):
        template = choice(["three_groups", "heavy_collect", "mixed_linear"])

        if template == "three_groups":
            a = randint(2, 6)
            b = randint(2, 6)
            c = randint(2, 6)
            p = randint(1, 8)
            q = randint(1, 8)
            r = randint(1, 8)

            expr = a * (x + p) - b * (x - q) + c * (x + r)
            prompt_body = f"{a}(x + {p}) - {b}(x - {q}) + {c}(x + {r})"

        elif template == "heavy_collect":
            a = randint(4, 8)
            b = randint(2, 6)
            c = randint(2, 6)
            d = randint(1, 9)

            expr = a * x - b * (x + c) + d
            prompt_body = f"{_x_term(a)} - {b}(x + {c}) + {d}"

        else:
            a = randint(2, 6)
            b = randint(2, 6)
            c = randint(2, 6)
            p = randint(1, 7)
            q = randint(1, 7)
            d = randint(1, 9)

            expr = a * (x - p) + b * x - c * (x + q) - d
            prompt_body = f"{a}(x - {p}) + {_x_term(b)} - {c}(x + {q}) - {d}"

        if _is_good_simplify_prompt(prompt_body, expr):
            return prompt_body, expr

    fallback_expr = 4 * (x + 3) - 3 * (x - 2) + 2 * (x - 5)
    return "4(x + 3) - 3(x - 2) + 2(x - 5)", fallback_expr


def _build_evaluate(difficulty: str) -> tuple[str, object]:
    if difficulty == "easy":
        a = randint(2, 5)
        b = randint(1, 9)
        value = randint(-4, 4)
        expr = a * x + b
        prompt = f"Evaluate: {_x_term(a)} + {b} when x = {value}"
        return prompt, simplify(expr.subs(x, value))

    if difficulty == "medium":
        a = randint(2, 5)
        b = randint(1, 6)
        c = randint(1, 7)
        value = randint(-3, 5)
        expr = a * (x + b) - c
        prompt = f"Evaluate: {a}(x + {b}) - {c} when x = {value}"
        return prompt, simplify(expand(expr).subs(x, value))

    a = randint(2, 6)
    b = randint(2, 5)
    c = randint(1, 6)
    d = randint(1, 8)
    value = randint(-3, 6)
    expr = a * (x + c) - b * x + d
    prompt = f"Evaluate: {a}(x + {c}) - {_x_term(b)} + {d} when x = {value}"
    return prompt, simplify(expand(expr).subs(x, value))


def generate_algebra_expression_question(difficulty: str) -> QuestionResponse:
    if difficulty == "easy":
        mode = choice(["simplify", "simplify", "evaluate"])

        if mode == "evaluate":
            prompt, expected_value = _build_evaluate("easy")
            question_kind = "evaluate_expression"
            answer_type = "integer"
            correct_answer_display = str(expected_value)
            expected_answer = str(expected_value)
            placeholder = "Example: 11"
        else:
            prompt_body, expr = _build_easy_simplify()
            prompt = f"Simplify: {prompt_body}"
            simplified = simplify(expand(expr))
            question_kind = "simplify_expression"
            answer_type = "expression"
            correct_answer_display = display_expression(str(simplified))
            expected_answer = str(simplified)
            placeholder = "Example: 7x - 2"

    elif difficulty == "medium":
        mode = choice(["simplify", "simplify", "evaluate"])

        if mode == "evaluate":
            prompt, expected_value = _build_evaluate("medium")
            question_kind = "evaluate_expression"
            answer_type = "integer"
            correct_answer_display = str(expected_value)
            expected_answer = str(expected_value)
            placeholder = "Example: 14"
        else:
            prompt_body, expr = _build_medium_simplify()
            prompt = f"Simplify: {prompt_body}"
            simplified = simplify(expand(expr))
            question_kind = "simplify_expression"
            answer_type = "expression"
            correct_answer_display = display_expression(str(simplified))
            expected_answer = str(simplified)
            placeholder = "Example: 3x + 8"

    else:
        mode = choice(["simplify", "simplify", "simplify", "evaluate"])

        if mode == "evaluate":
            prompt, expected_value = _build_evaluate("hard")
            question_kind = "evaluate_expression"
            answer_type = "integer"
            correct_answer_display = str(expected_value)
            expected_answer = str(expected_value)
            placeholder = "Example: 22"
        else:
            prompt_body, expr = _build_hard_simplify()
            prompt = f"Simplify fully: {prompt_body}"
            simplified = simplify(expand(expr))
            question_kind = "simplify_expression"
            answer_type = "expression"
            correct_answer_display = display_expression(str(simplified))
            expected_answer = str(simplified)
            placeholder = "Example: 3x - 11"

    payload = {
        "question_id": str(uuid4()),
        "module": "algebra-expressions",
        "difficulty": difficulty,
        "prompt": prompt,
        "question_kind": question_kind,
        "input_type": "text",
        "answer_type": answer_type,
        "expected_answer": expected_answer,
        "correct_answer_display": correct_answer_display,
        "explanation": algebra_expression_explanation(
            question_kind,
            prompt,
            correct_answer_display,
        ),
    }

    return QuestionResponse(
        question_id=payload["question_id"],
        module="algebra-expressions",
        difficulty=difficulty,
        prompt=prompt,
        input_type="text",
        question_kind=question_kind,
        placeholder=placeholder,
        validation_token=sign_question_payload(payload),
    )