.PHONY: install update format lint doc test run bench

install:
	uv sync --frozen --no-install-project
	uv run pre-commit install

update:
	uv lock --upgrade

format:
	uv run ruff format && uv run ruff check --fix --select I

lint:
	uv run ruff check --fix

run:
	uv run gunicorn --worker-class server.AppUvicornWorker app.main:app

test:
	uv run pytest tests/
