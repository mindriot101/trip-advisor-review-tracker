all: help

help:
	@echo  "Tasks: test coverage lint compile-packages sync-packages"

test:
	py.test testing

coverage:
	py.test --cov fetch_latest.py --cov-report html --cov-report term testing

lint:
	flake8 --max-complexity 10 fetch_latest.py {toxinidir}/testing \
		--max-line-length 90

compile-packages:
	pip-compile --no-index

sync-packages:
	pip-sync

.PHONY: help test coverage lint compile-packages sync-packages
