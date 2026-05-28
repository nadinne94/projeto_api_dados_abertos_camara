from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_partido(df_partidos):

    df_dim = (

        df_partidos

        .select(
            "id_partido",
            "sigla_partido",
            "nome_partido",
            "espectro_politico",
            "corrente_ideologica",
            "bloco_ideologico"
        )

        .dropDuplicates(
            ["id_partido"]
        )
    )

    return add_surrogate_key(
        df_dim,
        "sk_partido"
    )