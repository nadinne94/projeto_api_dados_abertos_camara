"""
Transformação Gold — Votações.

Enriquecimento analítico das votações legislativas.
"""

from pyspark.sql import DataFrame

from pyspark.sql.functions import (
    col,
    when,
    lit,
    trim,
    upper,
    coalesce,
    year,
    month,
    quarter,
    current_timestamp
)

from src.gold.classification.votacoes.functions import (
    classificar_resultado_votacao
)


def transform_votacoes(
    df: DataFrame
) -> DataFrame:

    return (

        df

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        .withColumn(
            "orgao",

            upper(
                trim(
                    coalesce(
                        col("orgao"),
                        lit("")
                    )
                )
            )
        )

        .withColumn(
            "descricao_votacao",

            trim(
                coalesce(
                    col("descricao_votacao"),
                    lit("")
                )
            )
        )

        # =================================================
        # CLASSIFICAÇÃO RESULTADO
        # =================================================

        .withColumn(
            "resultado_votacao",

            classificar_resultado_votacao(
                col("aprovacao")
            )
        )

        # =================================================
        # FLAGS ANALÍTICAS
        # =================================================

        .withColumn(
            "flag_aprovada",

            when(
                col("aprovacao") == True,
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_rejeitada",

            when(
                col("aprovacao") == False,
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_resultado_indefinido",

            when(
                col("aprovacao").isNull(),
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_possui_descricao",

            when(
                col("descricao_votacao") != "",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_possui_data",

            when(
                col("data_votacao").isNotNull(),
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        # =================================================
        # FEATURES TEMPORAIS
        # =================================================

        .withColumn(
            "ano_votacao",

            year(
                col("data_votacao")
            )
        )

        .withColumn(
            "mes_votacao",

            month(
                col("data_votacao")
            )
        )

        .withColumn(
            "trimestre_votacao",

            quarter(
                col("data_votacao")
            )
        )

        # =================================================
        # AUDITORIA
        # =================================================

        .withColumn(
            "data_gold",
            current_timestamp()
        )
    )