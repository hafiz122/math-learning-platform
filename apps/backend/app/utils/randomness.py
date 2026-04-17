from random import choice, randint, sample


def non_zero_int(start: int, end: int) -> int:
    while True:
        value = randint(start, end)
        if value != 0:
            return value


def mixed_sign_pair(limit: int = 12) -> tuple[int, int]:
    a = non_zero_int(-limit, limit)
    b = non_zero_int(-limit, limit)
    if a * b > 0:
        b = -b
    return a, b


def shuffled_choices(correct_label: str, distractors: list[str]) -> list[tuple[str, str]]:
    options = [correct_label, *distractors]
    sampled = sample(options, k=len(options))
    letters = ["A", "B", "C", "D"]
    return list(zip(letters, sampled))
