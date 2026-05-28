"""
Transformação Gold — Partidos.

Enriquecimento analítico da dimensão partidos.
"""

from pyspark.sql.functions import (
    col,
    upper,
    trim,
    current_timestamp,
    when,
    length
)

from src.gold.classification.partidos.functions import (
    classificar_bloco_ideologico,
    classificar_corrente_ideologica,
    classificar_espectro_politico
)

def transform_partidos(df):

    return (

        df

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        .withColumn(
            "nome_partido",
            trim(col("nome_partido"))
        )

        .withColumn(
            "sigla_partido",
            upper(
                trim(col("sigla_partido"))
            )
        )

        # =================================================
        # FEATURES ANALÍTICAS
        # =================================================

        .withColumn(
            "bloco_ideologico",
            classificar_bloco_ideologico(
                col("sigla_partido")
            )
        )

        .withColumn(
            "corrente_ideologica",
            classificar_corrente_ideologica(
                col("sigla_partido")
            )
        )

        .withColumn(
            "espectro_politico",
            classificar_espectro_politico(
                col("sigla_partido")
            )
        )

        # =================================================
        # FLAGS ANALÍTICAS
        # =================================================

        .withColumn(
            "flag_sigla_valida",
            when(
                col("sigla_partido").isNotNull(),
                1
            ).otherwise(0)
        )

        .withColumn(
            "flag_nome_disponivel",
            when(
                col("nome_partido").isNotNull(),
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