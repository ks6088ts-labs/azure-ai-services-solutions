#!/bin/sh

# get the directory of the script
SCRIPT_DIR=$(cd "$(dirname "$0")" || exit; pwd)

# get the name of the current directory
appName=test-$(basename "$(pwd)")

# Azure sign in
az login

# Get the current Azure subscription ID
subscriptionId=$(az account show --query 'id' --output tsv)

# Create a new Azure Active Directory application
appId=$(az ad app create --display-name "$appName" --query appId --output tsv)

# Create a new service principal for the application
assigneeObjectId=$(az ad sp create --id "$appId" --query id --output tsv)

# Assign the 'Contributor' role to the service principal for the subscription
az role assignment create --role contributor \
    --subscription "$subscriptionId" \
    --assignee-object-id "$assigneeObjectId" \
    --assignee-principal-type ServicePrincipal \
    --scope /subscriptions/"$subscriptionId"/resourceGroups/"$appName"

# Assign the 'Contributor' role to the service principal for the subscription
az ad app federated-credential create \
    --id "$appId" \
    --parameters "$SCRIPT_DIR"/credential.json
