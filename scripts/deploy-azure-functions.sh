#!/bin/sh

# Variables
LOCATION=japaneast
RANDOM_SUFFIX=$(openssl rand -hex 4)
RESOURCE_GROUP_NAME="rg-adhoc-azure-functions-$RANDOM_SUFFIX"
STORAGE_NAME=stadhoc"$RANDOM_SUFFIX"
FUNCTION_APP_NAME=adhoc-azure-functions-"$RANDOM_SUFFIX"

# Create a resource group
az group create \
    --name "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION"

# Create a storage account
az storage account create \
    --name "$STORAGE_NAME" \
    --location "$LOCATION" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --sku Standard_LRS

# Create a function app
az functionapp create \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --consumption-plan-location "$LOCATION" \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --name "$FUNCTION_APP_NAME" \
    --os-type linux \
    --storage-account "$STORAGE_NAME"

# create json file containing the resource group name and storage account name
echo "{\"RESOURCE_GROUP_NAME\": \"$RESOURCE_GROUP_NAME\", \"STORAGE_NAME\": \"$STORAGE_NAME\", \"FUNCTION_APP_NAME\": \"$FUNCTION_APP_NAME\"}" > azure-functions.json
