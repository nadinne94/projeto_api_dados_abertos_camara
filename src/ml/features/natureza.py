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
    when
)

from src.ml.base.preprocessing import (
    normalize_text
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


def calculate_legal_nature_scores(
    col_ementa: Column
):

    texto = normalize_text(
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


def classify_legal_nature(
    col_ementa: Column
):

    scores = calculate_legal_nature_scores(
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


def classify_legal_nature_for_training(
    col_ementa: Column
):

    return classify_legal_nature(
        col_ementa
    )["natureza_juridica"]
