SERVICE_DIR := src
TESTS_DIR := tests

setup:
	@uv sync

setup-pre-commit:
	@uv run pre-commit install

lint:
	@printf "run ruff check...\n"
	@uv run ruff check --fix --show-fixes --exit-non-zero-on-fix .
	@printf "finish ruff check\n"
	@printf "run mypy...\n"
	@uv run mypy $(SERVICE_DIR)/
	@printf "finish mypy\n"

format:
	@printf "run ruff format...\n"
	@uv run ruff format $(SERVICE_DIR)/ ${TESTS_DIR}/
	@printf "finish ruff format\n"

test:
	@uv run pytest tests --cov $(SERVICE_DIR) -vv

migration:
	@uv run alembic revision --autogenerate

migrate:
	@uv run alembic upgrade head

start:
	@uv run python -m $(SERVICE_DIR).app.runner
