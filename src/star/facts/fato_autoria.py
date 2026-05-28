from pyspark.sql.functions import (
    col,
    lit
)


def build_fato_autoria(
    df_autores,
    dim_proposicao,
    dim_deputado
):

    return (

        df_autores.alias("a")

        .join(
            dim_proposicao.alias("p"),
            "id_proposicao",
            "left"
        )

        .join(
            dim_deputado.alias("d"),
            "id_deputado",
            "left"
        )

        .select(

            col("p.sk_proposicao"),

            col("d.sk_deputado"),

            col("a.tipo_autor"),

            col("a.tipo_autor_classificado"),

            col("a.papel_autor"),

            col("a.ordem_assinatura"),

            col("a.proponente").cast("int").alias(
                "flag_proponente"
            ),

            col("a.flag_autor_principal").cast("int").alias(
                "flag_autor_principal"
            ),

            lit(1).alias(
                "qtd_autorias"
            )
        )
    )