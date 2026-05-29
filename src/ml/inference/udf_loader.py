import traceback
import mlflow
import mlflow.sklearn
import pandas as pd

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StringType


_MODEL_CACHE = {}


def carregar_modelo(
    model_name: str,
    model_alias: str = "champion",
    registry_uri: str = "databricks-uc"
):
    """Load and cache an MLflow model by name and alias.

    Args:
        model_name: Registered model name.
        model_alias: Model alias used for inference.
        registry_uri: MLflow registry URI.

    Returns:
        Loaded scikit-learn compatible model.
    """
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


def criar_udf_classificacao(
    model_name: str,
    model_alias: str = "champion",
    fallback: str = "Não Classificado",
    registry_uri: str = "databricks-uc"
):
    """Create a pandas UDF for Spark batch inference.

    Args:
        model_name: Registered model name.
        model_alias: Model alias used for inference.
        fallback: Value returned when a prediction is missing.
        registry_uri: MLflow registry URI.

    Returns:
        pandas UDF that receives text values and returns predicted labels.
    """

    @pandas_udf(StringType())
    def classificar_ml(
        texts: pd.Series
    ) -> pd.Series:

        try:

            model = carregar_modelo(
                model_name=model_name,
                model_alias=model_alias,
                registry_uri=registry_uri
            )

            textos_limpos = (
                texts
                .fillna("")
                .astype(str)
                .str.strip()
            )

            predictions = model.predict(
                textos_limpos
            )

            return (
                pd.Series(predictions)
                .fillna(fallback)
                .astype(str)
            )

        except Exception as exc:

            erro = traceback.format_exc()

            raise RuntimeError(
                f"Erro inferência ML "
                f"[{model_name}@{model_alias}]\n{erro}"
            ) from exc

    return classificar_ml