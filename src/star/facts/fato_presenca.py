from pyspark.sql.functions import (
    col,
    lit
)


def build_fato_presenca_evento(
    df_presencas,
    dim_evento,
    dim_deputado
):

    return (

        df_presencas.alias("p")

        .join(
            dim_evento.alias("e"),
            "id_evento",
            "left"
        )

        .join(
            dim_deputado.alias("d"),
            "id_deputado",
            "left"
        )

        .select(

            col("e.sk_evento"),

            col("d.sk_deputado"),

            col("p.flag_presenca_valida"),

            col("p.flag_evento_encontrado"),

            col("p.flag_deputado_encontrado"),

            lit(1).alias(
                "qtd_presencas"
            )
        )
    )