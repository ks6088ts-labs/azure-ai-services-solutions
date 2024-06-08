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
    capacity: 3
  }
]

param tags = {
  environment: 'dev'
}
