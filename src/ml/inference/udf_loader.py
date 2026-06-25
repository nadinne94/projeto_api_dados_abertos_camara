"""
Carregamento de modelos e criação de UDFs de inferência.

Centraliza a leitura de modelos registrados no MLflow e a criação de UDFs
Spark usadas para aplicar classificação textual em DataFrames.

Este módulo permite integrar os modelos de Machine Learning ao fluxo de
transformação da camada Gold.
"""

import os
import traceback

import mlflow
import mlflow.sklearn
import pandas as pd
from dotenv import load_dotenv

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StringType


load_dotenv()

_MODEL_CACHE = {}


def load_model(
    model_name: str,
    model_alias: str | None = None,
    registry_uri: str | None = None
):
    """Carrega e mantém em cache um modelo MLflow por nome e alias.

    Parâmetros:
        model_name: Nome do modelo registrado.
        model_alias: Alias do modelo usado para inferência.
        registry_uri: MLflow registry URI.

    Retorna:
        Loaded scikit-learn compatible model.
    """
    model_alias = model_alias or os.getenv("MLFLOW_MODEL_ALIAS", "champion")
    registry_uri = registry_uri or os.getenv("MLFLOW_REGISTRY_URI", "databricks-uc")

    mlflow.set_registry_uri(
        registry_uri
    )

    model_uri = f"models:/{model_name}@{model_alias}"

    if model_uri not in _MODEL_CACHE:

        print(
            f"[MLFLOW] Loading model: {model_uri}"
        )

        _MODEL_CACHE[model_uri] = mlflow.sklearn.load_model(
            model_uri
        )

    return _MODEL_CACHE[model_uri]


def create_classification_udf(
    model_name: str,
    model_alias: str | None = None,
    fallback: str = "Não Classificado",
    registry_uri: str | None = None
):
    """Cria uma pandas UDF para inferência em lote no Spark.

    Parâmetros:
        model_name: Nome do modelo registrado.
        model_alias: Alias do modelo usado para inferência.
        fallback: Value returned when a prediction is missing.
        registry_uri: MLflow registry URI.

    Retorna:
        pandas UDF that receives text values and returns predicted labels.
    """

    @pandas_udf(StringType())
    def classify_with_ml(
        texts: pd.Series
    ) -> pd.Series:

        try:

            model = load_model(
                model_name=model_name,
                model_alias=model_alias,
                registry_uri=registry_uri
            )

            clean_texts = (
                texts
                .fillna("")
                .astype(str)
                .str.strip()
            )

            predictions = model.predict(
                clean_texts
            )

            return (
                pd.Series(predictions)
                .fillna(fallback)
                .astype(str)
            )

        except Exception as exc:

            error = traceback.format_exc()

            raise RuntimeError(
                f"Erro inferência ML "
                f"[{model_name}@{model_alias}]\n{error}"
            ) from exc

    return classify_with_ml