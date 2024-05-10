// Parameters
@description('Specifies the name prefix.')
param prefix string = uniqueString(resourceGroup().id)

@description('Specifies the primary location of Azure resources.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

@description('Specifies the name of the Azure resource.')
param name string = '${prefix}-eventgrid-topic'

resource eventGridTopic 'Microsoft.EventGrid/topics@2024-06-01-preview' = {
  name: name
  location: location
  tags: tags
  kind: 'Azure'
  sku: {
    name: 'Basic'
  }
  properties: {
    inputSchema: 'EventGridSchema'
    minimumTlsVersionAllowed: '1.0'
  }
}
