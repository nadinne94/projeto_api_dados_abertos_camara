"""
Features para classificação de natureza jurídica.

Centraliza a criação de variáveis textuais, scores e indicadores usados
para identificar a natureza jurídica de proposições legislativas.

Este módulo combina evidências baseadas em texto, regex e dicionários
para apoiar regras de classificação e modelos supervisionados.
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

from src.ml.dictionaries.natureza import (
    NATUREZA_REGEX
)


def calculate_legal_nature_scores(
    col_ementa: Column
):

    normalized_text = normalize_text(
        col_ementa
    )

    scores = {}

    for class_name, rules in NATUREZA_REGEX.items():

        total = lit(0)

        for regex, weight in rules:

            total += score_regex(
                normalized_text,
                regex,
                weight
            )

        scores[class_name] = total

    return scores


def classify_legal_nature(
    col_ementa: Column
):

    scores = calculate_legal_nature_scores(
        col_ementa
    )

    result = select_best_score(

        scores_dict=scores,

        min_score=4,

        min_margin=2,

        fallback="Outros Tipos"
    )

    return struct(

        result["classe"].alias(
            "natureza_juridica"
        ),

        result["score_max"],

        result["score_second"],

        result["score_margem"],

        result["confianca"]
    )


def classify_legal_nature_for_training(
    col_ementa: Column
):

    return classify_legal_nature(
        col_ementa
    )["natureza_juridica"]
