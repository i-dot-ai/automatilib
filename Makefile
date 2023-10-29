test:
	DJANGO_SETTINGS_MODULE=example_project.settings pytest --cov cola --cov-report term-missing --cov-fail-under 80

lint:
	isort .
	black .
	flake8 .
