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

from src.ml.dictionaries.temas import (
    TEMA_REGEX_RULES,
    TEMA_THRESHOLDS,
    TEMA_MIN_SCORE,
    TEMA_MIN_MARGIN,
    TEMA_FALLBACK
)


def calcular_scores_tema(
    col_ementa: Column
) -> dict:

    texto = normalizar_texto(
        col_ementa
    )

    scores = {}

    for tema, regras in TEMA_REGEX_RULES.items():

        total = lit(0)

        for regex, peso in regras:

            total = total + score_regex(
                texto,
                regex,
                peso
            )

        scores[tema] = total

    return scores


def classificar_tema(
    col_ementa: Column
):

    scores = calcular_scores_tema(
        col_ementa
    )

    resultado = escolher_melhor_score(

        scores_dict=scores,

        min_score=TEMA_MIN_SCORE,

        min_margin=TEMA_MIN_MARGIN,

        fallback=TEMA_FALLBACK,

        thresholds_por_classe=TEMA_THRESHOLDS
    )

    return struct(

        resultado["classe"].alias(
            "tema"
        ),

        resultado["score_max"],

        resultado["score_second"],

        resultado["score_margem"],

        resultado["confianca"]
    )


def classificar_tema_treino(
    col_ementa: Column
):

    return classificar_tema(
        col_ementa
    )["tema"]


def classificar_tema_final(
    col_ementa: Column,
    udf_ml
):

    tema_rule = classificar_tema(
        col_ementa
    )

    tema_ml = udf_ml(
        col_ementa
    )

    regra_valida = (
        tema_rule["tema"] != TEMA_FALLBACK
    )

    return struct(

        when(
            regra_valida,
            tema_rule["tema"]
        )
        .otherwise(
            tema_ml
        )
        .alias(
            "tema_final"
        ),

        when(
            regra_valida,
            lit("REGRA_SCORE")
        )
        .otherwise(
            lit("ML")
        )
        .alias(
            "origem_classificacao"
        ),

        tema_rule["score_max"],

        tema_rule["score_second"],

        tema_rule["score_margem"],

        tema_rule["confianca"]
    )