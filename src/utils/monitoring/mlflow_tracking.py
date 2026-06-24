"""
Utilitários de configuração do MLflow.

Centraliza a configuração do registry e do experimento utilizados para
rastreamento, registro e versionamento dos modelos de Machine Learning.

Este módulo apoia o treinamento e a inferência dos modelos de
classificação textual.
"""

import os

import mlflow
from dotenv import load_dotenv


load_dotenv()


def configure_mlflow(experiment_name: str | None = None) -> None:
    """Configura registry e experimento do MLflow."""

    mlflow.set_registry_uri(
        os.getenv("MLFLOW_REGISTRY_URI", "databricks-uc")
    )

    mlflow.set_experiment(
        experiment_name
        or os.getenv("MLFLOW_EXPERIMENT_NAME", "/Shared/api_dados_abertos_ml")
    )