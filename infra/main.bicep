param location string = 'japaneast'
param resourceName string = 'myOpenAIService'

resource azureOpenAIServiceAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: resourceName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: azureOpenAIServiceAccount
  name: 'deployment'
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-35-turbo'
      version: '0613'
    }
  }
  sku: {
    name: 'Standard'
    capacity: 20
  }
}
