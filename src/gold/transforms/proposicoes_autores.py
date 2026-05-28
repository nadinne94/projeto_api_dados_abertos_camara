from pyspark.sql.functions import (
    col,
    lower,
    trim,
    lit
)

from src.gold.classification.autores.functions import (
    classificar_papel_autor,
    classificar_tipo_autor
)


def transform_proposicoes_autores(
    df,
    df_deputados=None
):

    df_gold = df.withColumn(
        "nome_norm",
        lower(
            trim(
                col("nome_autor")
            )
        )
    )

    if df_deputados is not None:

        deputados_clean = (

            df_deputados

            .select(
                "id_deputado",

                lower(
                    trim(
                        col("nome_deputado")
                    )
                ).alias(
                    "nome_norm"
                )
            )

            .dropDuplicates(
                ["nome_norm"]
            )
        )

        df_gold = (

            df_gold

            .join(
                deputados_clean,
                "nome_norm",
                "left"
            )
        )

    else:

        df_gold = df_gold.withColumn(
            "id_deputado",
            lit(None).cast("string")
        )

    return (

        df_gold

        .drop(
            "nome_norm"
        )

        .withColumn(
            "papel_autor",

            classificar_papel_autor(
                col("ordem_assinatura")
            )
        )

        .withColumn(
            "flag_autor_principal",

            col("ordem_assinatura") == 1
        )

        .withColumn(
            "tipo_autor_classificado",

            classificar_tipo_autor(
                col("tipo_autor")
            )
        )
    )