"""
Funções auxiliares para cálculo de scores de classificação.

Centraliza regras de pontuação usadas para combinar evidências textuais,
dicionários e padrões identificados durante a classificação de proposições.

Este módulo apoia a priorização de classes candidatas antes da aplicação
de fallback ou seleção final.
"""


from pyspark.sql.functions import (
    array,
    array_sort,
    element_at,
    size,
    when,
    lit,
    struct
)


def calculate_confidence(
    max_score,
    second_score
):
    margin = max_score - second_score

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


def select_best_score(
    scores_dict: dict,
    min_score: int = 4,
    min_margin: int = 1,
    fallback: str = "Tema Não Explícito",
    class_thresholds: dict | None = None
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

    margin = max_score - second_score

    selected_class = lit(fallback)

    for class_name, score in scores_dict.items():

        class_threshold = (
            class_thresholds.get(class_name, min_score)
            if class_thresholds
            else min_score
        )

        selected_class = when(
            (score == max_score)
            & (max_score >= class_threshold)
            & (margin >= min_margin),
            lit(class_name)
        ).otherwise(selected_class)

    return struct(
        selected_class.alias("classe"),
        max_score.alias("score_max"),
        second_score.alias("score_second"),
        margin.alias("score_margem"),
        calculate_confidence(
            max_score,
            second_score
        ).alias("confianca")
    )