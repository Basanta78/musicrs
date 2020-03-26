SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

last_tag := $(shell git tag --sort=-creatordate | head -n 1)
new_tag := $(shell semver bump patch "${last_tag}")
timestamp := $(shell date -u +%Y%m%d%H%M%S)
# The new version is tagged as pre-release for master. Once we are good to go for production, remove the -prerelease suffix
new_version := $(shell if [ "${TRAVIS_BRANCH}" = "master" ]; then echo "${new_tag}-alpha.${timestamp}"; else echo "${new_tag}-${TRAVIS_BRANCH}.${timestamp}"; fi)
COLOR=\x1b[36m
NO_COLOR=\x1b[m]

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

.PHONY: build
## Build the docker container.
build:
	@docker build --no-cache --target=test -t musicrs:test .
	@docker build --no-cache --target=main -t musicrs .

.PHONY: test
## Test application in docker container.
test:
	@docker build --target=test -t musicrs:test .
	@docker run musicrs:test

.PHONY: all test clean

.PHONY: format
## Format the code.
format:
	@black .

.PHONY: check
## Check the code.
check:
	@black --check --diff .
	@npm run typecheck

.DEFAULT_GOAL := help

