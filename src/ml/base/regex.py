from pyspark.sql.column import Column

from pyspark.sql.functions import (
    when,
    lit,
    regexp_extract,
    length,
    size,
    split
)


def regex_match(
    col_texto: Column,
    pattern: str
) -> Column:

    return col_texto.rlike(
        pattern
    )


def regex_count(
    col_texto: Column,
    pattern: str
) -> Column:

    """
    Conta quantidade de ocorrências
    do regex no texto.

    Ex:
    "sus sus sus"
    regex="sus"

    -> 3
    """

    return (

        size(

            split(
                col_texto,
                pattern
            )

        ) - 1
    )


def regex_extract_length(
    col_texto: Column,
    pattern: str
) -> Column:

    """
    Retorna tamanho do primeiro match.

    Ex:
    texto="sistema unico de saude"
    regex="saude"

    -> 5
    """

    return length(

        regexp_extract(
            col_texto,
            pattern,
            0
        )
    )


def score_regex(
    col_texto: Column,
    pattern: str,
    peso: int
) -> Column:

    return when(

        regex_match(
            col_texto,
            pattern
        ),

        lit(peso)

    ).otherwise(

        lit(0)
    )