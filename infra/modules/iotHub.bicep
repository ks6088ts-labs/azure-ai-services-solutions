// Parameters
@description('Specifies the name prefix.')
param prefix string = uniqueString(resourceGroup().id)

@description('Specifies the primary location of Azure resources.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

@description('Specifies the name of the Azure resource.')
param name string = '${prefix}-iothub'

@description('The SKU to use for the IoT Hub.')
param skuName string = 'S1'

@description('The number of IoT Hub units.')
param skuUnits int = 1

@description('Specifies the resource id of the Log Analytics workspace.')
param workspaceId string

resource iotHub 'Microsoft.Devices/IotHubs@2023-06-30' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: skuName
    capacity: skuUnits
  }
}

resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diagnosticSettings'
  scope: iotHub
  properties: {
    workspaceId: workspaceId
    metrics: [
      for metric in ['AllMetrics']: {
        category: metric
        enabled: true
        timeGrain: null
      }
    ]
    logs: [
      for categoryGroup in ['allLogs', 'audit']: {
        categoryGroup: categoryGroup
        enabled: true
      }
    ]
  }
}

// Outputs
output iotHubId string = iotHub.id
output iotHubName string = iotHub.name
