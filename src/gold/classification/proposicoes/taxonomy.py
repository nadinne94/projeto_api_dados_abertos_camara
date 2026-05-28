from pyspark.sql.functions import (
    col,
    when,
    lit
)


def aplicar_taxonomia_regimental(df):

    return (

        df

        # =================================================
        # PESO REGIMENTAL
        # =================================================

        .withColumn(

            "peso_regimental",

            when(
                col("tipo_documental") == "Norma Material",
                10
            )

            .when(
                col("tipo_documental") == "Fiscalização",
                7
            )

            .when(
                col("tipo_documental") == "Administrativa",
                4
            )

            .when(
                col("tipo_documental") == "Homenagem",
                1
            )

            .otherwise(2)
        )

        # =================================================
        # CATEGORIA REGIMENTAL
        # =================================================

        .withColumn(

            "categoria_regimental",

            when(
                col("tipo_documental") == "Norma Material",
                "Normativa"
            )

            .when(
                col("tipo_documental") == "Fiscalização",
                "Fiscalizatória"
            )

            .when(
                col("tipo_documental") == "Homenagem",
                "Simbólica"
            )

            .otherwise(
                "Administrativa"
            )
        )

        # =================================================
        # MACROTEMA
        # =================================================

        .withColumn(

            "macrotema",

            when(

                col("tema_ementa").isin(
                    "Saúde",
                    "Educação"
                ),

                "Social"
            )

            .when(

                col("tema_ementa").isin(
                    "Economia",
                    "Agricultura"
                ),

                "Econômico"
            )

            .when(

                col("tema_ementa").isin(
                    "Segurança Pública"
                ),

                "Segurança"
            )

            .when(

                col("tema_ementa").isin(
                    "Tecnologia"
                ),

                "Tecnologia"
            )

            .when(

                col("tema_ementa").isin(
                    "Meio Ambiente"
                ),

                "Ambiental"
            )

            .otherwise(
                "Outros"
            )
        )

        # =================================================
        # FLAGS ANALÍTICAS
        # =================================================

        .withColumn(

            "flag_normativa",

            col("categoria_regimental")
            == "Normativa"
        )

        .withColumn(

            "flag_fiscalizacao",

            col("categoria_regimental")
            == "Fiscalizatória"
        )

        .withColumn(

            "flag_baixo_impacto",

            col("peso_regimental") <= 2
        )

        .withColumn(

            "flag_social",

            col("macrotema") == "Social"
        )

        .withColumn(

            "flag_economico",

            col("macrotema") == "Econômico"
        )
    )