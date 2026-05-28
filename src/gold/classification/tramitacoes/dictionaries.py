STATUS_TRAMITACAO = {

    "Convertida em Norma": [

        r"transformad.*norma",
        r"convertid.*lei",
        r"lei n",
        r"sancionad",
        r"promulgad"
    ],

    "Rejeitada": [

        r"rejeitad",
        r"inconstitucional",
        r"perdeu a eficacia"
    ],

    "Arquivada": [

        r"arquivad",
        r"retirad",
        r"prejudicad",
        r"devolvid"
    ],

    "Em Deliberação": [

        r"ordem do dia",
        r"pauta",
        r"deliberacao",
        r"votacao"
    ],

    "Em Comissão": [

        r"comissao",
        r"relator",
        r"parecer"
    ],

    "Em Recurso": [

        r"recurso"
    ],

    "Encaminhada": [

        r"senado",
        r"executivo",
        r"autografo",
        r"sancao"
    ],

    "Aguardando Despacho": [

        r"despacho do presidente",
        r"aguardando despacho"
    ]
}