"""
Ingestão genérica para datasets simples.

Suporta datasets full load e incremental
via WatermarkManager.
"""

from pyspark.sql.functions import current_timestamp

from src.config.project_config import STORAGE_CONFIG

from src.utils.api.api_client import (
    get_all_pages
)

from src.utils.helpers.schema_utils import (
    safe_dataframe
)

from src.utils.storage.watermark_manager import (
    WatermarkManager
)


def ingest_simple_dataset(
    spark,
    dataset_name: str,
    config: dict,
    api_config: dict,
    logger,
):
    """
    Executa ingestão de datasets simples.

    Args:
        spark: SparkSession.
        dataset_name: Nome do dataset.
        config: Configuração do dataset.
        api_config: Configuração da API.
        logger: Logger estruturado.

    Returns:
        DataFrame Spark ou None.
    """

    logger.log_start(
        "bronze",
        dataset_name
    )

    watermark_manager = WatermarkManager(
        spark=spark,
        watermark_path=(
            STORAGE_CONFIG["watermark"]
        )
    )

    params = dict(
        config.get("params", {})
    )

    params = (
        watermark_manager
        .apply_incremental_params(
            dataset_name=dataset_name,
            config=config,
            params=params,
        )
    )

    data = get_all_pages(
        endpoint=config["endpoint"],
        params=params,
        api_config=api_config,
    )

    logger.log_info(
        "bronze",
        dataset_name,
        f"Registros API={len(data)}"
    )

    if not data:

        logger.log_warning(
            "bronze",
            dataset_name,
            "Nenhum dado retornado",
        )

        return None

    df = (
        safe_dataframe(
            spark,
            data
        )
        .withColumn(
            "data_ingestao",
            current_timestamp()
        )
    )

    (
        watermark_manager
        .update_incremental_watermark(
            dataset_name=dataset_name,
            config=config,
            df=df,
        )
    )

    return df