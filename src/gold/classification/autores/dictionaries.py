"""
Dicionários de classificação de autoria.

Centraliza mapeamentos usados para identificar papéis e tipos de autores
associados às proposições legislativas.
"""

TIPO_AUTOR_RULES = {

    "Deputado(a)": [
        r"deputad"
    ],

    "Comissão": [
        r"comissão",
        r"comissao"
    ],

    "Mesa Diretora": [
        r"mesa"
    ],

    "Poder Executivo": [
        r"executivo",
        r"presidência",
        r"presidencia"
    ]
}