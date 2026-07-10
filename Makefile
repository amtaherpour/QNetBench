.PHONY: install test lint format-check

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check .

format-check:
	python -m ruff format --check .
