.PHONY: help install sync-requirements dev clean run build deploy

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep --extended-regexp --no-filename '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

sync-requirements: ## Sync requirements.txt from pyproject.toml
	uv pip compile pyproject.toml -o requirements.txt

dev: ## Install with dev dependencies
	uv sync --all-extras

run: ## Run the application locally
	uv run mesop app.py

build: sync-requirements ## Build MTA archive
	@echo "Building MTA archive..."
	cd deploy && mbt build

deploy: build ## Deploy to Cloud Foundry
	@echo "Deploying to Cloud Foundry..."
	cd deploy && cf deploy mta_archives/ai-agent-demo_1.0.0.mtar -f

clean: ## Clean build artifacts
	rm -rf .venv/ __pycache__/ tools/__pycache__/ *.egg-info/ uv.lock deploy/mta_archives/ deploy/.che/
