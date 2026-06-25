"""
Geração de relatórios de Data Quality.

Centraliza funções para converter resultados de validações em DataFrames
Spark, permitindo persistência dos relatórios em Delta Lake e posterior
consulta operacional.

Este módulo apoia a rastreabilidade das validações executadas no pipeline.
"""

from datetime import datetime
from typing import List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    TimestampType
)


def build_quality_report_df(
    spark: SparkSession,
    results: List[dict],
    execution_id: str,
    layer: str,
    table_name: str
) -> DataFrame:
    """
    Converte resultados de Data Quality em DataFrame Spark.

    Parâmetros:
        spark: SparkSession ativa.
        results: Lista de resultados retornada pelo runner de qualidade.
        execution_id: Identificador da execução do pipeline.
        layer: Camada validada.
        table_name: Tabela validada.

    Retorna:
        DataFrame Spark com relatório de qualidade.
    """

    now = datetime.utcnow()

    rows = [
        (
            execution_id,
            layer,
            table_name,
            result["rule_name"],
            result["status"],
            result["severity"],
            result["message"],
            str(result.get("metric_value")),
            str(result.get("expected_value")),
            now
        )
        for result in results
    ]

    schema = StructType(
        [
            StructField("execution_id", StringType(), False),
            StructField("layer", StringType(), False),
            StructField("table_name", StringType(), False),
            StructField("rule_name", StringType(), False),
            StructField("status", StringType(), False),
            StructField("severity", StringType(), False),
            StructField("message", StringType(), True),
            StructField("metric_value", StringType(), True),
            StructField("expected_value", StringType(), True),
            StructField("checked_at", TimestampType(), False),
        ]
    )

    return spark.createDataFrame(
        rows,
        schema
    )