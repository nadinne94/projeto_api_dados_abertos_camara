from pyspark.sql.functions import (
    col,
    to_date,
    to_timestamp,
    coalesce,
    current_timestamp
)

def transform_eventos(df):

    return (
        df.select(
            col("id").cast("string").alias("id_evento"),

            to_date(
                coalesce(
                    col("dataHoraInicio"),
                    col("dataHoraFim")
                )
            ).alias("data_evento"),

            to_timestamp(
                col("dataHoraInicio")
            ).alias("data_hora_inicio"),

            to_timestamp(
                col("dataHoraFim")
            ).alias("data_hora_fim"),

            col("descricao")
                .alias("descricao_evento"),

            col("descricaoTipo")
                .alias("tipo_evento"),

            col("situacao"),

            col("localCamara")
                .alias("local_nome"),

            current_timestamp()
                .alias("data_processamento")
        )
        .dropDuplicates(["id_evento"])
    )