# Devopstrio AI-MR: High-Performance ML Serving Tier
# Purpose: Managed Online Endpoints for Model Inference

resource "azurerm_machine_learning_workspace" "mlw" {
  name                    = "mlw-devopstrio-prod"
  location                = var.location
  resource_group_name     = var.resource_group_name
  application_insights_id = var.app_insights_id
  key_vault_id            = var.key_vault_id
  storage_account_id      = var.storage_account_id

  identity {
    type = "SystemAssigned"
  }
}

# Managed Online Endpoint (Global Inference Hub)
resource "azurerm_machine_learning_online_endpoint" "inference" {
  name                  = "mep-ai-registry-prod"
  location              = var.location
  workspace_id          = azurerm_machine_learning_workspace.mlw.id
  auth_mode             = "Key"
  
  traffic {
    # Defaulting all traffic to the current stable model
    label_values = {
      "stable" = 100
    }
  }
}

output "workspace_id" {
  value = azurerm_machine_learning_workspace.mlw.id
}

output "endpoint_uri" {
  value = azurerm_machine_learning_online_endpoint.inference.scoring_uri
}
