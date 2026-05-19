"""
Utilities para surrogate keys.
"""

from pyspark.sql import DataFrame

from pyspark.sql.functions import (
    monotonically_increasing_id
)


def add_surrogate_key(
    df: DataFrame,
    key_name: str
) -> DataFrame:
    """
    Adiciona surrogate key Spark.

    Observação:
    não produz sequência contínua.
    """

    return df.withColumn(
        key_name,
        monotonically_increasing_id()
    )