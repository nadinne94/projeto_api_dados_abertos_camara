from pyspark.sql.functions import (
    col,
    trim,
    upper,
    lit,
    date_format
)


def build_fato_votacao(
    df_votacoes,
    dim_proposicao,
    dim_orgao
):

    votacoes = (

        df_votacoes

        .withColumn(
            "orgao_norm",
            trim(
                upper(
                    col("orgao")
                )
            )
        )
    )

    orgaos = (

        dim_orgao

        .withColumn(
            "orgao_norm",
            trim(
                upper(
                    col("orgao")
                )
            )
        )
    )

    return (

        votacoes.alias("v")

        .join(
            dim_proposicao.alias("p"),
            col("v.id_proposicao")
            == col("p.id_proposicao"),
            "left"
        )

        .join(
            orgaos.alias("o"),
            col("v.orgao_norm")
            == col("o.orgao_norm"),
            "left"
        )

        .select(

            col("v.id_votacao"),

            col("p.sk_proposicao"),

            col("o.sk_orgao"),

            date_format(
                col("v.data_votacao"),
                "yyyyMMdd"
            ).cast("int").alias(
                "sk_tempo"
            ),

            col("v.aprovacao").cast("int").alias(
                "flag_aprovada_original"
            ),

            col("v.resultado_votacao"),

            col("v.flag_aprovada"),

            col("v.flag_rejeitada"),

            col("v.flag_resultado_indefinido"),

            col("v.flag_possui_descricao"),

            col("v.flag_possui_data"),

            lit(1).alias(
                "qtd_votacoes"
            )
        )
    )