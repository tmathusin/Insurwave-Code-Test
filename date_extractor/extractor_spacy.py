from __future__ import annotations
import logging, re
from typing import List

logger = logging.getLogger(__name__)

# --- Fallback regex for date-like strings (numeric + month names) ---
_FALLBACK_RE = re.compile(
    r"""
    (?:
        \b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b
      | \b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+\d{2,4}\b
      | \b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2,4}\b
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _fallback_dates(txt: str) -> List[str]:
    return [m.group(0) for m in _FALLBACK_RE.finditer(txt)]

# ---- spaCy (lazy) ----
try:
    import spacy  # type: ignore
except Exception:
    spacy = None  # type: ignore

_NLP = None
def _get_nlp():
    global _NLP
    if spacy is None:
        raise RuntimeError("spaCy not installed")
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP

def extract_date_strings(text: str) -> List[str]:
    """
    Use spaCy NER and regex together. Regex also runs on each spaCy DATE span
    to split ranges like '31 June 2019 to 1 July 2022 inclusive'.
    """
    candidates = []  # merge all sources
    # always collect regex from the full text
    candidates.extend(_fallback_dates(text))

    # try spaCy too (if available)
    try:
        nlp = _get_nlp()
        doc = nlp(text)
        ents = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        candidates.extend(ents)
        # split any range entities into individual dates
        for ent_text in ents:
            candidates.extend(_fallback_dates(ent_text))
    except Exception:
        logger.info("spaCy unavailable; relying on regex only")

    # de-dupe while preserving order
    seen, merged = set(), []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            merged.append(c)
    return merged





