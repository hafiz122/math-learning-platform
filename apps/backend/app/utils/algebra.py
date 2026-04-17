from __future__ import annotations

from sympy import Symbol, simplify
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
    parse_expr,
)

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)
_ALLOWED_SYMBOLS = {name: Symbol(name) for name in ["x", "y", "a", "b", "m", "n"]}


def parse_math_expression(value: str):
    normalized = value.strip().replace("^", "**")
    return parse_expr(normalized, local_dict=_ALLOWED_SYMBOLS, transformations=TRANSFORMATIONS, evaluate=True)


def expressions_are_equivalent(left: str, right: str) -> bool:
    return simplify(parse_math_expression(left) - parse_math_expression(right)) == 0


def normalize_expression(value: str) -> str:
    expr = parse_math_expression(value)
    return str(expr)


def display_expression(value: str) -> str:
    return (
        value.replace("**", "^")
        .replace("*x", "x")
        .replace("*y", "y")
        .replace("*a", "a")
        .replace("*b", "b")
        .replace("*m", "m")
        .replace("*n", "n")
    )
