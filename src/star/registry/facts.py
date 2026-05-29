from src.star.facts.fato_proposicao import (
    build_fato_proposicao
)

from src.star.facts.fato_autoria import (
    build_fato_autoria
)

from src.star.facts.fato_tramitacao import (
    build_fato_tramitacao
)

from src.star.facts.fato_votacao import (
    build_fato_votacao
)

from src.star.facts.fato_voto import (
    build_fato_voto
)

from src.star.facts.fato_evento import (
    build_fato_evento
)

from src.star.facts.fato_presenca import (
    build_fato_presenca_evento
)

STAR_FACTS = {

    "fato_proposicao": {
        "fn": build_fato_proposicao,
        "table": "fato_proposicao",
        "merge_keys": ["sk_proposicao"],
        "sources": [
            "gold.proposicoes",
            "star.dim_proposicao"
        ]
    },

    "fato_autoria": {
        "fn": build_fato_autoria,
        "table": "fato_autoria",
        "merge_keys": [
            "sk_proposicao",
            "sk_deputado",
            "ordem_assinatura"
        ],
        "sources": [
            "gold.proposicoes_autores",
            "star.dim_proposicao",
            "star.dim_deputado"
        ]
    },

    "fato_tramitacao": {
        "fn": build_fato_tramitacao,
        "table": "fato_tramitacao",
        "merge_keys": [
            "id_proposicao",
            "sequencia"
        ],
        "sources": [
            "gold.tramitacoes",
            "star.dim_proposicao",
            "star.dim_orgao"
        ]
    },

    "fato_votacao": {
        "fn": build_fato_votacao,
        "table": "fato_votacao",
        "merge_keys": ["id_votacao"],
        "sources": [
            "gold.votacoes",
            "star.dim_proposicao",
            "star.dim_orgao"
        ]
    },

    "fato_voto": {
        "fn": build_fato_voto,
        "table": "fato_voto",
        "merge_keys": [
            "id_votacao",
            "sk_deputado"
        ],
        "sources": [
            "gold.votos",
            "star.dim_deputado",
            "gold.votacoes",
            "star.dim_proposicao"
        ]
    },

    "fato_evento": {
        "fn": build_fato_evento,
        "table": "fato_evento",
        "merge_keys": ["sk_evento"],
        "sources": [
            "gold.eventos",
            "star.dim_evento"
        ]
    },

    "fato_presenca": {
        "fn": build_fato_presenca_evento,
        "table": "fato_presenca",
        "merge_keys": [
            "sk_evento",
            "sk_deputado"
        ],
        "sources": [
            "gold.presencas_eventos",
            "star.dim_evento",
            "star.dim_deputado"
        ]
    }
}

FACTS_EXECUTION_ORDER = [

    # ==========================
    # FATOS
    # ==========================

    "fato_proposicao",

    "fato_autoria",

    "fato_tramitacao",

    "fato_votacao",

    "fato_voto",

    "fato_evento",

    "fato_presenca"
]