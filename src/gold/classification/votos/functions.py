from pyspark.sql.functions import (
    lower,
    trim,
    coalesce,
    when,
    lit
)


def classificar_voto(col_voto):

    voto = lower(
        trim(
            coalesce(
                col_voto,
                lit("")
            )
        )
    )

    return (
        when(
            voto == "sim",
            lit("Sim")
        )

        .when(
            voto.isin(
                "não",
                "nao"
            ),
            lit("Não")
        )

        .when(
            voto.rlike("absten"),
            lit("Abstenção")
        )

        .when(
            voto.rlike("obstru"),
            lit("Obstrução")
        )

        .when(
            voto.rlike("ausente|falta"),
            lit("Ausente")
        )

        .otherwise(
            lit("Outros")
        )
    )