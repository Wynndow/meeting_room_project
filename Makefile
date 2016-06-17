SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)

run_app:
	python manage.py runserver

test: test_pep8 test_unit

virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && virtualenv venv || true

test_pep8: virtualenv
	${VIRTUALENV_ROOT}/bin/pep8 .

test_unit: virtualenv
	${VIRTUALENV_ROOT}/bin/py.test ${PYTEST_ARGS}
