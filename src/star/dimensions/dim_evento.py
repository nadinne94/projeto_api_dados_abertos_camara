from pyspark.sql.functions import (
    col
)

from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_evento(df_eventos):

    df_dim = (

        df_eventos

        .select(

            col("id_evento").alias(
                "id_evento"
            ),

            col("tipo_evento").alias(
                "tipo_evento_original"
            ),

            col("tipo_evento_classificado").alias(
                "tipo_evento"
            ),

            col("situacao").alias(
                "situacao_original"
            ),

            col("situacao_evento").alias(
                "situacao_evento"
            ),

            col("tipo_local").alias(
                "tipo_local"
            ),

            col("local_nome").alias(
                "local_nome"
            ),

            col("flag_evento_realizado").alias(
                "flag_evento_realizado"
            )
        )

        .dropDuplicates(
            ["id_evento"]
        )
    )

    return add_surrogate_key(
        df_dim,
        "sk_evento"
    )