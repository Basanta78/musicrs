SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

.PHONY: clean
## Clean the pycache folder and pyc files.
clean:
	@rm -rf $(TMP_PATH) ./**/*.pyc __pycache__ **/__pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

.PHONY: venv
## Create virtual environment for python.
venv:
	@virtualenv -p python3 $(VENV_PATH)

.PHONY: setup
## Setup the application by installing the packages.
setup:
	@pip install -U -e .[dev]
	@npm install

.PHONY: venv_test
## Test for virtual environment.
venv_test:
	@pytest -vvv

.PHONY: format
## Format the code.
format:
	@black .

.PHONY: check
## Check the code.
check:
	@black --check --diff .

.DEFAULT_GOAL := help

