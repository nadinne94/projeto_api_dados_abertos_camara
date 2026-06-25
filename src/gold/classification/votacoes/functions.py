"""
Funções de classificação de votações.

Centraliza regras usadas para classificar o resultado de votações
legislativas.
"""

from pyspark.sql.functions import (
    when,
    lit
)


def classify_vote_result(
    col_aprovacao
):

    return (
        when(
            col_aprovacao == True,
            lit("Aprovada")
        )

        .when(
            col_aprovacao == False,
            lit("Rejeitada")
        )

        .otherwise(
            lit("Indefinido")
        )
    )