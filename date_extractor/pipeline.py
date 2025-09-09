from __future__ import annotations
import logging
from typing import Dict, List
from . import preprocess
from . import extractor_spacy
from . import postprocess
from .validators import has_any_digits
from .schema import ExtractionResult
from .config import settings

logger = logging.getLogger(__name__)

def extract_dates(text: str) -> Dict[str, List[str] | str]:
    """Public entry point: returns the required JSON-like structure."""
    raw = text or ""
    cleaned = preprocess.preprocess(raw)
    # Extract candidate date strings using spaCy NER
    # Extract candidate date strings (spaCy or regex fallback)
    candidates = extractor_spacy.extract_date_strings(cleaned)

    normalised = postprocess.normalise_dates(candidates)

    dates = list(dict.fromkeys(normalised)) if settings.DEDUPLICATE else normalised

    if dates:
        result = ExtractionResult(dates=dates, message="Success").model_dump()
    else:
        if has_any_digits(cleaned):
            result = ExtractionResult(dates=[], message="Warning, dates not extracted correctly").model_dump()
        else:
            result = ExtractionResult(dates=[], message="Success").model_dump()
    return result
