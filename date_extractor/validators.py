import re

_DIGIT_RE = re.compile(r"\d")

def has_any_digits(text: str) -> bool:
    return bool(_DIGIT_RE.search(text))
