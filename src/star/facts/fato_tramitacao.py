from pyspark.sql.functions import (
    col,
    trim,
    upper,
    lit,
    date_format
)


def build_fato_tramitacao(
    df_tramitacoes,
    dim_proposicao,
    dim_orgao
):

    tramitacoes = (

        df_tramitacoes

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

        tramitacoes.alias("t")

        .join(
            dim_proposicao.alias("p"),
            col("t.id_proposicao")
            == col("p.id_proposicao"),
            "left"
        )

        .join(
            orgaos.alias("o"),
            col("t.orgao_norm")
            == col("o.orgao_norm"),
            "left"
        )

        .select(

            col("p.sk_proposicao"),

            col("o.sk_orgao"),

            date_format(
                col("t.data_tramitacao"),
                "yyyyMMdd"
            ).cast("int").alias(
                "sk_tempo"
            ),

            col("t.sk_tempo_status_final"),

            col("t.id_proposicao"),

            col("t.sequencia"),

            col("t.cod_situacao"),

            col("t.status"),

            col("t.descricao_situacao"),

            col("t.descricao_tramitacao"),

            col("t.data_tramitacao"),

            col("t.data_status_final"),

            col("t.rn_tramitacao_recente"),

            col("t.flag_finalizada").cast("int").alias(
                "flag_finalizada"
            ),

            col("t.flag_aprovada").cast("int").alias(
                "flag_aprovada"
            ),

            col("t.flag_rejeitada").cast("int").alias(
                "flag_rejeitada"
            ),

            col("t.flag_em_tramitacao").cast("int").alias(
                "flag_em_tramitacao"
            ),

            col("t.flag_ultima_tramitacao").cast("int").alias(
                "flag_ultima_tramitacao"
            ),

            lit(1).alias(
                "qtd_tramitacoes"
            )
        )
    )