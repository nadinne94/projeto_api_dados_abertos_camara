from src.ml.training.labels import (
    classificar_tema_label,
    classificar_natureza_label
)

from src.ml.dictionaries.temas import (
    TEMA_MIN_SCORE,
    TEMA_MIN_MARGIN,
    TEMA_THRESHOLDS,
    TEMA_FALLBACK
)


SOURCE_TABLE_PROPOSICOES = "proposicoes"


CONFIG_TEMA = {

    "reset": False,

    "source_table": SOURCE_TABLE_PROPOSICOES,

    "model_name": "api_dados_abertos.ml.tema_classificador",

    "target_col": "tema_ementa",

    "tabela_treino": "proposicoes_tema_treino",

    "regex_func": classificar_tema_label,

    "fallback": TEMA_FALLBACK,

    "min_score": TEMA_MIN_SCORE,

    "min_margin": TEMA_MIN_MARGIN,

    "thresholds_por_classe": TEMA_THRESHOLDS
}


CONFIG_NATUREZA = {

    "reset": False,

    "source_table": SOURCE_TABLE_PROPOSICOES,

    "model_name": "api_dados_abertos.ml.natureza_classificador",

    "target_col": "natureza_juridica",

    "tabela_treino": "proposicoes_natureza_treino",

    "regex_func": classificar_natureza_label,

    "fallback": "Outros Tipos",

    "min_score": 4,

    "min_margin": 2
}


CLASSIFICADORES_PROPOSICOES = [

    CONFIG_TEMA,

    CONFIG_NATUREZA
]