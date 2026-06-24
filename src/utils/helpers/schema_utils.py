"""
Utilitários para criação e tratamento de schemas.

Centraliza funções auxiliares para criação segura de DataFrames Spark a
partir de registros JSON, especialmente em cenários de respostas vazias
ou estruturas variáveis retornadas pela API.

Este módulo apoia a ingestão e a padronização dos dados no pipeline.
"""

from typing import List, Dict, Any

from pyspark.sql.types import (
    StructField,
    StructType,
    StringType,
)


def safe_dataframe(
    spark,
    records: List[Dict[str, Any]],
):
    """
    Cria DataFrame Spark resiliente
    para respostas JSON da API.
    """

    if not records:

        empty_schema = StructType([])

        return spark.createDataFrame(
            [],
            empty_schema
        )

    normalized = []

    for row in records:

        clean = {}

        for key, value in row.items():

            if isinstance(
                value,
                (dict, list)
            ):

                clean[key] = str(value)

            elif value is None:

                clean[key] = None

            else:

                clean[key] = str(value)

        normalized.append(clean)

    schema = StructType([

        StructField(
            column,
            StringType(),
            True
        )

        for column in normalized[0].keys()
    ])

    return spark.createDataFrame(
        normalized,
        schema=schema
    )