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
    classificar_tema_treino
)

from src.ml.features.natureza import (
    classificar_natureza_juridica_treino
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


def classificar_tema_label(
    col_ementa
):

    tema = classificar_tema_treino(
        col_ementa
    )

    return when(

        tema.isin(
            *TEMAS_TREINO
        ),

        tema
    )


def classificar_natureza_label(
    col_ementa
):

    natureza = classificar_natureza_juridica_treino(
        col_ementa
    )

    return when(

        natureza.isin(
            *NATUREZAS_TREINO
        ),

        natureza
    )