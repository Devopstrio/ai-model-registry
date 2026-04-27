// Devopstrio AI Model Registry: Master Bicep Template
// Architecture: Native Intelligence Governance

targetScope = 'subscription'

param location string = 'uksouth'
param prefix string = 'aimr'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${prefix}-platform-prod'
  location: location
}

// 1. Registry Database (PostgreSQL)
module database './modules/data.bicep' = {
  scope: rg
  name: 'dbDeploy'
  params: {
    location: location
    serverName: 'psql-${prefix}-prod'
  }
}

// 2. ML Serving Hub (Workspace & Endpoints)
module ml './modules/ml.bicep' = {
  scope: rg
  name: 'mlDeploy'
  params: {
    location: location
    workspaceName: 'mlw-${prefix}-prod'
  }
}

output registryUrl string = 'https://registry-${prefix}.devopstrio.co.uk'
