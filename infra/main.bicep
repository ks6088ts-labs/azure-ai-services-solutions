// Parameters
@description('Specifies the name prefix.')
param prefix string = toLower(uniqueString(resourceGroup().id, location))

@description('Specifies the primary location of Azure resources.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

// OpenAI
@description('Specifies the name of the Azure OpenAI resource.')
param openAiName string = '${prefix}openai'

@description('Specifies the OpenAI deployments to create.')
param openAiDeployments array = []

module openAi './modules/openAi.bicep' = {
  name: 'openAi'
  params: {
    name: openAiName
    sku: {
      name: 'S0'
    }
    customSubDomainName: toLower(openAiName)
    deployments: openAiDeployments
    location: location
    tags: tags
  }
}
