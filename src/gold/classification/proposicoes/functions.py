from pyspark.sql.column import Column

from pyspark.sql.functions import (
    lower,
    coalesce,
    concat_ws,
    when,
    lit
)

from src.gold.classification.proposicoes.dictionaries import (
    TIPOS_DOCUMENTAIS
)

from src.ml.features.tema import (
    classificar_tema
)

from src.ml.features.natureza import (
    classificar_natureza_juridica
)


# =========================================================
# TEXTO BASE
# =========================================================

def montar_texto_proposicao(
    col_ementa: Column,
    col_sigla_tipo: Column = None
):

    if col_sigla_tipo is not None:

        return concat_ws(

            " ",

            lower(
                coalesce(
                    col_sigla_tipo,
                    lit("")
                )
            ),

            lower(
                coalesce(
                    col_ementa,
                    lit("")
                )
            )
        )

    return lower(
        coalesce(
            col_ementa,
            lit("")
        )
    )


# =========================================================
# TEMA REGEX
# =========================================================

def classificar_tema_regex(
    col_ementa: Column
):

    return classificar_tema(
        col_ementa
    )["tema"]


# =========================================================
# NATUREZA JURÍDICA
# =========================================================

def classificar_natureza_juridica_regex(
    col_ementa: Column
):

    return classificar_natureza_juridica(
        col_ementa
    )


# =========================================================
# TIPO DOCUMENTAL
# =========================================================

def classificar_tipo_documental(
    col_ementa: Column,
    col_sigla_tipo: Column = None
):

    texto = montar_texto_proposicao(
        col_ementa,
        col_sigla_tipo
    )

    expr = lit("Outros Tipos")

    for categoria, patterns in reversed(
        list(TIPOS_DOCUMENTAIS.items())
    ):

        regex = "|".join(patterns)

        expr = when(
            texto.rlike(regex),
            lit(categoria)
        ).otherwise(
            expr
        )

    return expr