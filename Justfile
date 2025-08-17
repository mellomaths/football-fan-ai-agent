

lint-fix:
    @echo "Running linters with auto-fix..."
    @just lint-ruff-fix
    @just lint-black-fix
    @echo "All linters fixed successfully."

lint-ruff-fix:
    ruff check --fix

lint-black-fix:
    black . --exclude venv
    @echo "Black formatting applied."

lint-isort-fix:
    isort .

lint: lint-ruff lint-flake8 lint-pylint lint-black
    @echo "All linters passed successfully."

lint-ruff:
    ruff check

lint-flake8:
    flake8

lint-pylint:
    pylint .

lint-black:
    black --check
