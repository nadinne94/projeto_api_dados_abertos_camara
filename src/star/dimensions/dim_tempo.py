from pyspark.sql.functions import (
    col,
    date_format,
    dayofmonth,
    dayofweek,
    month,
    quarter,
    weekofyear,
    year
)


def build_dim_tempo(
    df_proposicoes,
    df_votacoes,
    df_tramitacoes,
    df_eventos
):

    df_datas = (

        df_proposicoes
        .select(
            col("data_apresentacao").alias("data")
        )

        .unionByName(
            df_votacoes.select(
                col("data_votacao").alias("data")
            )
        )

        .unionByName(
            df_tramitacoes.select(
                col("data_tramitacao").alias("data")
            )
        )

        .unionByName(
            df_eventos.select(
                col("data_evento").alias("data")
            )
        )

        .filter(
            col("data").isNotNull()
        )

        .dropDuplicates(
            ["data"]
        )
    )

    return (

        df_datas

        .withColumn(
            "sk_tempo",
            date_format(
                col("data"),
                "yyyyMMdd"
            ).cast("int")
        )

        .withColumn(
            "ano",
            year(col("data"))
        )

        .withColumn(
            "mes",
            month(col("data"))
        )

        .withColumn(
            "nome_mes",
            date_format(
                col("data"),
                "MMMM"
            )
        )

        .withColumn(
            "trimestre",
            quarter(col("data"))
        )

        .withColumn(
            "semana_ano",
            weekofyear(col("data"))
        )

        .withColumn(
            "dia",
            dayofmonth(col("data"))
        )

        .withColumn(
            "dia_semana",
            date_format(
                col("data"),
                "E"
            )
        )

        .withColumn(
            "fim_semana",
            dayofweek(
                col("data")
            ).isin(1, 7)
        )
    )