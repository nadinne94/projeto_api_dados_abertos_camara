"""
Configurações de treinamento dos modelos de classificação.

Centraliza os parâmetros usados na geração da base de treino, criação de
features, divisão treino/teste, vetorização textual, treinamento,
avaliação e registro dos modelos.

As configurações deste módulo permitem padronizar o treinamento dos
classificadores de tema e natureza jurídica.
"""


import os

from dotenv import load_dotenv

from src.ml.training.labels import (
    classify_topic_label,
    classify_legal_nature_label
)

from src.ml.dictionaries.temas import (
    TEMA_MIN_SCORE,
    TEMA_MIN_MARGIN,
    TEMA_THRESHOLDS,
    TEMA_FALLBACK
)


load_dotenv()

SOURCE_TABLE_PROPOSICOES = "proposicoes"


CONFIG_TEMA = {

    "reset": False,

    "source_table": SOURCE_TABLE_PROPOSICOES,

    "model_name": os.getenv(
        "MLFLOW_TEMA_MODEL_NAME",
        "api_dados_abertos.ml.tema_classificador",
    ),

    "target_col": "tema_ementa",

    "training_table": "proposicoes_tema_treino",

    "regex_func": classify_topic_label,

    "fallback": TEMA_FALLBACK,

    "min_score": TEMA_MIN_SCORE,

    "min_margin": TEMA_MIN_MARGIN,

    "class_thresholds": TEMA_THRESHOLDS
}


CONFIG_NATUREZA = {

    "reset": False,

    "source_table": SOURCE_TABLE_PROPOSICOES,

    "model_name": os.getenv(
        "MLFLOW_NATUREZA_MODEL_NAME",
        "api_dados_abertos.ml.natureza_classificador",
    ),

    "target_col": "natureza_juridica",

    "training_table": "proposicoes_natureza_treino",

    "regex_func": classify_legal_nature_label,

    "fallback": "Outros Tipos",

    "min_score": 4,

    "min_margin": 2
}


CLASSIFICADORES_PROPOSICOES = [

    CONFIG_TEMA,

    CONFIG_NATUREZA
]