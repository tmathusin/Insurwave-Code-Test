import re

_ORDINAL_SUFFIX_RE = re.compile(r'\b(\d{1,2})(st|nd|rd|th)\b', flags=re.IGNORECASE)

# Keep digits, letters (for month names), and basic whitespace/punctuation separators we rely on
# but strip other special symbols to simplify downstream parsing.
_ALLOWED_CHARS_RE = re.compile(r'[^A-Za-z0-9\s:/.,-]')

def remove_cardinality(text: str) -> str:
    """Remove ordinal suffixes like 1st, 2nd, 3rd, 4th -> 1,2,3,4."""
    return _ORDINAL_SUFFIX_RE.sub(lambda m: m.group(1), text)

def strip_special_chars(text: str) -> str:
    """Remove special characters not needed for date parsing, preserve separators."""
    return _ALLOWED_CHARS_RE.sub(' ', text)

def preprocess(text: str) -> str:
    text = remove_cardinality(text)
    text = strip_special_chars(text)
    # normalise whitespace
    return re.sub(r'\s+', ' ', text).strip()
