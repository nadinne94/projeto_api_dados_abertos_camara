"""
Transformação Gold — Votos.

Enriquecimento analítico dos votos individuais
em votações legislativas.
"""

from pyspark.sql import DataFrame

from pyspark.sql.functions import (
    col,
    upper,
    trim,
    coalesce,
    lit,
    when,
    current_timestamp
)

from src.gold.classification.votos.functions import (
    classificar_voto
)


def transform_votos(
    df: DataFrame
) -> DataFrame:

    return (

        df

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        .withColumn(
            "voto",

            upper(
                trim(
                    coalesce(
                        col("voto"),
                        lit("")
                    )
                )
            )
        )

        .withColumn(
            "nome_deputado",

            trim(
                coalesce(
                    col("nome_deputado"),
                    lit("")
                )
            )
        )

        # =================================================
        # CLASSIFICAÇÃO DO VOTO
        # =================================================

        .withColumn(
            "categoria_voto",

            classificar_voto(
                col("voto")
            )
        )

        # =================================================
        # FLAGS ANALÍTICAS
        # =================================================

        .withColumn(
            "flag_sim",

            when(
                col("categoria_voto") == "Sim",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_nao",

            when(
                col("categoria_voto") == "Não",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_abstencao",

            when(
                col("categoria_voto") == "Abstenção",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_obstrucao",

            when(
                col("categoria_voto") == "Obstrução",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_ausente",

            when(
                col("categoria_voto") == "Ausente",
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_voto_valido",

            when(
                col("categoria_voto").isin(
                    "Sim",
                    "Não"
                ),
                lit(1)
            ).otherwise(
                lit(0)
            )
        )

        .withColumn(
            "flag_voto_registrado",

            when(
                col("voto") != "",
                lit(1)
            ).otherwise(
                lit(0)
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