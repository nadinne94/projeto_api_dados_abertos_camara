"""
Utilities para geração de surrogate keys determinísticas.

Em modelos dimensionais, surrogate keys precisam ser estáveis entre
reprocessamentos para garantir consistência nos relacionamentos entre
fatos e dimensões.

Este módulo evita o uso de `monotonically_increasing_id()`, pois essa
função depende do particionamento físico do Spark e pode gerar valores
diferentes a cada execução.
"""

from typing import Iterable, Union

from pyspark.sql import DataFrame
from pyspark.sql.column import Column
from pyspark.sql.functions import (
    col,
    concat_ws,
    lit,
    sha2,
    trim,
    upper,
    when
)


def _normalize_key_column(column_name: str) -> Column:
    """
    Normaliza uma coluna usada na composição da chave determinística.

    A normalização reduz risco de chaves diferentes por variações simples
    de texto, como espaços extras ou diferenças entre maiúsculas/minúsculas.

    Args:
        column_name: Nome da coluna usada como chave natural.

    Returns:
        Expressão Spark normalizada para composição do hash.
    """

    return when(
        col(column_name).isNull(),
        lit("__NULL__")
    ).otherwise(
        upper(
            trim(
                col(column_name).cast("string")
            )
        )
    )


def add_surrogate_key(
    df: DataFrame,
    key_name: str,
    natural_keys: Union[str, Iterable[str]]
) -> DataFrame:
    """
    Adiciona uma surrogate key determinística baseada em hash SHA-256.

    A chave é gerada a partir das colunas de chave natural informadas.
    Diferentemente de `monotonically_increasing_id()`, o resultado é
    estável entre execuções desde que os valores das chaves naturais
    permaneçam os mesmos.

    Args:
        df: DataFrame de entrada.
        key_name: Nome da coluna de surrogate key a ser criada.
        natural_keys: Coluna ou lista de colunas que identificam
            unicamente o registro na dimensão.

    Returns:
        DataFrame com a coluna de surrogate key adicionada.

    Raises:
        ValueError: Se nenhuma chave natural for informada.
    """

    if isinstance(natural_keys, str):
        natural_keys = [natural_keys]

    natural_keys = list(natural_keys)

    if not natural_keys:
        raise ValueError(
            "É necessário informar ao menos uma coluna de chave natural "
            "para gerar a surrogate key."
        )

    missing_columns = [
        key
        for key in natural_keys
        if key not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Colunas de chave natural não encontradas no DataFrame: "
            f"{missing_columns}"
        )

    normalized_key = concat_ws(
        "||",
        *[
            _normalize_key_column(key)
            for key in natural_keys
        ]
    )

    return df.withColumn(
        key_name,
        sha2(
            normalized_key,
            256
        )
    )