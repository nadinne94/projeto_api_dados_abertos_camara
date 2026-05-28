from src.utils.helpers.surrogate import (
    add_surrogate_key
)


def build_dim_proposicao(df_proposicoes):

    df_dim = (

        df_proposicoes

        .select(
            "id_proposicao",
            "sigla_tipo",
            "tipo_documental",
            "categoria_regimental",
            "macrotema",
            "tema_ementa",
            "origem_tema",
            "natureza_juridica",
            "origem_natureza_juridica",
            "peso_regimental",
            "flag_normativa",
            "flag_fiscalizacao",
            "flag_baixo_impacto",
            "flag_social",
            "flag_economico",
            "flag_tema_por_ml",
            "flag_natureza_por_ml",
            "flag_classificacao_automatica"
        )

        .dropDuplicates(
            ["id_proposicao"]
        )
    )

    return add_surrogate_key(
        df=df_dim,
        key_name="sk_proposicao",
        natural_keys=["id_proposicao"]
    )