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


def aplicar_classificacao_dict(
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


def classificar_bloco_ideologico(
    col_partido
):

    return aplicar_classificacao_dict(
        col_partido,
        BLOCO_IDEOLOGICO
    )


def classificar_corrente_ideologica(
    col_partido
):

    return aplicar_classificacao_dict(
        col_partido,
        CORRENTE_IDEOLOGICA
    )


def classificar_espectro_politico(
    col_partido
):

    return aplicar_classificacao_dict(
        col_partido,
        ESPECTRO_POLITICO
    )