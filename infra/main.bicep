// Parameters
@description('Specifies the name prefix.')
param prefix string = toLower(uniqueString(resourceGroup().id, location))

@description('Specifies the primary location of Azure resources.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

@description('Specifies the name of the Azure OpenAI resource.')
param openAiName string = '${prefix}openai'

@description('Specifies the OpenAI deployments to create.')
param openAiDeployments array = []

@description('Specifies the OpenAI location to deploy to')
param openAiLocation string = 'eastus2'

@description('Specifies the name of the Azure Cognitive Services resource.')
param cognitiveServicesName string = '${prefix}aiServices'

@description('Specifies the location of the Azure Cognitive Services resource.')
param cognitiveServicesLocation string = 'eastus'

@description('Specifies the name of the Azure Storage Account resource.')
param storageAccountName string = '${prefix}sa'

@description('Specifies the name of the Azure Event Grid resource.')
param eventGridName string = '${prefix}eg'

@description('Specifies the name of the Azure Event Grid MQTT resource.')
param eventGridMqttName string = '${prefix}egmqtt'

@description('Specifies the name of the encoded certificate.')
param eventGridMqttEncodedCertificate string

@description('Specifies the name of the Azure Cosmos DB resource.')
param cosmosDbName string = '${prefix}cosmosdb'

@description('Specifies the name of the Azure IoT Hub resource.')
param iotHubName string = '${prefix}iothub'

@description('Specifies the name of the Azure Log Analytics workspace.')
param logAnalyticsWorkspaceName string = '${prefix}law'

module openAi './modules/openAi.bicep' = {
  name: 'openAi'
  params: {
    name: openAiName
    sku: {
      name: 'S0'
    }
    customSubDomainName: toLower(openAiName)
    deployments: openAiDeployments
    location: openAiLocation
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
    customSubDomainName: toLower(cognitiveServicesName)
    location: cognitiveServicesLocation
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

module eventGridMqtt './modules/eventGridMqtt.bicep' = {
  name: 'eventGridMqtt'
  params: {
    name: eventGridMqttName
    location: location
    tags: tags
    encodedCertificate: eventGridMqttEncodedCertificate
  }
}

module cosmosDb './modules/cosmosDb.bicep' = {
  name: 'cosmosDb'
  params: {
    name: cosmosDbName
    location: location
    tags: tags
    primaryRegion: location
    secondaryRegion: 'japanwest'
  }
}

module iotHub './modules/iotHub.bicep' = {
  name: 'iotHub'
  params: {
    name: iotHubName
    location: location
    tags: tags
    workspaceId: logAnalytics.outputs.id
  }
}

module logAnalytics './modules/logAnalytics.bicep' = {
  name: 'logAnalytics'
  params: {
    name: logAnalyticsWorkspaceName
    location: location
    tags: tags
  }
}

// Output
output cognitiveServicesName string = cognitiveServices.outputs.name
output cognitiveServicesEndpoint string = cognitiveServices.outputs.endpoint
output eventGridTopicName string = eventGrid.outputs.eventGridTopicName
output eventGridTopicEndpoint string = eventGrid.outputs.eventGridTopicEndpoint
output openAiName string = openAi.outputs.name
output openAiEndpoint string = openAi.outputs.endpoint
output storageAccountName string = storageAccount.outputs.name
output iotHubName string = iotHub.outputs.iotHubName
