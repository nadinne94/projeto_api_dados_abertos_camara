from typing import Iterable

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def assert_not_empty(
    df: DataFrame,
    dataset_name: str = "dataset"
) -> None:
    """
    Valida se o DataFrame possui registros.

    Args:
        df: DataFrame a ser validado.
        dataset_name: Nome lógico do dataset.

    Raises:
        ValueError: Se o DataFrame estiver vazio.
    """

    if df.limit(1).count() == 0:
        raise ValueError(
            f"O dataset '{dataset_name}' está vazio."
        )


def assert_required_columns(
    df: DataFrame,
    required_columns: Iterable[str],
    dataset_name: str = "dataset"
) -> None:
    """
    Valida se todas as colunas obrigatórias existem no DataFrame.

    Args:
        df: DataFrame a ser validado.
        required_columns: Lista de colunas obrigatórias.
        dataset_name: Nome lógico do dataset.

    Raises:
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"O dataset '{dataset_name}' não possui as colunas obrigatórias: "
            f"{missing_columns}"
        )


def assert_no_nulls(
    df: DataFrame,
    columns: Iterable[str],
    dataset_name: str = "dataset"
) -> None:
    """
    Valida se as colunas informadas não possuem valores nulos.

    Args:
        df: DataFrame a ser validado.
        columns: Colunas que não devem conter nulos.
        dataset_name: Nome lógico do dataset.

    Raises:
        ValueError: Se houver valores nulos nas colunas informadas.
    """

    for column in columns:
        null_count = (
            df
            .filter(
                col(column).isNull()
            )
            .limit(1)
            .count()
        )

        if null_count > 0:
            raise ValueError(
                f"O dataset '{dataset_name}' possui valores nulos na coluna "
                f"'{column}'."
            )


def assert_unique_key(
    df: DataFrame,
    key_columns: Iterable[str],
    dataset_name: str = "dataset"
) -> None:
    """
    Valida se uma chave é única no DataFrame.

    Args:
        df: DataFrame a ser validado.
        key_columns: Colunas que compõem a chave.
        dataset_name: Nome lógico do dataset.

    Raises:
        ValueError: Se houver duplicidade na chave.
    """

    key_columns = list(key_columns)

    duplicated_count = (
        df
        .groupBy(*key_columns)
        .count()
        .filter(
            col("count") > 1
        )
        .limit(1)
        .count()
    )

    if duplicated_count > 0:
        raise ValueError(
            f"O dataset '{dataset_name}' possui duplicidades na chave: "
            f"{key_columns}"
        )