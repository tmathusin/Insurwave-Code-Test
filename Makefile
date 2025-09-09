.PHONY: setup test lint fmt type

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev]" && python -m spacy download en_core_web_sm

test:
	pytest -q

lint:
	ruff check date_extractor tests

fmt:
	black date_extractor tests

type:
	mypy date_extractor
