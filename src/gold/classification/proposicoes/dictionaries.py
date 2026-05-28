# =========================================================
# TIPO DOCUMENTAL
# =========================================================

TIPOS_DOCUMENTAIS = {

    "Norma Material": [

        r"\binstitui\b",
        r"\baltera\b",
        r"\bdispõe\b",
        r"\bcria\b",
        r"\bestabelece\b",
        r"\bregulamenta\b"
    ],

    "Fiscalização": [

        r"\brequer informacoes\b",
        r"\brequerimento de informacao\b",
        r"\bconvoca\b",
        r"\baudiencia publica\b",
        r"\bfiscalizacao\b"
    ],

    "Homenagem": [

        r"\bdenomina\b",
        r"\bmo[cç]ao\b",
        r"\bhomenagem\b",
        r"\bvoto de louvor\b"
    ],

    "Administrativa": [

        r"\bmesa diretora\b",
        r"\bregimento interno\b",
        r"\borganizacao administrativa\b"
    ]
}


# =========================================================
# CATEGORIAS REGIMENTAIS
# =========================================================

CATEGORIAS_REGIMENTAIS = {

    "Normativa": [

        r"\bprojeto de lei\b",
        r"\bpec\b",
        r"\bmedida provisoria\b",
        r"\bsubstitutivo\b"
    ],

    "Fiscalizatória": [

        r"\brequerimento de informacao\b",
        r"\bconvocacao\b",
        r"\baudiencia publica\b"
    ],

    "Simbólica": [

        r"\bhomenagem\b",
        r"\bdenominacao\b",
        r"\bsessao solene\b"
    ]
}