# =========================================================
# NATUREZA JURÍDICA
# =========================================================

NATUREZA_REGEX = {

    "Outorga / Concessão": [

        (r"\boutorga\b", 5),

        (r"\bconcessao\b", 5),

        (r"\bpermissao\b", 4),

        (r"autoriza\s+(a\s+)?explorar\s+servico", 6)
    ],

    "Alteração Legislativa": [

        (r"\baltera\b", 5),

        (r"\bmodifica\b", 4),

        (r"\brevoga\b", 5),

        (r"\bacrescenta\b", 4),

        (r"\binclui\b", 4),

        (r"\bsuprime\b", 4),

        (r"\bsubstitui\b", 4),

        (r"nova\s+redacao", 4)
    ],

    "Consolidação Legislativa": [

        (r"\bestatuto\b", 5),

        (r"\bcodigo\b", 5),

        (r"\bconsolida\b", 5)
    ],

    "Ato Simbólico": [

        (r"dia nacional", 6),

        (r"confere o titulo", 6),

        (r"\bdenomina\b", 5)
    ],

    "Norma Material": [

        (r"\binstitui\b", 5),

        (r"\bcria\b", 4),

        (r"\bregulamenta\b", 5),

        (r"dispoe\s+sobre", 3)
    ]
}