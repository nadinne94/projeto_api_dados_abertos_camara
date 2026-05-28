import mlflow


def configure_mlflow(experiment_name):

    mlflow.set_registry_uri(
        "databricks-uc"
    )

    mlflow.set_experiment(
        experiment_name
    )