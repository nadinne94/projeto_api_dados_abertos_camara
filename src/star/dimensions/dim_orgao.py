from pyspark.sql.functions import (
    col,
    trim
)

from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_orgao(
    df_tramitacoes,
    df_votacoes
):

    df_orgaos = (

        df_tramitacoes

        .select(
            trim(
                col("orgao")
            ).alias("orgao")
        )

        .unionByName(

            df_votacoes.select(
                trim(
                    col("orgao")
                ).alias("orgao")
            )
        )

        .filter(
            col("orgao").isNotNull()
        )

        .dropDuplicates(
            ["orgao"]
        )
    )

    return add_surrogate_key(
        df_orgaos,
        "sk_orgao"
    )