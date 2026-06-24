"""
Utilitários para manipulação de datas.

Centraliza funções auxiliares usadas em transformações Spark relacionadas
a datas, como cálculo de intervalos e geração da data de processamento.

Este módulo é usado nas camadas de transformação e enriquecimento do
pipeline.
"""

from pyspark.sql.column import Column

from pyspark.sql.functions import (
    col,
    current_date,
    datediff,
    to_date,
)


def calculate_days_between(
    start_col: str,
    end_col: str
) -> Column:
    """
    Calcula diferença entre duas datas em dias.
    """

    return datediff(
        to_date(col(end_col)),
        to_date(col(start_col))
    )


def current_processing_date() -> Column:
    """
    Retorna data atual do processamento.
    """

    return current_date()