from pyspark.sql.functions import col

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
        df_dim,
        "sk_deputado"
    )