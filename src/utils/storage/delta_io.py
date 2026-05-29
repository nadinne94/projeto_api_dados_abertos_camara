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
    """Return the physical Delta path for a table.

    Args:
        storage_config: Mapping with base paths by layer.
        layer: Logical layer name, such as bronze, silver, gold or star.
        table_name: Table name inside the layer.

    Returns:
        Full storage path for the Delta table.
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
    """Read a Delta table from the configured storage path.

    Args:
        spark: Active SparkSession.
        storage_config: Mapping with base paths by layer.
        layer: Logical layer name.
        table_name: Table to read.
        validate: If True, checks whether the path is a Delta table.

    Returns:
        DataFrame loaded from Delta.
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
    """Write a DataFrame as a Delta table using overwrite mode.

    Args:
        spark: Active SparkSession.
        df: DataFrame to persist.
        storage_config: Mapping with base paths by layer.
        layer: Logical layer name.
        table_name: Target table name.
    """

    path = get_path(
        storage_config,
        layer,
        table_name
    )

    logger.info(
        "[WRITE] %s.%s",
        layer,
        table_name
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
    """Merge a DataFrame into a Delta table using the provided keys.

    If the target table does not exist yet, the function creates it with
    the same write behavior used by `write_table`.

    Args:
        spark: Active SparkSession.
        df: Source DataFrame.
        storage_config: Mapping with base paths by layer.
        layer: Logical layer name.
        table_name: Target table name.
        merge_keys: Columns used to match source and target records.
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
