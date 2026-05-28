"""
Transformação Gold — Deputados.

Enriquecimento analítico da dimensão deputados.
"""

from pyspark.sql.functions import (
    col,
    upper,
    lower,
    trim,
    current_timestamp,
    when
)

from src.gold.classification.deputados.functions import (
    classificar_estado,
    classificar_regiao
)

def transform_deputados(df):

    return (

        df

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        .withColumn(
            "nome_deputado",
            trim(col("nome_deputado"))
        )

        .withColumn(
            "sigla_partido",
            upper(
                trim(col("sigla_partido"))
            )
        )

        .withColumn(
            "uf_origem",
            upper(
                trim(col("uf_origem"))
            )
        )

        .withColumn(
            "nome_estado",
            classificar_estado(col("uf_origem"))
        )

        .withColumn(
            "regiao",
            classificar_regiao(col("uf_origem"))
        )

        .withColumn(
            "email",
            lower(
                trim(col("email"))
            )
        )

        # =================================================
        # FLAGS ANALÍTICAS
        # =================================================

        .withColumn(

            "flag_email_disponivel",

            when(
                col("email").isNotNull(),
                1
            ).otherwise(0)
        )

        .withColumn(

            "flag_foto_disponivel",

            when(
                col("url_foto").isNotNull(),
                1
            ).otherwise(0)
        )

        # =================================================
        # AUDITORIA
        # =================================================

        .withColumn(
            "data_gold",
            current_timestamp()
        )
    )