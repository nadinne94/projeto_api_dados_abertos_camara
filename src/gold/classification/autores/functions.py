"""
Funções de classificação de autoria.

Centraliza regras usadas para classificar papel e tipo de autor nas
relações entre proposições e seus autores.
"""

from pyspark.sql.functions import (
    lower,
    trim,
    when,
    lit
)


def classify_author_role(
    col_ordem_assinatura
):

    return (
        when(
            col_ordem_assinatura == 1,
            lit("Autor Principal")
        )
        .when(
            col_ordem_assinatura > 1,
            lit("Coautor")
        )
        .otherwise(
            lit("Não Informado")
        )
    )


def classify_author_type(
    col_tipo_autor
):

    tipo = lower(
        trim(
            col_tipo_autor
        )
    )

    return (
        when(
            tipo.rlike("deputad"),
            lit("Deputado")
        )
        .when(
            tipo.rlike("senador"),
            lit("Senador")
        )
        .when(
            tipo.rlike("comiss"),
            lit("Comissão")
        )
        .when(
            tipo.rlike("poder executivo|executivo"),
            lit("Poder Executivo")
        )
        .when(
            tipo.rlike("tribunal|judiciario|judiciário"),
            lit("Poder Judiciário")
        )
        .otherwise(
            lit("Outros")
        )
    )