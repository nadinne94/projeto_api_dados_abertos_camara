from pyspark.sql.functions import (
    col,
    lit,
    trim,
    upper,
    when,
    coalesce,
    date_format
)

from src.gold.classification.tramitacoes.functions import (
    classificar_status_tramitacao
)


def transform_tramitacoes(df):

    return (

        df

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        .withColumn(
            "orgao",
            upper(
                trim(
                    col("orgao")
                )
            )
        )

        .withColumn(
            "descricao_situacao",
            trim(
                coalesce(
                    col("descricao_situacao"),
                    lit("")
                )
            )
        )

        .withColumn(
            "descricao_tramitacao",
            trim(
                coalesce(
                    col("descricao_tramitacao"),
                    lit("")
                )
            )
        )

        .withColumn(
            "despacho",
            trim(
                coalesce(
                    col("despacho"),
                    lit("")
                )
            )
        )

        # =================================================
        # CLASSIFICAÇÃO
        # =================================================

        .withColumn(
            "status",

            classificar_status_tramitacao(
                col("descricao_situacao"),
                col("descricao_tramitacao"),
                col("despacho")
            )
        )

        # =================================================
        # FLAGS
        # =================================================

        .withColumn(
            "flag_finalizada",

            when(
                col("status").isin(
                    "Convertida em Norma",
                    "Rejeitada",
                    "Arquivada"
                ),
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_aprovada",

            when(
                col("status") == "Convertida em Norma",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_rejeitada",

            when(
                col("status").isin(
                    "Rejeitada",
                    "Arquivada"
                ),
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_em_tramitacao",

            when(
                col("flag_finalizada") == 0,
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_ultima_tramitacao",

            when(
                col("rn_tramitacao_recente") == 1,
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        # =================================================
        # DATAS DERIVADAS
        # =================================================

        .withColumn(
            "data_status_final",

            when(
                col("rn_tramitacao_recente") == 1,
                col("data_tramitacao")
            ).otherwise(
                lit(None).cast("date")
            )
        )

        .withColumn(
            "sk_tempo_status_final",

            when(
                col("rn_tramitacao_recente") == 1,

                date_format(
                    col("data_tramitacao"),
                    "yyyyMMdd"
                ).cast("int")
            ).otherwise(
                lit(None).cast("int")
            )
        )
    )