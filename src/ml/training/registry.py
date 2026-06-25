"""
Registro dos modelos no MLflow.

Centraliza funções responsáveis por registrar modelos treinados, definir
aliases e organizar versões usadas posteriormente na inferência.

Este módulo apoia o controle de versões dos classificadores de tema e
natureza jurídica.
"""


import mlflow
import mlflow.sklearn

from mlflow.models.signature import (
    infer_signature
)

from src.utils.monitoring.mlflow_registry import (
    set_alias
)


def register_run(
    training_result,
    config
):

    model_name = config["model_name"]

    pipeline = training_result["pipeline"]

    X_test = training_result["X_test"]

    report = training_result["report"]

    predictions = pipeline.predict(
        X_test
    )

    signature = infer_signature(

        model_input=X_test,

        model_output=predictions
    )

    with mlflow.start_run(

        run_name=model_name
    ):

        # ==========================
        # METRICS
        # ==========================

        mlflow.log_metric(

            "accuracy",

            report["accuracy"]
        )

        if "macro avg" in report:

            mlflow.log_metric(

                "macro_f1",

                report["macro avg"]["f1-score"]
            )

        # ==========================
        # PARAMS
        # ==========================

        tfidf = pipeline.named_steps[
            "tfidf"
        ]

        mlflow.log_params({

            "max_features":
                tfidf.max_features,

            "ngram_range":
                str(
                    tfidf.ngram_range
                ),

            "min_df":
                tfidf.min_df,

            "classifier":
                "LogisticRegression"
        })

        # ==========================
        # MODEL
        # ==========================

        model_info = (

            mlflow.sklearn.log_model(

                sk_model=pipeline,

                artifact_path="model",

                signature=signature
            )
        )

        # ==========================
        # REGISTER
        # ==========================

        registered = (

            mlflow.register_model(

                model_uri=model_info.model_uri,

                name=model_name
            )
        )

        version = (
            registered.version
        )

        set_alias(

            model_name=model_name,

            alias="champion",

            version=version
        )

        return {

            "model_name":
                model_name,

            "version":
                version
        }