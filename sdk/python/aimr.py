import requests
import json
import logging
from typing import Dict, Any, Optional

# AI Model Registry (AI-MR) - Native Python SDK
# Master Command: Register & Govern Intelligent Assets

class RegistryClient:
    def __init__(self, api_base_url: str, api_token: str):
        self.base_url = api_base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger("AI-MR-SDK")

    def register_model(self, name: str, team: str, tags: Optional[Dict] = None) -> str:
        """Registers a centralized model record in the institutional registry."""
        payload = {"name": name, "owner_team": team, "tags": tags or {}}
        response = requests.post(f"{self.base_url}/api/v1/models/register", json=payload, headers=self.headers)
        response.raise_for_status()
        model_id = response.json().get("model_id")
        self.logger.info(f"✅ Model registered successfully: {model_id}")
        return model_id

    def upload_version(self, model_id: str, version: str, artifact_uri: str, metrics: Dict[str, float]) -> str:
        """Appends a new semantic version to an existing model lineage."""
        payload = {
            "version_tag": version,
            "artifact_uri": artifact_uri,
            "framework": "PyTorch", # Default to institutional standard
            "metrics": metrics
        }
        response = requests.post(f"{self.base_url}/api/v1/models/{model_id}/versions", json=payload, headers=self.headers)
        response.raise_for_status()
        self.logger.info(f"✅ Version {version} uploaded for Model {model_id}")
        return response.json().get("version_id")

# SDK Usage Pattern:
# client = RegistryClient("https://registry.devopstrio.co.uk", "dt_key_...")
# m_id = client.register_model("churn-predictor", "Retention-Team")
# v_id = client.upload_version(m_id, "1.2.0", "azure://staimr/models/weights.bin", {"accuracy": 0.94})
