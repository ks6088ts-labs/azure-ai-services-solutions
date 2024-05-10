using 'main.bicep'

param openAiDeployments = [
  {
    name: 'gpt-35-turbo'
    version: '0613'
    capacity: 30
  }
  {
    name: 'gpt-4'
    version: 'vision-preview'
    capacity: 30
  }
  {
    name: 'text-embedding-ada-002'
    version: '2'
    capacity: 30
  }
]

param tags = {
  environment: 'dev'
}
