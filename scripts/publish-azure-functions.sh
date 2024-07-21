#!/bin/sh

# Export the dependencies to requirements.txt
poetry export \
    --format requirements.txt \
    --output backend/requirements.txt \
    --with backend,azure-functions \
    --without-hashes

# Publish the Azure Functions
cd backend || exit
FUNCTION_APP_NAME=$(jq -r '.FUNCTION_APP_NAME' < ../azure-functions.json)
func azure functionapp publish $FUNCTION_APP_NAME
