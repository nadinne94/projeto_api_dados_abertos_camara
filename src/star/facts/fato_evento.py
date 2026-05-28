from pyspark.sql.functions import (
    col,
    lit,
    date_format
)


def build_fato_evento(
    df_eventos,
    dim_evento
):

    return (

        df_eventos.alias("e")

        .join(
            dim_evento.alias("d"),
            "id_evento",
            "left"
        )

        .select(

            col("d.sk_evento"),

            date_format(
                col("e.data_evento"),
                "yyyyMMdd"
            ).cast("int").alias(
                "sk_tempo"
            ),

            col("e.flag_tem_inicio"),

            col("e.flag_tem_fim"),

            col("e.flag_tem_local"),

            col("e.flag_evento_realizado").cast("int").alias(
                "flag_evento_realizado"
            ),

            lit(1).alias(
                "qtd_eventos"
            )
        )
    )