# Devopstrio AI Model Registry: One-Touch Provisioner
# Usage: ./provision-aimr.ps1 -Environment prod -AutoApprove

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "test", "prod")]
    [string]$Environment,

    [switch]$AutoApprove
)

Write-Host "🚀 Initializing AI Model Registry (AI-MR) Deployment: [$Environment]" -ForegroundColor Cyan

# 1. Platform Infrastructure (Database & Managed ML)
Write-Host "--- Provisioning Institutional Registry Core ---" -ForegroundColor DarkGray
Set-Location "./terraform/environments/$Environment"
terraform init
if ($AutoApprove) {
    terraform apply -auto-approve
} else {
    terraform apply
}

# 2. Kubernetes Platform Deployment
Write-Host "--- Deploying Registry Management API ---" -ForegroundColor DarkGray
helm upgrade --install ai-model-registry "../../helm/ai-model-registry" --values "../../helm/ai-model-registry/values.yaml" --namespace ai-registry --create-namespace

Write-Host "✅ AI Model Registry [$Environment] is now OPERATIONAL." -ForegroundColor Green
Write-Host "Registry API: https://registry.devopstrio.co.uk"
Write-Host "Serving Hub: https://inference.devopstrio.co.uk"
