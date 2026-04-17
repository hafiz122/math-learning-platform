def validate_integer_answer(user_answer: str, expected_answer: str) -> tuple[bool, str]:
    normalized = user_answer.strip()
    return normalized == str(int(expected_answer)), normalized
