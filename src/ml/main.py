"""
Ponto de entrada do pipeline de Machine Learning.

Executa o fluxo principal de treinamento e registro dos modelos de
classificação textual utilizados no projeto.

Este módulo orquestra a preparação da base de treino, criação de labels,
treinamento, avaliação e registro dos modelos no MLflow.
"""


import os

from dotenv import load_dotenv

from src.ml.config.training_configs import CLASSIFICADORES_PROPOSICOES
from src.ml.orchestration.training_runner import executar_lote_treinamento


load_dotenv()

EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "/Shared/api_dados_abertos_ml",
)


def main() -> None:
    """Executa o lote de treinamento dos classificadores configurados."""

    executar_lote_treinamento(
        configs=CLASSIFICADORES_PROPOSICOES,
        experiment_name=EXPERIMENT_NAME,
    )


if __name__ == "__main__":
    main()