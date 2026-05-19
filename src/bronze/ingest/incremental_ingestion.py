"""
Wrapper especializado para ingestões incrementais.
"""

from src.bronze.ingest.simple_ingestion import (
    ingest_simple_dataset
)


def ingest_incremental_dataset(
    spark,
    dataset_name: str,
    config: dict,
    api_config: dict,
    logger
):
    """
    Executa ingestão incremental.
    """

    return ingest_simple_dataset(
        spark=spark,
        dataset_name=dataset_name,
        config=config,
        api_config=api_config,
        logger=logger
    )