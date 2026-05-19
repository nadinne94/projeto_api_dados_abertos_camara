from pyspark.sql import SparkSession

from src.config.dataset_config import DATASETS_CONFIG
from src.config.project_config import STORAGE_CONFIG

from src.utils.storage.delta_io import read_table, merge_table
from src.utils.monitoring.pipeline_logger import PipelineLogger

from src.silver.registry import TRANSFORMS


def run_silver(dataset_name="all"):

    spark = SparkSession.builder.getOrCreate()

    logger = PipelineLogger(
        spark,
        STORAGE_CONFIG["logs"]
    )

    datasets = (
        DATASETS_CONFIG.keys()
        if dataset_name == "all"
        else [dataset_name]
    )

    for dataset in datasets:

        if dataset not in DATASETS_CONFIG:

            logger.log_warning(
                "silver",
                dataset,
                "Dataset não configurado"
            )
            continue

        if dataset not in TRANSFORMS:

            logger.log_warning(
                "silver",
                dataset,
                "Transformação não registrada"
            )
            continue

        try:

            logger.log_start(
                "silver",
                dataset
            )

            cfg = DATASETS_CONFIG[dataset]

            transform_cfg = TRANSFORMS[dataset]

            df_bronze = read_table(
                spark,
                STORAGE_CONFIG,
                "bronze",
                cfg["table"]
            )

            df_silver = transform_cfg["fn"](df_bronze)

            if df_silver.limit(1).count() == 0:

                logger.log_warning(
                    "silver",
                    dataset,
                    "DataFrame vazio"
                )

                continue

            df_silver.cache()

            record_count = df_silver.count()

            merge_table(
                spark=spark,
                df=df_silver,
                storage_config=STORAGE_CONFIG,
                layer="silver",
                table_name=cfg["table"],
                merge_keys=transform_cfg["merge_keys"]
            )

            logger.log_success(
                "silver",
                dataset,
                record_count
            )

            df_silver.unpersist()

        except Exception as e:

            logger.log_error(
                "silver",
                dataset,
                str(e)
            )

            raise