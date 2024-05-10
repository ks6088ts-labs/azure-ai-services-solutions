// Parameters
@description('Specifies the name of the Azure cognitiveServices resource.')
param name string

@description('Specifies the resource model definition representing SKU.')
param sku object = {
  name: 'S0'
}

@description('Specifies the identity of the cognitiveServices resource.')
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

// Resources
resource cognitiveServices 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: name
  location: location
  sku: sku
  kind: 'CognitiveServices'
  identity: identity
  tags: tags
  properties: {
    customSubDomainName: customSubDomainName
    publicNetworkAccess: publicNetworkAccess
  }
}

// Outputs
output id string = cognitiveServices.id
output name string = cognitiveServices.name
output endpoint string = cognitiveServices.properties.endpoint
