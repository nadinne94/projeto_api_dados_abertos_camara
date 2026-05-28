from src.star.dimensions.dim_deputado import (
    build_dim_deputado
)

from src.star.dimensions.dim_partido import (
    build_dim_partido
)

from src.star.dimensions.dim_proposicao import (
    build_dim_proposicao
)

from src.star.dimensions.dim_tempo import (
    build_dim_tempo
)

from src.star.dimensions.dim_evento import (
    build_dim_evento
)

from src.star.dimensions.dim_orgao import (
    build_dim_orgao
)


STAR_DIMENSIONS = {

    "dim_tempo": {

        "fn": build_dim_tempo,

        "table": "dim_tempo",

        "merge_keys": [
            "sk_tempo"
        ],

        "sources": [
            "proposicoes",
            "votacoes",
            "tramitacoes",
            "eventos"
        ]
    },

    "dim_partido": {

        "fn": build_dim_partido,

        "table": "dim_partido",

        "merge_keys": [
            "id_partido"
        ],

        "sources": [
            "partidos"
        ]
    },

    "dim_deputado": {

        "fn": build_dim_deputado,

        "table": "dim_deputado",

        "merge_keys": [
            "id_deputado"
        ],

        "sources": [
            "deputados"
        ]
    },

    "dim_proposicao": {

        "fn": build_dim_proposicao,

        "table": "dim_proposicao",

        "merge_keys": [
            "id_proposicao"
        ],

        "sources": [
            "proposicoes"
        ]
    },

    "dim_orgao": {

        "fn": build_dim_orgao,

        "table": "dim_orgao",

        "merge_keys": [
            "orgao"
        ],

        "sources": [
            "tramitacoes",
            "votacoes"
        ]
    },

    "dim_evento": {

        "fn": build_dim_evento,

        "table": "dim_evento",

        "merge_keys": [
            "id_evento"
        ],

        "sources": [
            "eventos"
        ]
    }
}


DIMENSIONS_EXECUTION_ORDER = [

    "dim_tempo",

    "dim_partido",

    "dim_deputado",

    "dim_proposicao",

    "dim_orgao",

    "dim_evento"
]