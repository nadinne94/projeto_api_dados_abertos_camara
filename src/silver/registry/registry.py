from src.silver.transforms.deputados import transform_deputados
from src.silver.transforms.partidos import transform_partidos
from src.silver.transforms.proposicoes import transform_proposicoes
from src.silver.transforms.tramitacoes import transform_tramitacoes
from src.silver.transforms.proposicoes_autores import transform_autores
from src.silver.transforms.eventos import transform_eventos
from src.silver.transforms.presencas import transform_presencas
from src.silver.transforms.votacoes import transform_votacoes
from src.silver.transforms.votos import transform_votos

TRANSFORMS = {

    "deputados": {
        "fn": transform_deputados,
        "merge_keys": ["id_deputado"]
    },

    "partidos": {
        "fn": transform_partidos,
        "merge_keys": ["id_partido"]
    },

    "proposicoes": {
        "fn": transform_proposicoes,
        "merge_keys": ["id_proposicao"]
    },

    "proposicoes_autores": {
        "fn": transform_autores,

        # ajuste recomendado
        "merge_keys": [
            "id_proposicao",
            "nome_autor",
            "ordem_assinatura"
        ]
    },

    "tramitacoes": {
        "fn": transform_tramitacoes,
        "merge_keys": [
            "id_proposicao",
            "sequencia"
        ]
    },

    "eventos": {
        "fn": transform_eventos,
        "merge_keys": ["id_evento"]
    },

    "presencas_eventos": {
        "fn": transform_presencas,
        "merge_keys": [
            "id_evento",
            "id_deputado"
        ]
    },

    "votacoes": {
        "fn": transform_votacoes,
        "merge_keys": ["id_votacao"]
    },

    "votos": {
        "fn": transform_votos,
        "merge_keys": [
            "id_votacao",
            "id_deputado"
        ]
    }
}