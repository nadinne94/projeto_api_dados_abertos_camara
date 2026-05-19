"""
Date utilities.
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