from src.gold.transforms.deputados import (
    transform_deputados
)

from src.gold.transforms.partidos import (
    transform_partidos
)

from src.gold.transforms.eventos import (
    transform_eventos
)

from src.gold.transforms.presencas import (
    transform_presencas
)

from src.gold.transforms.proposicoes import (
    transform_proposicoes
)

from src.gold.transforms.proposicoes_autores import (
    transform_proposicoes_autores
)

from src.gold.transforms.tramitacoes import (
    transform_tramitacoes
)

from src.gold.transforms.votacoes import (
    transform_votacoes
)

from src.gold.transforms.votos import (
    transform_votos
)


TRANSFORMS = {

    "deputados": {

        "fn": transform_deputados,

        "merge_keys": [
            "id_deputado"
        ]
    },

    "partidos": {

        "fn": transform_partidos,

        "merge_keys": [
            "id_partido"
        ]
    },

    "eventos": {

        "fn": transform_eventos,

        "merge_keys": [
            "id_evento"
        ]
    },

    "presencas_eventos": {
        "fn": transform_presencas,
        "merge_keys": [
            "id_evento",
            "id_deputado"
        ]
    },

    "proposicoes": {

        "fn": transform_proposicoes,

        "merge_keys": [
            "id_proposicao"
        ]
    },

    "proposicoes_autores": {

        "fn": transform_proposicoes_autores,

        "merge_keys": [
            "id_proposicao",
            "nome_autor"
        ]
    },

    "tramitacoes": {

        "fn": transform_tramitacoes,

        "merge_keys": [
            "id_proposicao",
            "sequencia"
        ]
    },

    "votacoes": {

        "fn": transform_votacoes,

        "merge_keys": [
            "id_votacao"
        ]
    },

    "votos": {

        "fn": transform_votos,

        "merge_keys": [
            "id_votacao",
            "id_deputado"
        ]
    }

}