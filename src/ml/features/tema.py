"""
Features para classificação temática.

Centraliza a criação de variáveis textuais, scores e indicadores usados
para identificar o tema principal de proposições legislativas.

Este módulo combina evidências baseadas em texto, regex, dicionários e
taxonomia temática para apoiar regras de classificação e modelos
supervisionados.
"""


from pyspark.sql.column import Column

from pyspark.sql.functions import (
    lit,
    struct,
)

from src.ml.base.preprocessing import (
    normalize_text
)

from src.ml.base.regex import (
    score_regex
)

from src.ml.base.scoring import (
    select_best_score
)

from src.ml.dictionaries.temas import (
    TEMA_REGEX_RULES,
    TEMA_THRESHOLDS,
    TEMA_MIN_SCORE,
    TEMA_MIN_MARGIN,
    TEMA_FALLBACK
)


def calculate_topic_scores(
    col_ementa: Column
) -> dict:

    normalized_text = normalize_text(
        col_ementa
    )

    scores = {}

    for topic, rules in TEMA_REGEX_RULES.items():

        total = lit(0)

        for regex, weight in rules:

            total = total + score_regex(
                normalized_text,
                regex,
                weight
            )

        scores[topic] = total

    return scores


def classify_topic(
    col_ementa: Column
):

    scores = calculate_topic_scores(
        col_ementa
    )

    result = select_best_score(

        scores_dict=scores,

        min_score=TEMA_MIN_SCORE,

        min_margin=TEMA_MIN_MARGIN,

        fallback=TEMA_FALLBACK,

        class_thresholds=TEMA_THRESHOLDS
    )

    return struct(

        result["classe"].alias(
            "tema"
        ),

        result["score_max"],

        result["score_second"],

        result["score_margem"],

        result["confianca"]
    )


def classify_topic_for_training(
    col_ementa: Column
):

    return classify_topic(
        col_ementa
    )["tema"]
