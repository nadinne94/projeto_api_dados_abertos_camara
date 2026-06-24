"""
Taxonomia de classificação legislativa.

Centraliza categorias, hierarquias e mapeamentos usados para organizar
os temas e classificações aplicadas às proposições legislativas.

Este módulo apoia a padronização das classes utilizadas nas regras,
features, treinamento e documentação do modelo.
"""


TAXONOMIA_REGIMENTAL = {

    "PL": {
        "categoria": "Normativa",
        "peso": 10,
        "tipo_documental": "Projeto de Lei"
    },

    "PLP": {
        "categoria": "Normativa",
        "peso": 10,
        "tipo_documental": "Projeto de Lei Complementar"
    },

    "PEC": {
        "categoria": "Constitucional",
        "peso": 10,
        "tipo_documental": "PEC"
    },

    "PDL": {
        "categoria": "Deliberativa",
        "peso": 8,
        "tipo_documental": "Projeto de Decreto Legislativo"
    },

    "REQ": {
        "categoria": "Procedimental",
        "peso": 3,
        "tipo_documental": "Requerimento"
    },

    "RIC": {
        "categoria": "Fiscalizatória",
        "peso": 4,
        "tipo_documental": "Requerimento de Informação"
    }
}