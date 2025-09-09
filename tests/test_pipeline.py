import json
import re
import os
from date_extractor.pipeline import extract_dates

def _is_ddmmyyyy(s: str) -> bool:
    return bool(re.match(r"^\d{2}/\d{2}/\d{4}$", s))

def test_examples_happy_path():
    r1 = extract_dates("The policy provides cover from 31st June 2019 to 1st July 2022 inclusive")
    assert "dates" in r1 and isinstance(r1["dates"], list)
    assert "message" in r1
    # Normalised format
    for d in r1["dates"]:
        assert _is_ddmmyyyy(d)

    r2 = extract_dates("Policy terms from 1/1/2021 to 31/12/2022")
    assert r2["dates"]
    for d in r2["dates"]:
        assert _is_ddmmyyyy(d)

def test_warning_when_digits_but_no_dates():
    r = extract_dates("Policy ref 123456789; see code ABC.")
    assert r["dates"] == []
    assert "Warning" in r["message"]
