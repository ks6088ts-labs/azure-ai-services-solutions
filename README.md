[![test](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/azure-ai-services-solutions/actions/workflows/docker-release.yaml)

# azure-ai-services-solutions

This repository contains a collection of solutions that leverage Azure AI services.

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [GNU Make](https://www.gnu.org/software/make/)

## Development instructions

### Local development

Use Makefile to run the project locally.

```shell
# help
make

# install dependencies for development
make install-deps-dev

# run tests
make test

# run CI tests
make ci-test
```

### Docker development

```shell
# build docker image
make docker-build

# run docker container
make docker-run

# run CI tests in docker container
make ci-test-docker
```

### Run local test

Currently almost all tests won't run on CI because it consumes Azure resources.
To run the tests locally, follow the steps below.

```shell
# Run test if RUN_TEST is defined
export RUN_TEST=1

make test
```

## Deployment instructions

### Docker compose

Docker compose is used to run the services locally.
Refer to the following steps to run the services.
See the actual implementation in the [compose.yaml](./compose.yaml) file.

```shell
# Create environment files for each service
cp {NAME}.env.sample {NAME}.env

# Build and run the services
docker compose up
```

### Push docker image to Docker Hub

To publish the docker image to Docker Hub via GitHub Actions, you need to set the following secrets in the repository.

```shell
gh secret set DOCKERHUB_USERNAME --body $DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN --body $DOCKERHUB_TOKEN
```

### Deploy Azure Functions

To deploy the Azure Functions, run the following script.

```shell
# Deploy the Azure Functions
sh ./scripts/deploy-azure-functions.sh

# Destroy the Azure Functions
sh ./scripts/destroy-azure-functions.sh
```

- [scripts/deploy-azure-functions.sh](./scripts/deploy-azure-functions.sh): Deploy the Azure Functions using Azure CLI.
- [scripts/destroy-azure-functions.sh](./scripts/destroy-azure-functions.sh): Destroy the Azure Functions using Azure CLI.
