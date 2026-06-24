"""
Utilitários para gerenciamento do Model Registry no MLflow.

Centraliza funções auxiliares para operações administrativas em modelos
registrados, como remoção de modelos e definição de aliases.

Este módulo apoia o controle de versões dos modelos usados na
classificação textual de proposições legislativas.
"""

from mlflow.tracking import MlflowClient


def reset_model(model_name):

    client = MlflowClient()

    try:

        client.delete_registered_model(
            model_name
        )

        print(
            f"Modelo removido: {model_name}"
        )

    except Exception:

        print(
            f"Modelo inexistente: {model_name}"
        )


def set_alias(
    model_name,
    alias,
    version
):

    client = MlflowClient()

    client.set_registered_model_alias(
        name=model_name,
        alias=alias,
        version=version
    )