from pyspark.sql.column import Column

from pyspark.sql.functions import (
    lit,
    struct,
    when
)

from src.ml.base.preprocessing import (
    normalizar_texto
)

from src.ml.base.regex import (
    score_regex
)

from src.ml.base.scoring import (
    escolher_melhor_score
)

from src.ml.dictionaries.natureza import (
    NATUREZA_REGEX
)


def calcular_scores_natureza(
    col_ementa: Column
):

    texto = normalizar_texto(
        col_ementa
    )

    scores = {}

    for classe, regras in (
        NATUREZA_REGEX.items()
    ):

        total = lit(0)

        for regex, peso in regras:

            total += score_regex(
                texto,
                regex,
                peso
            )

        scores[classe] = total

    return scores


def classificar_natureza_juridica(
    col_ementa: Column
):

    scores = calcular_scores_natureza(
        col_ementa
    )

    resultado = escolher_melhor_score(

        scores_dict=scores,

        min_score=4,

        min_margin=2,

        fallback="Outros Tipos"
    )

    return struct(

        resultado["classe"].alias(
            "natureza_juridica"
        ),

        resultado["score_max"],

        resultado["score_second"],

        resultado["score_margem"],

        resultado["confianca"]
    )


def classificar_natureza_juridica_treino(
    col_ementa: Column
):

    return classificar_natureza_juridica(
        col_ementa
    )["natureza_juridica"]


def classificar_natureza_juridica_final(

    col_ementa: Column,

    udf_ml
):

    natureza_rule = (

        classificar_natureza_juridica(
            col_ementa
        )
    )

    natureza_ml = udf_ml(
        col_ementa
    )

    return struct(

        when(

            natureza_rule[
                "natureza_juridica"
            ]

            !=

            "Outros Tipos",

            natureza_rule[
                "natureza_juridica"
            ]

        )

        .otherwise(

            natureza_ml
        )

        .alias(
            "natureza_juridica"
        ),

        when(

            natureza_rule[
                "natureza_juridica"
            ]

            !=

            "Outros Tipos",

            lit("REGRA_SCORE")

        )

        .otherwise(

            lit("ML")
        )

        .alias(
            "origem_classificacao"
        ),

        natureza_rule["score_max"],

        natureza_rule["score_second"],

        natureza_rule["score_margem"],

        natureza_rule["confianca"]
    )