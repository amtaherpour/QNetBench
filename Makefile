.PHONY: install lint format-check test diff-check check

install:
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check .

format-check:
	python -m ruff format --check .

test:
	python -m pytest -q

diff-check:
	git diff --check

check: lint format-check test diff-check
