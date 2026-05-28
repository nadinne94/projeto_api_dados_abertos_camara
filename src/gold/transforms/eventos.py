"""
Transformação Gold — Eventos.
"""

from pyspark.sql.functions import (
    col,
    upper,
    trim,
    current_timestamp,
    when,
    hour,
    dayofweek,
    month,
    year,
    lit
)

from src.gold.classification.eventos.functions import (
    classificar_tipo_evento,
    classificar_status_evento
)


def transform_eventos(df):

    return (

        df

        .withColumn(
            "descricao_evento",
            trim(col("descricao_evento"))
        )

        .withColumn(
            "tipo_evento",
            upper(trim(col("tipo_evento")))
        )

        .withColumn(
            "situacao",
            trim(col("situacao"))
        )

        .withColumn(
            "local_nome",
            trim(col("local_nome"))
        )

        .withColumn(
            "ano_evento",
            year(col("data_evento"))
        )

        .withColumn(
            "mes_evento",
            month(col("data_evento"))
        )

        .withColumn(
            "dia_semana_evento",
            dayofweek(col("data_evento"))
        )

        .withColumn(
            "hora_inicio_evento",
            hour(col("data_hora_inicio"))
        )

        .withColumn(
            "flag_tem_inicio",
            when(col("data_hora_inicio").isNotNull(), lit(1)).otherwise(lit(0))
        )

        .withColumn(
            "flag_tem_fim",
            when(col("data_hora_fim").isNotNull(), lit(1)).otherwise(lit(0))
        )

        .withColumn(
            "flag_tem_local",
            when(col("local_nome").isNotNull(), lit(1)).otherwise(lit(0))
        )

        .withColumn(
            "situacao_evento",
            classificar_status_evento(col("situacao"))
        )

        .withColumn(
            "tipo_evento_classificado",
            classificar_tipo_evento(col("tipo_evento"))
        )

        .withColumn(
            "tipo_local",
            when(col("local_nome").isNotNull(), lit("Local informado"))
            .otherwise(lit("Local não informado"))
        )

        .withColumn(
            "flag_evento_realizado",
            when(col("situacao_evento") == "Realizado", lit(1)).otherwise(lit(0))
        )

        .withColumn(
            "data_gold",
            current_timestamp()
        )
    )