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
    classify_topic
)

from src.ml.features.natureza import (
    classify_legal_nature
)


# =========================================================
# TEXTO BASE
# =========================================================

def build_proposition_text(
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
# TIPO DOCUMENTAL
# =========================================================

def classify_document_type(
    col_ementa: Column,
    col_sigla_tipo: Column = None
):

    texto = build_proposition_text(
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