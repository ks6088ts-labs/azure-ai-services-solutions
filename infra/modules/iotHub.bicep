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
param skuName string = 'B1'

@description('The number of IoT Hub units.')
param skuUnits int = 1

resource iotHub 'Microsoft.Devices/IotHubs@2023-06-30' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: skuName
    capacity: skuUnits
  }
}

// Outputs
output iotHubId string = iotHub.id
output iotHubName string = iotHub.name
