"""
Factory responsável por determinar automaticamente
qual estratégia de ingestão deve ser utilizada.
"""

from src.bronze.ingest.simple_ingestion import (
    ingest_simple_dataset
)

from src.bronze.ingest.nested_ingestion import (
    ingest_nested_dataset
)

from src.bronze.ingest.incremental_ingestion import (
    ingest_incremental_dataset
)


class IngestionFactory:
    """
    Factory de ingestão.
    """

    @staticmethod
    def execute(
        spark,
        dataset_name: str,
        config: dict,
        api_config: dict,
        storage_config: dict,
        logger,
    ):

        if config.get("dependency"):

            return ingest_nested_dataset(
                spark=spark,
                dataset_name=dataset_name,
                config=config,
                api_config=api_config,
                storage_config=storage_config,
                logger=logger,
            )

        if config.get("incremental"):

            return ingest_incremental_dataset(
                spark=spark,
                dataset_name=dataset_name,
                config=config,
                api_config=api_config,
                logger=logger,
            )

        return ingest_simple_dataset(
            spark=spark,
            dataset_name=dataset_name,
            config=config,
            api_config=api_config,
            logger=logger,
        )