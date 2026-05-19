"""
Orquestrador principal da camada Bronze.
"""

from src.config.api_config import (
    API_CONFIG
)

from src.config.dataset_config import (
    DATASETS_CONFIG
)

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.utils.helpers.spark_utils import (
    get_spark
)

from src.utils.monitoring.pipeline_logger import (
    PipelineLogger
)

from src.utils.storage.delta_io import (
    write_table
)

from src.bronze.ingest.ingestion_factory import (
    IngestionFactory
)

from src.bronze.orchestration.dependency_manager import (
    sort_datasets_by_dependency,
)


def run_pipeline(
    dataset: str = "all",
    stop_on_error: bool = False,
):
    """
    Executa pipeline Bronze.
    """

    spark = get_spark()

    logger = PipelineLogger(
        spark=spark,
        log_path=STORAGE_CONFIG["logs"],
    )

    if (

        dataset != "all"

        and

        dataset not in DATASETS_CONFIG
    ):

        raise ValueError(
            f"Dataset inválido: {dataset}"
        )

    datasets = (

        {dataset: DATASETS_CONFIG[dataset]}

        if dataset != "all"

        else DATASETS_CONFIG
    )

    ordered_datasets = (
        sort_datasets_by_dependency(
            datasets
        )
    )

    logger.log_info(
        "bronze",
        "pipeline",
        f"Datasets={len(ordered_datasets)}"
    )

    logger.log_start(
        "bronze",
        "pipeline"
    )

    for dataset_name, config in ordered_datasets:

        try:

            df = IngestionFactory.execute(

                spark=spark,

                dataset_name=dataset_name,

                config=config,

                api_config=API_CONFIG,

                storage_config=STORAGE_CONFIG,

                logger=logger,
            )

            if df is None:

                continue

            logger.log_info(
                "bronze",
                dataset_name,
                "Iniciando persistência"
            )

            records = df.count()

            write_table(
                spark=spark,
                df=df,
                storage_config=STORAGE_CONFIG,
                layer="bronze",
                table_name=dataset_name,
            )

            logger.log_success(
                "bronze",
                dataset_name,
                records,
            )

        except Exception as exc:

            logger.log_error(
                "bronze",
                dataset_name,
                str(exc),
                exc,
            )

            if stop_on_error:
                raise

    logger.log_success(
        "bronze",
        "pipeline",
    )


if __name__ == "__main__":

    run_pipeline()