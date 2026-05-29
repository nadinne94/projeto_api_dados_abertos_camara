from pyspark.sql.functions import (
    col,
    date_format,
    lit
)


def build_fato_voto(
    df_votos,
    dim_deputado,
    df_votacoes,
    dim_proposicao
):

    return (

        df_votos.alias("v")

        .join(
            dim_deputado.alias("d"),
            "id_deputado",
            "left"
        )

        .join(
            df_votacoes.select("id_votacao", "id_proposicao").alias("vt"),
            "id_votacao",
            "left"
        )
        .join(
            dim_proposicao.alias("p"),
            "id_proposicao",
            "left"
        )

        .select(

            col("v.id_votacao"),

            col("p.sk_proposicao"),

            col("d.sk_deputado"),

            date_format(
                col("v.data_voto"),
                "yyyyMMdd"
            ).cast("int").alias(
                "sk_tempo_voto"
            ),

            col("v.voto"),

            col("v.categoria_voto"),

            col("v.flag_sim"),

            col("v.flag_nao"),

            col("v.flag_abstencao"),

            col("v.flag_obstrucao"),

            col("v.flag_ausente"),

            col("v.flag_voto_valido"),

            col("v.flag_voto_registrado"),

            lit(1).alias(
                "qtd_votos"
            )
        )
    )