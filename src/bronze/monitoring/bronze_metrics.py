"""
Métricas operacionais da camada Bronze.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    count,
    lit,
    round,
)


def generate_bronze_metrics(
    df: DataFrame,
    dataset_name: str,
) -> DataFrame:
    """
    Gera métricas operacionais do dataset.
    """

    total_records = df.count()

    metrics = [(
        dataset_name,
        total_records,
        len(df.columns),
    )]

    return (
        df.sparkSession.createDataFrame(
            metrics,
            schema=[
                "dataset",
                "total_registros",
                "total_colunas",
            ],
        )
    )


def generate_column_metrics(
    df: DataFrame
) -> DataFrame:
    """
    Calcula completude por coluna.
    """

    total_rows = df.count()

    if total_rows == 0:

        return df.sparkSession.createDataFrame(
            [],
            schema="""
                coluna STRING,
                preenchidos LONG,
                pct_completude DOUBLE
            """
        )

    expressions = [

        count(col(c)).alias(c)

        for c in df.columns
    ]

    counts = df.select(
        expressions
    ).collect()[0]

    rows = [

        (
            column,
            int(counts[column]),
            round(
                int(counts[column]) / total_rows,
                4
            )
        )

        for column in df.columns
    ]

    return (

        df.sparkSession

        .createDataFrame(
            rows,
            [
                "coluna",
                "preenchidos",
                "pct_completude",
            ]
        )

        .orderBy(
            "pct_completude",
            ascending=False
        )
    )