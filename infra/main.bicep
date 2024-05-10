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

@description('Specifies the name of the Azure Cognitive Services resource.')
param cognitiveServicesName string = '${prefix}cognitiveServices'

@description('Specifies the name of the Azure Storage Account resource.')
param storageAccountName string = '${prefix}sa'

@description('Specifies the name of the Azure Event Grid resource.')
param eventGridName string = '${prefix}eg'

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

module cognitiveServices './modules/cognitiveServices.bicep' = {
  name: 'cognitiveServices'
  params: {
    name: cognitiveServicesName
    sku: {
      name: 'S0'
    }
    customSubDomainName: toLower(openAiName)
    location: location
    tags: tags
  }
}

module storageAccount './modules/storageAccount.bicep' = {
  name: 'storageAccount'
  params: {
    name: storageAccountName
    containerNames: [
      'dev'
      'prod'
    ]
    location: location
    tags: tags
  }
}

module eventGrid './modules/eventGrid.bicep' = {
  name: 'eventGrid'
  params: {
    name: eventGridName
    location: location
    tags: tags
  }
}
