from src.ml.features.proposicoes import (
    classificar_tema_treino,
    classificar_natureza_juridica_treino
)


CONFIG_TEMA = {

    "reset": True,

    "source_table": "proposicoes",

    "model_name":
        "main.default.tema_classificador",

    "target_col":
        "tema_ementa",

    "tabela_treino":
        "proposicoes_treino",

    "regex_func":
        classificar_tema_treino
}


CONFIG_NATUREZA = {

    "reset": True,

    "source_table": "proposicoes",

    "model_name":
        "main.default.natureza_classificador",

    "target_col":
        "natureza_juridica",

    "tabela_treino":
        "proposicoes_natureza_treino",

    "regex_func":
        classificar_natureza_juridica_treino
}


MODELS = [

    CONFIG_TEMA,

    CONFIG_NATUREZA
]