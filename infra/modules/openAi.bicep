// Parameters
@description('Specifies the name of the Azure OpenAI resource.')
param name string

@description('Specifies the resource model definition representing SKU.')
param sku object = {
  name: 'S0'
}

@description('Specifies the identity of the OpenAI resource.')
param identity object = {
  type: 'SystemAssigned'
}

@description('Specifies the location.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

@description('Specifies an optional subdomain name used for token-based authentication.')
param customSubDomainName string = ''

@description('Specifies whether or not public endpoint access is allowed for this account..')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccess string = 'Enabled'

@description('Specifies the OpenAI deployments to create.')
param deployments array = []

// Resources
resource openAi 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: name
  location: location
  sku: sku
  kind: 'OpenAI'
  identity: identity
  tags: tags
  properties: {
    customSubDomainName: customSubDomainName
    publicNetworkAccess: publicNetworkAccess
  }
}

@batchSize(1)
resource model 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = [
  for deployment in deployments: {
    name: deployment.name
    parent: openAi
    properties: {
      model: {
        format: 'OpenAI'
        name: deployment.name
        version: deployment.version
      }
      currentCapacity: deployment.capacity
      raiPolicyName: deployment.?raiPolicyName ?? null
      versionUpgradeOption: deployment.?versionUpgradeOption ?? 'OnceNewDefaultVersionAvailable'
    }
    sku: deployment.?sku ?? {
      name: 'Standard'
      capacity: deployment.capacity
    }
  }
]

// Outputs
output id string = openAi.id
output name string = openAi.name
output endpoint string = openAi.properties.endpoint
