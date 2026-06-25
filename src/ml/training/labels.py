"""
Geração de labels para treinamento supervisionado.

Centraliza regras usadas para atribuir rótulos iniciais às proposições
legislativas a partir de dicionários, padrões textuais, taxonomias e
critérios determinísticos.

Este módulo apoia a criação da base supervisionada usada no treinamento
dos classificadores.
"""


from pyspark.sql.functions import (
    when
)

from src.ml.features.tema import (
    classify_topic_for_training
)

from src.ml.features.natureza import (
    classify_legal_nature_for_training
)


TEMAS_TREINO = [

    "Saúde",

    "Educação",

    "Comunicação e Radiodifusão",

    "Datas Comemorativas e Homenagens",

    "Homenagens e Denominações",

    "Meio Ambiente",

    "Segurança Pública",

    "Economia",

    "Agricultura",

    "Tecnologia"
]


NATUREZAS_TREINO = [

    "Norma Material",

    "Alteração Legislativa",

    "Consolidação Legislativa",

    "Ato Simbólico",

    "Outorga / Concessão"
]


def classify_topic_label(
    col_ementa
):

    tema = classify_topic_for_training(
        col_ementa
    )

    return when(

        tema.isin(
            *TEMAS_TREINO
        ),

        tema
    )


def classify_legal_nature_label(
    col_ementa
):

    natureza = classify_legal_nature_for_training(
        col_ementa
    )

    return when(

        natureza.isin(
            *NATUREZAS_TREINO
        ),

        natureza
    )