using 'main.bicep'

param openAiDeployments = [
  {
    name: 'gpt-4o'
    version: '2024-05-13'
    capacity: 30
  }
  {
    name: 'text-embedding-3-large'
    version: '1'
    capacity: 30
  }
  {
    name: 'whisper'
    version: '001'
    capacity: 1
  }
]

// To create certificate, overwrite the default value of the parameter by the output from the following command:
// $ cat ~/.step/certs/intermediate_ca.crt | tr -d "\n"
// ref. https://github.com/ks6088ts-labs/azure-iot-scenarios/tree/main/scenarios/3_event-grid-mqtt-messaging
param eventGridMqttEncodedCertificate = ''

param tags = {
  environment: 'dev'
}
