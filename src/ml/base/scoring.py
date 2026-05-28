from pyspark.sql.functions import (
    array,
    array_sort,
    element_at,
    size,
    when,
    lit,
    struct
)


def calcular_confianca(
    max_score,
    second_score
):
    margem = max_score - second_score

    return (
        when(
            (max_score >= 8) & (margem >= 4),
            lit("Alta")
        )
        .when(
            (max_score >= 5) & (margem >= 2),
            lit("Média")
        )
        .otherwise(
            lit("Baixa")
        )
    )


def escolher_melhor_score(
    scores_dict: dict,
    min_score: int = 4,
    min_margin: int = 1,
    fallback: str = "Tema Não Explícito",
    thresholds_por_classe: dict | None = None
):
    scores = list(scores_dict.values())

    sorted_scores = array_sort(
        array(*scores)
    )

    max_score = element_at(
        sorted_scores,
        -1
    )

    second_score = when(
        size(sorted_scores) >= 2,
        element_at(sorted_scores, -2)
    ).otherwise(
        lit(0)
    )

    margem = max_score - second_score

    classe = lit(fallback)

    for nome, score in scores_dict.items():

        threshold_classe = (
            thresholds_por_classe.get(nome, min_score)
            if thresholds_por_classe
            else min_score
        )

        classe = when(
            (score == max_score)
            & (max_score >= threshold_classe)
            & (margem >= min_margin),
            lit(nome)
        ).otherwise(classe)

    return struct(
        classe.alias("classe"),
        max_score.alias("score_max"),
        second_score.alias("score_second"),
        margem.alias("score_margem"),
        calcular_confianca(
            max_score,
            second_score
        ).alias("confianca")
    )