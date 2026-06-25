"""
Construção da dimensão Deputado.

Centraliza a seleção, padronização, deduplicação e geração de surrogate key
da dimensão `dim_deputado` usada no modelo Star Schema.
"""

from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_deputado(df_deputados):

    df_dim = (

        df_deputados

        .select(
            "id_deputado",
            "nome_deputado",
            "sigla_partido",
            "uf_origem",
            "regiao",
            "email",
            "url_foto"
        )

        .dropDuplicates(
            ["id_deputado"]
        )
    )

    return add_surrogate_key(
        df=df_dim,
        key_name="sk_deputado",
        natural_keys=["id_deputado"]
    )