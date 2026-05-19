"""
Delta Lake utilities.

Centraliza:
- leitura
- escrita
- merge/upsert
- optimize
- vacuum
"""

import logging

from typing import List
from typing import Optional

from delta.tables import DeltaTable

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


def get_path(
    storage_config: dict,
    layer: str,
    table_name: str
) -> str:
    """
    Retorna path físico.
    """

    return (
        f"{storage_config[layer]}"
        f"/{table_name}"
    )


def read_table(
    spark: SparkSession,
    storage_config: dict,
    layer: str,
    table_name: str,
    validate: bool = True
) -> DataFrame:
    """
    Lê tabela Delta.
    """

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    if validate:

        if not DeltaTable.isDeltaTable(
            spark,
            path
        ):

            raise FileNotFoundError(
                f"Tabela não encontrada: "
                f"{layer}.{table_name}"
            )

    logger.info(
        "[READ] %s.%s",
        layer,
        table_name
    )

    return (
        spark.read
        .format("delta")
        .load(path)
    )


def write_table(
    spark: SparkSession,
    df: DataFrame,
    storage_config: dict,
    layer: str,
    table_name: str
) -> None:
    """
    Escreve tabela Delta.
    """

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    logger.info(
        "[WRITE] %s.%s rows=%s",
        layer,
        table_name,
        df.count()
    )

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option(
            "overwriteSchema",
            "true"
        )
        .option(
            "mergeSchema",
            "true"
        )
        .save(path)
    )


def merge_table(
    spark: SparkSession,
    df: DataFrame,
    storage_config: dict,
    layer: str,
    table_name: str,
    merge_keys: List[str]
) -> None:
    """
    Executa merge/upsert Delta.
    """

    if not merge_keys:

        raise ValueError(
            "merge_keys obrigatório."
        )

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    if not DeltaTable.isDeltaTable(
        spark,
        path
    ):

        logger.info(
            "[MERGE] tabela inexistente -> write"
        )

        write_table(
            spark=spark,
            df=df,
            storage_config=storage_config,
            layer=layer,
            table_name=table_name
        )

        return

    delta_table = DeltaTable.forPath(
        spark,
        path
    )

    condition = " AND ".join([

        f"target.{k}=source.{k}"

        for k in merge_keys
    ])

    update_map = {

        column:
        f"source.{column}"

        for column in df.columns
    }

    logger.info(
        "[MERGE] %s.%s keys=%s",
        layer,
        table_name,
        merge_keys
    )

    (
        delta_table.alias("target")
        .merge(
            df.alias("source"),
            condition
        )
        .whenMatchedUpdate(
            set=update_map
        )
        .whenNotMatchedInsert(
            values=update_map
        )
        .execute()
    )


def optimize_table(
    spark: SparkSession,
    storage_config: dict,
    layer: str,
    table_name: str,
    zorder_cols: Optional[List[str]] = None
) -> None:
    """
    Executa optimize.

    Disponível principalmente
    em Databricks.
    """

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    try:

        if zorder_cols:

            cols = ",".join(
                zorder_cols
            )

            spark.sql(
                f"""
                OPTIMIZE delta.`{path}`
                ZORDER BY ({cols})
                """
            )

        else:

            spark.sql(
                f"""
                OPTIMIZE delta.`{path}`
                """
            )

        logger.info(
            "[OPTIMIZE] %s.%s",
            layer,
            table_name
        )

    except Exception as exc:

        logger.warning(
            "[OPTIMIZE] unsupported: %s",
            exc
        )


def vacuum_table(
    spark: SparkSession,
    storage_config: dict,
    layer: str,
    table_name: str,
    retention_hours: int = 168
) -> None:
    """
    Executa vacuum.
    """

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    logger.info(
        "[VACUUM] %s.%s",
        layer,
        table_name
    )

    spark.sql(
        f"""
        VACUUM delta.`{path}`
        RETAIN {retention_hours} HOURS
        """
    )