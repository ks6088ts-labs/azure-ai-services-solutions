#!/bin/sh

RESOURCE_GROUP_NAME=$(jq -r '.RESOURCE_GROUP_NAME' < azure-functions.json)

az group delete --name "$RESOURCE_GROUP_NAME" --yes --no-wait
rm azure-functions.json
