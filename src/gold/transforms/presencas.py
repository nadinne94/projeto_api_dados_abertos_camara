"""
Transformação Gold — Presenças em eventos.

Enriquecimento analítico das participações de deputados
em eventos legislativos.
"""

from pyspark.sql.functions import (
    col,
    upper,
    trim,
    current_timestamp,
    when,
    lit
)


def transform_presencas(
    df,
    df_deputados=None,
    df_eventos=None
):

    df_gold = (

        df

        .withColumn(
            "nome_deputado",
            trim(
                col("nome_deputado")
            )
        )

        .withColumn(
            "sigla_partido",
            upper(
                trim(
                    col("sigla_partido")
                )
            )
        )

        .withColumn(
            "uf_origem",
            upper(
                trim(
                    col("uf_origem")
                )
            )
        )
    )

    if df_deputados is not None:

        df_dep = (

            df_deputados

            .select(
                col("id_deputado"),
                col("nome_deputado").alias(
                    "nome_deputado_cadastro"
                ),
                col("email").alias(
                    "email_deputado"
                )
            )

            .dropDuplicates(
                ["id_deputado"]
            )
        )

        df_gold = (

            df_gold

            .join(
                df_dep,
                "id_deputado",
                "left"
            )
        )

    else:

        df_gold = (

            df_gold

            .withColumn(
                "nome_deputado_cadastro",
                lit(None).cast("string")
            )

            .withColumn(
                "email_deputado",
                lit(None).cast("string")
            )
        )

    if df_eventos is not None:

        df_evt = (

            df_eventos

            .select(
                "id_evento",
                "tipo_evento",
                "status_evento",
                "data_evento"
            )

            .dropDuplicates(
                ["id_evento"]
            )
        )

        df_gold = (

            df_gold

            .join(
                df_evt,
                "id_evento",
                "left"
            )
        )

    else:

        df_gold = (

            df_gold

            .withColumn(
                "tipo_evento",
                lit(None).cast("string")
            )

            .withColumn(
                "status_evento",
                lit(None).cast("string")
            )

            .withColumn(
                "data_evento",
                lit(None).cast("date")
            )
        )

    return (

        df_gold

        .withColumn(
            "flag_presenca_valida",

            when(
                col("id_deputado").isNotNull()
                & col("id_evento").isNotNull(),
                1
            ).otherwise(0)
        )

        .withColumn(
            "flag_evento_encontrado",

            when(
                col("data_evento").isNotNull(),
                1
            ).otherwise(0)
        )

        .withColumn(
            "flag_deputado_encontrado",

            when(
                col("nome_deputado_cadastro").isNotNull(),
                1
            ).otherwise(0)
        )

        .withColumn(
            "data_gold",
            current_timestamp()
        )
    )