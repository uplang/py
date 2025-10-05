# Makefile for UP Python Parser

PYTHON := python3
PIP := $(PYTHON) -m pip

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run tests
	$(PYTHON) -m pytest tests/ -v --cov=src/uplang --cov-report=term-missing

.PHONY: lint
lint: ## Run linters (ruff, mypy, black check)
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m mypy src/
	$(PYTHON) -m black --check src/

.PHONY: build
build: ## Build the package
	$(PYTHON) -m build

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

.PHONY: install
install: ## Install in development mode
	$(PIP) install -e .[dev]

.PHONY: install-prod
install-prod: ## Install production dependencies
	$(PIP) install .

.PHONY: fmt
fmt: ## Format code
	$(PYTHON) -m black src/
	$(PYTHON) -m ruff check --fix src/

.PHONY: publish
publish: build ## Publish to PyPI
	$(PYTHON) -m twine upload dist/*

.PHONY: test-ci
test-ci: ## Run CI tests locally using act (requires: brew install act)
	act --container-architecture linux/amd64 -j test
	act --container-architecture linux/amd64 -j lint

.DEFAULT_GOAL := test
