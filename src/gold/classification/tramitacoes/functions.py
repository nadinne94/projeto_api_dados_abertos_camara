from pyspark.sql.column import Column

from pyspark.sql.functions import (
    lower,
    coalesce,
    concat_ws,
    when,
    lit
)

from src.gold.classification.tramitacoes.dictionaries import (
    STATUS_TRAMITACAO
)


def classificar_status_tramitacao(
    col_situacao: Column,
    col_descricao: Column,
    col_despacho: Column
):

    texto = concat_ws(

        " ",

        lower(
            coalesce(
                col_situacao,
                lit("")
            )
        ),

        lower(
            coalesce(
                col_descricao,
                lit("")
            )
        ),

        lower(
            coalesce(
                col_despacho,
                lit("")
            )
        )
    )

    expr = lit("Em Tramitação")

    for status, patterns in reversed(
        list(
            STATUS_TRAMITACAO.items()
        )
    ):

        regex = "|".join(
            patterns
        )

        expr = when(
            texto.rlike(regex),
            lit(status)
        ).otherwise(
            expr
        )

    return expr