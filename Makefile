.PHONY: install
install:
	$(call log, installing packages)
	poetry install --no-dev


.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
	poetry run black .
	poetry run isort .
	poetry run ruff check . --fix --exit-zero
	poetry run pre-commit run --all
	poetry run mypy .

.PHONY: migrations
migrations:
	$(call log, Started make migrations)
	poetry run alembic -c app/alembic.ini revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

.PHONY: migrate
migrate:
	$(call log, Started migrate)
	poetry run alembic -c app/alembic.ini upgrade head

.PHONY: run
run:
	poetry run python app/run.py
