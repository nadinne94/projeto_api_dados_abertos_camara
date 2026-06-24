from pyspark.sql.functions import (
    upper,
    when,
    lit
)

from src.gold.classification.partidos.dictionaries import (
    BLOCO_IDEOLOGICO,
    CORRENTE_IDEOLOGICA,
    ESPECTRO_POLITICO
)


def apply_dict_classification(
    col_partido,
    mapping,
    default="Outros"
):
    partido = upper(
        col_partido
    )

    expr = lit(default)

    for classe, partidos in reversed(
        list(mapping.items())
    ):

        expr = when(
            partido.isin(*partidos),
            lit(classe)
        ).otherwise(
            expr
        )

    return expr


def classify_ideological_bloc(
    col_partido
):

    return apply_dict_classification(
        col_partido,
        BLOCO_IDEOLOGICO
    )


def classify_ideological_current(
    col_partido
):

    return apply_dict_classification(
        col_partido,
        CORRENTE_IDEOLOGICA
    )


def classify_political_spectrum(
    col_partido
):

    return apply_dict_classification(
        col_partido,
        ESPECTRO_POLITICO
    )