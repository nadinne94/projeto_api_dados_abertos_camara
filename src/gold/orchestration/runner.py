import time
from datetime import datetime

from pyspark.sql import SparkSession

from src.config.dataset_config import DATASETS_CONFIG
from src.config.project_config import STORAGE_CONFIG

from src.utils.storage.delta_io import (
    read_table,
    merge_table
)

from src.utils.monitoring.pipeline_logger import (
    PipelineLogger
)

from src.gold.registry.registry import (
    TRANSFORMS
)


LAYER = "gold"


def _now():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def _print_step(
    dataset: str,
    message: str
):
    print(
        f"[{_now()}] [GOLD] [{dataset}] {message}",
        flush=True
    )


def _validar_dataset(
    dataset: str,
    logger: PipelineLogger
) -> bool:

    if dataset not in DATASETS_CONFIG:

        message = "Dataset não configurado em DATASETS_CONFIG"

        _print_step(
            dataset,
            f"AVISO: {message}"
        )

        logger.log_warning(
            LAYER,
            dataset,
            message
        )

        return False

    if dataset not in TRANSFORMS:

        message = "Transformação não registrada em TRANSFORMS"

        _print_step(
            dataset,
            f"AVISO: {message}"
        )

        logger.log_warning(
            LAYER,
            dataset,
            message
        )

        return False

    return True


def _resolver_datasets(
    dataset_name
):

    if dataset_name == "all":

        return list(
            TRANSFORMS.keys()
        )

    if isinstance(
        dataset_name,
        str
    ):

        return [
            dataset_name
        ]

    return list(
        dataset_name
    )


def run_gold(
    dataset_name="all"
):

    spark = SparkSession.builder.getOrCreate()

    logger = PipelineLogger(
        spark,
        STORAGE_CONFIG["logs"]
    )

    datasets = _resolver_datasets(
        dataset_name
    )

    total_datasets = len(
        datasets
    )

    print(
        "\n"
        "==================================================\n"
        "INICIANDO PIPELINE GOLD\n"
        f"Datasets: {datasets}\n"
        f"Total datasets: {total_datasets}\n"
        f"Execution ID: {logger.execution_id}\n"
        "==================================================\n",
        flush=True
    )

    pipeline_start = time.time()

    for index, dataset in enumerate(
        datasets,
        start=1
    ):

        dataset_start = time.time()

        _print_step(
            dataset,
            f"Iniciando dataset {index}/{total_datasets}"
        )

        if not _validar_dataset(
            dataset,
            logger
        ):

            _print_step(
                dataset,
                "Pulando dataset por falha de validação"
            )

            continue

        cfg = DATASETS_CONFIG[
            dataset
        ]

        transform_cfg = TRANSFORMS[
            dataset
        ]

        table_name = cfg[
            "table"
        ]

        merge_keys = transform_cfg[
            "merge_keys"
        ]

        try:

            logger.log_start(
                LAYER,
                dataset
            )

            logger.log_info(
                LAYER,
                dataset,
                f"Tabela silver: {table_name}"
            )

            logger.log_info(
                LAYER,
                dataset,
                f"Merge keys: {merge_keys}"
            )

            # ======================================
            # READ SILVER
            # ======================================

            _print_step(
                dataset,
                f"Lendo silver.{table_name}"
            )

            read_start = time.time()

            df_silver = read_table(
                spark,
                STORAGE_CONFIG,
                "silver",
                table_name
            )

            silver_count = df_silver.count()

            read_duration = time.time() - read_start

            _print_step(
                dataset,
                f"Silver lida com {silver_count} registros "
                f"em {read_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                dataset,
                "READ_SILVER_SUCCESS",
                f"silver.{table_name} lida com sucesso",
                records=silver_count
            )

            if silver_count == 0:

                message = "Tabela silver vazia"

                _print_step(
                    dataset,
                    f"AVISO: {message}"
                )

                logger.log_warning(
                    LAYER,
                    dataset,
                    message
                )

                continue

            # ======================================
            # TRANSFORM
            # ======================================

            _print_step(
                dataset,
                "Iniciando transformação gold"
            )

            transform_start = time.time()

            df_gold = transform_cfg["fn"](
                df_silver
            )

            df_gold.cache()

            gold_count = df_gold.count()

            transform_duration = (
                time.time()
                - transform_start
            )

            _print_step(
                dataset,
                f"Transformação concluída com {gold_count} registros "
                f"em {transform_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                dataset,
                "TRANSFORM_SUCCESS",
                "Transformação gold concluída",
                records=gold_count
            )

            if gold_count == 0:

                message = "DataFrame gold vazio após transformação"

                _print_step(
                    dataset,
                    f"AVISO: {message}"
                )

                logger.log_warning(
                    LAYER,
                    dataset,
                    message
                )

                df_gold.unpersist()

                continue

            # ======================================
            # WRITE GOLD
            # ======================================

            _print_step(
                dataset,
                f"Gravando gold.{table_name} com merge_keys={merge_keys}"
            )

            write_start = time.time()

            merge_table(
                spark=spark,
                df=df_gold,
                storage_config=STORAGE_CONFIG,
                layer="gold",
                table_name=table_name,
                merge_keys=merge_keys
            )

            write_duration = time.time() - write_start

            _print_step(
                dataset,
                f"Gravação concluída em {write_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                dataset,
                "WRITE_GOLD_SUCCESS",
                f"gold.{table_name} gravada com sucesso",
                records=gold_count
            )

            # ======================================
            # SUCCESS
            # ======================================

            dataset_duration = (
                time.time()
                - dataset_start
            )

            logger.log_success(
                LAYER,
                dataset,
                gold_count
            )

            _print_step(
                dataset,
                f"Dataset concluído com sucesso em {dataset_duration:.1f}s"
            )

            df_gold.unpersist()

        except Exception as exc:

            dataset_duration = (
                time.time()
                - dataset_start
            )

            _print_step(
                dataset,
                f"ERRO após {dataset_duration:.1f}s: {type(exc).__name__}: {exc}"
            )

            logger.log_error(
                LAYER,
                dataset,
                "Falha no processamento gold",
                exc
            )

            raise

    pipeline_duration = (
        time.time()
        - pipeline_start
    )

    print(
        "\n"
        "==================================================\n"
        "PIPELINE GOLD FINALIZADO\n"
        f"Duração total: {pipeline_duration:.1f}s\n"
        f"Execution ID: {logger.execution_id}\n"
        "==================================================\n",
        flush=True
    )
datasets = ['eventos']
for dataset in datasets:
    run_gold(dataset)