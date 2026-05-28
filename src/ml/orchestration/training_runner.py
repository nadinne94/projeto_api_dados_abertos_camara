import time
import mlflow

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.ml.training.base_generator import (
    gerar_base_treino
)

from src.ml.training.trainer import (
    executar_treino
)

from src.ml.training.registry import (
    registrar_execucao
)

from src.utils.monitoring.mlflow_registry import (
    reset_model
)

from src.utils.monitoring.mlflow_tracking import (
    configure_mlflow
)

from src.utils.monitoring.pipeline_logger import (
    PipelineLogger
)


REQUIRED_CONFIG_KEYS = [

    "model_name",

    "target_col",

    "tabela_treino",

    "source_table",

    "regex_func"
]


def validar_config(
    config: dict
):

    missing = [

        key

        for key in REQUIRED_CONFIG_KEYS

        if key not in config
    ]

    if missing:

        raise ValueError(
            f"Config incompleta. Campos ausentes: {missing}"
        )


def logar_distribuicao_classes(
    df,
    target_col: str
):

    return {

        row[target_col]: row["count"]

        for row in (
            df
            .groupBy(target_col)
            .count()
            .collect()
        )
    }


def executar_pipeline_treino(
    config
):

    validar_config(
        config
    )

    spark = SparkSession.getActiveSession()

    if spark is None:

        raise RuntimeError(
            "Nenhuma SparkSession ativa encontrada."
        )

    model_name = config["model_name"]
    target_col = config["target_col"]

    logger = PipelineLogger(
        spark=spark,
        log_path=STORAGE_CONFIG["logs"]
    )

    start_time = time.time()

    try:

        if mlflow.active_run():

            mlflow.end_run()

        logger.log_start(
            "ML_PIPELINE",
            model_name
        )

        if config.get("reset", False):

            logger.log_event(
                "ML_PIPELINE",
                model_name,
                "RESET_START"
            )

            reset_model(
                model_name
            )

            logger.log_event(
                "ML_PIPELINE",
                model_name,
                "RESET_SUCCESS"
            )

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "BASE_START"
        )

        df_train = gerar_base_treino(
            config
        )

        n_records = df_train.count()

        distribuicao = logar_distribuicao_classes(
            df_train,
            target_col
        )

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "BASE_SUCCESS",
            records=n_records
        )

        print(
            f"\nDistribuição treino {model_name}: "
            f"{distribuicao}"
        )

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "TRAIN_START"
        )

        resultado = executar_treino(
            df=df_train,
            target_col=target_col
        )

        accuracy = resultado["report"]["accuracy"]

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "TRAIN_SUCCESS",
            records=resultado["n_samples"]
        )

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "REGISTRY_START"
        )

        version = registrar_execucao(
            resultado,
            config
        )

        logger.log_event(
            "ML_PIPELINE",
            model_name,
            "REGISTRY_SUCCESS"
        )

        duration = time.time() - start_time

        logger.log_success(
            "ML_PIPELINE",
            model_name
        )

        print(
            f"\nSucesso: {model_name} "
            f"(v{version}) "
            f"[{duration:.1f}s] "
            f"acc={accuracy:.4f}"
        )

        return version

    except Exception as exc:

        logger.log_error(
            "ML_PIPELINE",
            model_name,
            "Falha pipeline treino",
            exc
        )

        print(
            f"\nErro em {model_name}: {str(exc)}"
        )

        raise


def executar_lote_treinamento(
    configs,
    experiment_name
):

    configure_mlflow(
        experiment_name
    )

    for config in configs:

        print(
            f"\nRodando pipeline: {config['model_name']}"
        )

        executar_pipeline_treino(
            config
        )