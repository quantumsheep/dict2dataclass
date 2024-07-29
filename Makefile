.PHONY: lint
lint:
	poetry run mypy --install-types --non-interactive .

.PHONY: format
format:
	poetry run ruff format

.PHONY: format-check
format-check:
	poetry run ruff format --check

.PHONY: test
test:
	poetry run python -m unittest discover
