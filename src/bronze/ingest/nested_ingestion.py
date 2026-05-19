"""
Ingestão genérica para datasets dependentes.

Coleta sub-recursos da API da Câmara.
"""

from pyspark.sql.functions import current_timestamp

from src.utils.api.api_client import (
    fetch_nested_data
)

from src.utils.helpers.schema_utils import (
    safe_dataframe
)

from src.utils.storage.delta_io import (
    read_table
)


def ingest_nested_dataset(
    spark,
    dataset_name: str,
    config: dict,
    api_config: dict,
    storage_config: dict,
    logger,
):
    """
    Executa ingestão de datasets dependentes.

    Args:
        spark: SparkSession.
        dataset_name: Nome do dataset.
        config: Configuração do dataset.
        api_config: Configuração da API.
        storage_config: Configuração storage.
        logger: Logger estruturado.

    Returns:
        DataFrame Spark ou None.
    """

    logger.log_start(
        "bronze",
        dataset_name
    )

    dependency = config["dependency"]

    parent_dataset = dependency["parent"]
    parent_key = dependency["key"]

    parent_df = read_table(
        spark=spark,
        storage_config=storage_config,
        layer="bronze",
        table_name=parent_dataset,
    )

    max_parent_ids = api_config[
        "max_parent_ids"
    ]

    parent_ids = [

        row[parent_key]

        for row in (

            parent_df
            .select(parent_key)
            .distinct()
            .limit(max_parent_ids)
            .collect()
        )
    ]

    logger.log_info(
        "bronze",
        dataset_name,
        (
            f"Dataset pai={parent_dataset} "
            f"| Parent IDs={len(parent_ids)}"
        )
    )

    if not parent_ids:

        logger.log_warning(
            "bronze",
            dataset_name,
            "Nenhum parent_id encontrado"
        )

        return None

    data = fetch_nested_data(
        endpoint_template=config["endpoint"],
        parent_ids=parent_ids,
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
            "Nenhum dado retornado"
        )

        return None

    return (

        safe_dataframe(
            spark,
            data
        )

        .withColumn(
            "data_ingestao",
            current_timestamp()
        )
    )