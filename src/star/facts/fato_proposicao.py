from pyspark.sql.functions import (
    col,
    date_format,
    lit
)


def build_fato_proposicao(
    df_proposicoes,
    dim_proposicao
):

    return (

        df_proposicoes.alias("p")

        .join(
            dim_proposicao.alias("d"),
            "id_proposicao",
            "left"
        )

        .select(

            col("d.sk_proposicao"),

            date_format(
                col("p.data_apresentacao"),
                "yyyyMMdd"
            ).cast("int").alias(
                "sk_tempo"
            ),

            col("p.peso_regimental"),

            col("p.flag_normativa").cast("int").alias(
                "flag_normativa"
            ),

            col("p.flag_fiscalizacao").cast("int").alias(
                "flag_fiscalizacao"
            ),

            col("p.flag_baixo_impacto").cast("int").alias(
                "flag_baixo_impacto"
            ),

            col("p.flag_social").cast("int").alias(
                "flag_social"
            ),

            col("p.flag_economico").cast("int").alias(
                "flag_economico"
            ),

            col("p.flag_tema_por_ml").cast("int").alias(
                "flag_tema_por_ml"
            ),

            col("p.flag_natureza_por_ml").cast("int").alias(
                "flag_natureza_por_ml"
            ),

            lit(1).alias(
                "qtd_proposicoes"
            )
        )
    )