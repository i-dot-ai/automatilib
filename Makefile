test:
	DJANGO_SETTINGS_MODULE=example_project.settings poetry run pytest \
	--cov automatilib --cov-report term-missing --cov-fail-under 90

lint:
	poetry run isort .
	poetry run black .
	poetry run flake8 .
	poetry run mypy automatilib/  --ignore-missing-imports
