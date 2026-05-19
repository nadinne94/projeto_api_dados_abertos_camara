"""
Utilitários para análise de qualidade de dados.

Fornece métricas eficientes de completude
para DataFrames Spark.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    count,
    lit,
    sum,
    when,
)


def null_ratio(
    df: DataFrame
) -> DataFrame:
    """
    Calcula percentual de nulos por coluna.
    """

    spark = df.sparkSession

    if not df.columns:

        return spark.createDataFrame(
            [],
            schema="""
                coluna STRING,
                qtd_nulos LONG,
                pct_nulos DOUBLE
            """
        )

    total = df.count()

    if total == 0:

        return spark.createDataFrame(
            [],
            schema="""
                coluna STRING,
                qtd_nulos LONG,
                pct_nulos DOUBLE
            """
        )

    null_counts = (

        df.select([

            sum(
                when(
                    col(c).isNull(),
                    lit(1)
                ).otherwise(lit(0))
            ).alias(c)

            for c in df.columns

        ])

        .first()

    )

    rows = [

        (
            column,
            int(null_counts[column]),
            round(
                int(null_counts[column]) / total,
                4
            )
        )

        for column in df.columns

    ]

    return (

        spark.createDataFrame(
            rows,
            schema=[
                "coluna",
                "qtd_nulos",
                "pct_nulos"
            ]
        )

        .orderBy(
            col("pct_nulos").desc()
        )

    )