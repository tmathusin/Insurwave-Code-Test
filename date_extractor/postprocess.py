from __future__ import annotations
import re
import logging
from typing import Iterable, List, Optional
from datetime import datetime
from .config import settings

logger = logging.getLogger(__name__)

# Supported explicit formats (expandable)
_FORMATS = [
    "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d",
    "%d %B %Y", "%d %b %Y", "%B %d %Y", "%b %d %Y",
    "%d/%m/%y", "%d-%m-%y", "%m/%d/%Y",
]

# Map month names to numbers for simple normalisation attempts
_MONTH_MAP = {
    m.lower(): i for i, m in enumerate(
        ["January","February","March","April","May","June","July","August","September","October","November","December"], start=1
    )
}
# add short names
_MONTH_MAP.update({m[:3].lower(): i for m, i in _MONTH_MAP.items()})

_DAY_RE = r"(?P<day>\d{1,2})"
_MONTH_RE = r"(?P<month>\d{1,2}|[A-Za-z]{3,9})"
_YEAR_RE = r"(?P<year>\d{2,4})"

# basic patterns we try before strptime formats
_PATTERNS = [
    re.compile(fr"{_DAY_RE}\s*/\s*{_MONTH_RE}\s*/\s*{_YEAR_RE}", re.IGNORECASE),
    re.compile(fr"{_DAY_RE}\s*-\s*{_MONTH_RE}\s*-\s*{_YEAR_RE}", re.IGNORECASE),
    re.compile(fr"{_DAY_RE}\s+{_MONTH_RE}\s+{_YEAR_RE}", re.IGNORECASE),
    re.compile(fr"{_MONTH_RE}\s+{_DAY_RE}\s+{_YEAR_RE}", re.IGNORECASE),
]

def _full_year(y: int) -> int:
    if y < 100:
        return y + (2000 if y < 50 else 1900)
    return y

def _month_to_int(m: str) -> Optional[int]:
    if m.isdigit():
        mi = int(m)
        return mi if 1 <= mi <= 12 else None
    return _MONTH_MAP.get(m.lower())

def _normalise_ddmmyyyy(day: int, month: int, year: int) -> Optional[str]:
    y = _full_year(year)
    try:
        dt = datetime(y, month, day)
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        # If invalid calendar date (e.g., 31/06/2019) and we’re allowed to keep it,
        # output the zero-padded dd/mm/yyyy anyway.
        if settings.ALLOW_INVALID:
            return f"{day:02d}/{month:02d}/{y:04d}"
        return None

def normalise_dates(candidates: Iterable[str]) -> List[str]:
    out: List[str] = []
    for s in candidates:
        s_clean = re.sub(r"\s+", " ", s.strip())
        normalised: Optional[str] = None

        # Try explicit patterns first (captures sub-dates inside ranges)
        matched_any = False
        for pat in _PATTERNS:
            for m in pat.finditer(s_clean):
                matched_any = True
                d = int(m.group("day"))
                month_raw = m.group("month")
                mi = _month_to_int(month_raw)
                if mi is None:
                    continue
                y = int(m.group("year"))
                n = _normalise_ddmmyyyy(d, mi, y)
                if n:
                    out.append(n)

        # Fallback: attempt whole-string strptime if no pattern hits
        if not matched_any:
            for fmt in _FORMATS:
                try:
                    dt = datetime.strptime(s_clean, fmt)
                    out.append(dt.strftime("%d/%m/%Y"))
                    break
                except Exception:
                    continue
    return out
