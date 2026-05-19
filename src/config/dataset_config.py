"""
Dataset configuration.
"""

DATASETS_CONFIG = {

    "deputados": {

        "source": "camara",

        "endpoint": "/deputados",

        "table": "deputados",

        "description":
            "Lista de deputados federais",

        "pagination": True,

        "incremental": False,

        "keys": ["id"]
    },

    "partidos": {

        "source": "camara",

        "endpoint": "/partidos",

        "table": "partidos",

        "description":
            "Lista de partidos",

        "pagination": True,

        "incremental": False,

        "keys": ["id"]
    },

    "proposicoes": {

        "source": "camara",

        "endpoint": "/proposicoes",

        "table": "proposicoes",

        "description":
            "Projetos de lei",

        "pagination": True,

        "incremental": True,

        "incremental_param":
            "dataApresentacaoInicio",

        "incremental_field":
            "dataApresentacao",

        "params": {

            "dataApresentacaoInicio":
                "2023-01-01"
        },

        "keys": ["id"]
    },

    "proposicoes_autores": {

        "source": "camara",

        "endpoint":
            "/proposicoes/{id}/autores",

        "table":
            "proposicoes_autores",

        "description":
            "Autores das proposições",

        "pagination": False,

        "incremental": False,

        "dependency": {

            "parent": "proposicoes",

            "key": "id"
        },

        "keys": [

            "parent_id",

            "nome"
        ]
    },

    "tramitacoes": {

        "source": "camara",

        "endpoint":
            "/proposicoes/{id}/tramitacoes",

        "table":
            "tramitacoes",

        "description":
            "Tramitações das proposições",

        "pagination": False,

        "incremental": False,

        "dependency": {

            "parent": "proposicoes",

            "key": "id"
        },

        "keys": [

            "parent_id",

            "sequencia"
        ]
    },

    "votacoes": {

        "source": "camara",

        "endpoint":
            "/proposicoes/{id}/votacoes",

        "table":
            "votacoes",

        "description":
            "Votações da Câmara",

        "pagination": False,

        "incremental": False,

        "dependency": {

            "parent": "proposicoes",

            "key": "id"
        },

        "keys": [

            "id",

            "parent_id"
        ]
    },

    "votos": {

        "source": "camara",

        "endpoint":
            "/votacoes/{id}/votos",

        "table":
            "votos",

        "description":
            "Votos parlamentares",

        "pagination": False,

        "incremental": False,

        "dependency": {

            "parent": "votacoes",

            "key": "id"
        },

        "keys": ["parent_id"]
    },

    "eventos": {

        "source": "camara",

        "endpoint":
            "/eventos",

        "table":
            "eventos",

        "description":
            "Eventos da Câmara",

        "pagination": True,

        "incremental": True,

        "incremental_param":
            "dataInicio",

        "incremental_field":
            "dataHoraInicio",

        "params": {

            "dataInicio":
                "2023-01-01",

            "dataFim":
                "2026-12-31"
        },

        "keys": ["id"]
    },

    "presencas_eventos": {

        "source": "camara",

        "endpoint":
            "/eventos/{id}/deputados",

        "table":
            "presencas_eventos",

        "description":
            "Presenças em eventos",

        "pagination": False,

        "incremental": False,

        "dependency": {

            "parent": "eventos",

            "key": "id"
        },

        "keys": ["parent_id"]
    }
}