# Git
GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 --always | sed -e s/v//g)
LOG_LEVEL ?= "INFO"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: info
info: ## show information
	@echo "GIT_REVISION: $(GIT_REVISION)"
	@echo "GIT_TAG: $(GIT_TAG)"

.PHONY: install-deps-dev
install-deps-dev: ## install dependencies for development
	poetry install
	poetry run pre-commit install

.PHONY: install-deps
install-deps: ## install dependencies for production
	poetry install --without dev

.PHONY: format-check
format-check: ## format check
	poetry run black . --check --extend-exclude client/ --verbose

.PHONY: format
format: ## format code
	poetry run isort .
	poetry run black . --extend-exclude client/ --verbose

.PHONY: fix
fix: format ## apply auto-fixes
	poetry run ruff check --fix

.PHONY: lint
lint: ## lint
	poetry run ruff check .
	shellcheck scripts/*.sh

.PHONY: test
test: ## run tests
	poetry run pytest --log-cli-level=$(LOG_LEVEL)

.PHONY: ci-test
ci-test: install-deps-dev format-check lint test ## run CI tests

# ---
# Docker
# ---
DOCKER_REPO_NAME ?= ks6088ts
DOCKER_IMAGE_NAME ?= azure-ai-services-solutions
DOCKER_IMAGE_COMPONENT ?= backend
DOCKER_COMMAND ?=
DOCKER_TAG ?= $(DOCKER_IMAGE_COMPONENT)-$(GIT_TAG)
DOCKER_FILE ?= ./dockerfiles/$(DOCKER_IMAGE_COMPONENT).Dockerfile
DOCKER_COMPOSE_FILE ?= ./compose.yaml

# Tools
TOOLS_DIR ?= $(HOME)/.local/bin
TRIVY_VERSION ?= 0.49.1

.PHONY: docker-build
docker-build: ## build Docker image
	docker build \
		--tag $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) \
		--file $(DOCKER_FILE) \
		--build-arg GIT_REVISION=$(GIT_REVISION) \
		--build-arg GIT_TAG=$(GIT_TAG) \
		--no-cache \
		.

.PHONY: docker-run
docker-run: ## run Docker container
	docker run --rm $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) $(DOCKER_COMMAND)

.PHONY: docker-lint
docker-lint: ## lint Dockerfile
	docker run --rm -i hadolint/hadolint < $(DOCKER_FILE)

.PHONY: docker-compose-lint
docker-compose-lint: ## lint docker compose file
	docker compose --file $(DOCKER_COMPOSE_FILE) config --quiet

.PHONY: docker-scan
docker-scan: ## scan Docker image
	@# https://aquasecurity.github.io/trivy/v0.18.3/installation/#install-script
	@which trivy || curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b $(TOOLS_DIR) v$(TRIVY_VERSION)
	trivy image $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

.PHONY: _ci-test-docker
_ci-test-docker: docker-lint docker-build docker-scan docker-run

.PHONY: ci-test-docker
ci-test-docker: docker-compose-lint ## run CI test for Docker
	$(MAKE) _ci-test-docker DOCKER_IMAGE_COMPONENT=backend
	$(MAKE) _ci-test-docker DOCKER_IMAGE_COMPONENT=frontend

# ---
# Application
# ---
SOLUTION_NAME ?= "SANDBOX"
BACKEND_URL ?= "http://localhost:8000"

.PHONY: backend
backend: ## run backend
	poetry run python main.py backend --reload

.PHONY: frontend
frontend: ## run frontend
	poetry run streamlit run main.py -- frontend -- \
		--solution-name=$(SOLUTION_NAME) \
		--backend-url=$(BACKEND_URL)

# ---
# Azure Functions
# ---
.PHONY: azure-functions-start
azure-functions-start: ## start Azure Functions
	poetry run func start

.PHONY: azure-functions-deploy
azure-functions-deploy: ## deploy Azure Functions resources
	sh ./scripts/deploy-azure-functions.sh

.PHONY: azure-functions-destroy
azure-functions-destroy: ## destroy Azure Functions resources
	sh ./scripts/destroy-azure-functions.sh

.PHONY: azure-functions-functionapp-deploy
azure-functions-functionapp-deploy: ## deploy Azure Functions App
	poetry export \
		--format requirements.txt \
		--output requirements.txt \
		--with backend,azure-functions \
		--without-hashes
	func azure functionapp publish $(shell jq -r '.FUNCTION_APP_NAME' < azure-functions.json)

# ---
# OpenAPI Client
# ---
.PHONY: generate-openapi-spec
generate-openapi-spec: ## generate OpenAPI spec
	poetry run python main.py generate-openapi-spec

.PHONY: generate-openapi-client
generate-openapi-client: ## generate OpenAPI client
	@kiota generate \
		--language Python \
		--class-name ApiClient \
		--namespace-name client \
		--openapi ./specs/openapi.json \
		--output ./client
	@echo "Get the list of dependencies"
	@kiota info -d ./specs/openapi.json --language Python

.PHONY: generate-openapi
generate-openapi: generate-openapi-spec generate-openapi-client ## generate OpenAPI artifacts
