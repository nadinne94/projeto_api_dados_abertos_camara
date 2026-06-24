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
    when
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

    texto = normalize_text(
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

    scores = calculate_topic_scores(
        col_ementa
    )

    resultado = select_best_score(

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


def classify_topic_for_training(
    col_ementa: Column
):

    return classificar_tema(
        col_ementa
    )["tema"]
