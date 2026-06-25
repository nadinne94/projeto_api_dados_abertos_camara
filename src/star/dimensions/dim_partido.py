"""
Construção da dimensão Partido.

Centraliza a seleção, padronização, deduplicação e geração de surrogate key
da dimensão `dim_partido` usada no modelo Star Schema.
"""

from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_partido(df_partidos):

    df_dim = (

        df_partidos

        .select(
            "id_partido",
            "sigla_partido",
            "nome_partido",
            "espectro_politico",
            "corrente_ideologica",
            "bloco_ideologico"
        )

        .dropDuplicates(
            ["id_partido"]
        )
    )

    return add_surrogate_key(
        df=df_dim,
        key_name="sk_partido",
        natural_keys=["id_partido"]
    )