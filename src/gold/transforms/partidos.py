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
    classify_ideological_bloc,
    classify_ideological_current,
    classify_political_spectrum
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
            classify_ideological_bloc(
                col("sigla_partido")
            )
        )

        .withColumn(
            "corrente_ideologica",
            classify_ideological_current(
                col("sigla_partido")
            )
        )

        .withColumn(
            "espectro_politico",
            classify_political_spectrum(
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