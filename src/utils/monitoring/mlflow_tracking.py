"""
Utilitários de configuração do MLflow.

Centraliza a configuração do registry e do experimento utilizados para
rastreamento, registro e versionamento dos modelos de Machine Learning.

Este módulo apoia o treinamento e a inferência dos modelos de
classificação textual.
"""

import mlflow


def configure_mlflow(experiment_name):

    mlflow.set_registry_uri(
        "databricks-uc"
    )

    mlflow.set_experiment(
        experiment_name
    )