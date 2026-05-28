import mlflow
import mlflow.sklearn

from mlflow.models.signature import (
    infer_signature
)

from src.utils.monitoring.mlflow_registry import (
    set_alias
)


def registrar_execucao(
    resultado,
    config
):

    model_name = config["model_name"]

    pipeline = resultado["pipeline"]

    X_test = resultado["X_test"]

    report = resultado["report"]

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

        clf = pipeline.named_steps[
            "clf"
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