# =========================================================
# TEMA — REGEX RULES
# =========================================================

TEMA_REGEX_RULES = {

    # -----------------------------------------------------
    # SAÚDE
    # -----------------------------------------------------
    "Saúde": [

        (r"\bsaude\b", 6),
        (r"\bsaude publica\b", 7),
        (r"\bsus\b", 8),
        (r"\bsistema unico de saude\b", 8),

        (r"\bhospital(is)?\b", 6),
        (r"\bmedicamento(s)?\b", 7),
        (r"\bvacina(s)?\b", 7),
        (r"\bvacinacao\b", 7),
        (r"\bimunizacao\b", 7),

        (r"\btratamento medico\b", 6),
        (r"\btratamento de saude\b", 6),
        (r"\btratamento hospitalar\b", 6),
        (r"\btratamento\b", 2),

        (r"\bmedico(s)?\b", 4),
        (r"\bpaciente(s)?\b", 4),
        (r"\bdiagnostico\b", 5),
        (r"\bdoenca(s)?\b", 5),

        (r"\bcancer\b", 8),
        (r"\bsaude mental\b", 7),
        (r"\batencao primaria\b", 7),
        (r"\bsamu\b", 7),
        (r"\bambulancia\b", 6),

        (r"\bzoonose(s)?\b", 8),
        (r"\bcastracao animal\b", 7),
        (r"\bcontrole populacional\b", 5),
        (r"\bfibromialgia\b", 7),
        (r"\bmetanol\b", 5),
        (r"\bhipertermia maligna\b", 8),
        (r"\bmorte materna\b", 7),
        (r"\breabilitacao\b", 5)
    ],

    # -----------------------------------------------------
    # EDUCAÇÃO
    # -----------------------------------------------------
    "Educação": [

        (r"\beducacao\b", 6),
        (r"\bensino\b", 5),
        (r"\bescola(s)?\b", 5),
        (r"\buniversidade(s)?\b", 5),
        (r"\bfaculdade(s)?\b", 5),

        (r"\bprofessor(es)?\b", 6),
        (r"\baluno(s)?\b", 4),
        (r"\bestudante(s)?\b", 4),
        (r"\bcreche(s)?\b", 5),
        (r"\bmagisterio\b", 6),
        (r"\bmec\b", 6),

        (r"\bensino medio\b", 7),
        (r"\bensino fundamental\b", 7),
        (r"\beducacao basica\b", 7),
        (r"\beducacao superior\b", 7),
        (r"\beducacao infantil\b", 7),

        (r"\bmerenda escolar\b", 7),
        (r"\bmaterial escolar\b", 5),
        (r"\bbolsa de estudo\b", 6),
        (r"\beducacao financeira\b", 6),
        (r"\bead\b", 5),
        (r"\beducacao a distancia\b", 6)
    ],

    # -----------------------------------------------------
    # COMUNICAÇÃO E RADIODIFUSÃO
    # -----------------------------------------------------
    "Comunicação e Radiodifusão": [

        (r"\bradiodifusao\b", 8),
        (r"\bservico de radiodifusao\b", 9),
        (r"\bradiodifusao sonora\b", 9),

        (r"\btelecomunicac", 7),
        (r"\bemissora\b", 5),
        (r"\bfrequencia\b", 5),
        (r"\bradio\b", 4),
        (r"\btelevisao\b", 4),
        (r"\bfm\b", 4),
        (r"\boutorga\b", 5),
        (r"\bconcessao\b", 5),
        (r"\bpermissao\b", 5),
        (r"\bautorizacao\b", 4),
        (r"\bcomunitaria\b", 3),
        (r"\bfust\b", 7),
        (r"\binternet de alta velocidade\b", 6)
    ],

    # -----------------------------------------------------
    # DATAS COMEMORATIVAS
    # -----------------------------------------------------
    "Datas Comemorativas e Homenagens": [

        (r"dia\s+\d{1,2}\s+de", 5),
        (r"dia nacional", 3),
        (r"dia internacional", 3),
        (r"institui\s+o\s+dia", 3),
        (r"institui\s+o\s+mes", 4),
        (r"institui\s+a\s+semana", 4),
        (r"semana nacional", 4),
        (r"mes nacional", 4),
        (r"campanha nacional", 4)
    ],

    # -----------------------------------------------------
    # HOMENAGENS E DENOMINAÇÕES
    # -----------------------------------------------------
    "Homenagens e Denominações": [

        (r"confere o titulo", 7),
        (r"\bdenomina\b", 7),
        (r"inscreve o nome", 7),

        (r"mo[cç]ao de aplauso", 7),
        (r"mo[cç]ao de aplausos", 7),
        (r"mo[cç]ao de louvor", 7),
        (r"voto de louvor", 7),
        (r"voto de aplauso", 7),

        (r"sessao solene em homenagem", 7),
        (r"\bhomenagem\b", 6),
        (r"\bhomenageia\b", 6),
        (r"\blouvor\b", 5),
        (r"\baplauso(s)?\b", 5)
    ],

    # -----------------------------------------------------
    # MEIO AMBIENTE
    # -----------------------------------------------------
    "Meio Ambiente": [

        (r"\bmeio ambiente\b", 6),
        (r"\bambiental\b", 7),
        (r"\bambientais\b", 7),
        (r"\bsustentabilidade\b", 7),
        (r"\bdesenvolvimento sustentavel\b", 8),

        (r"\bbiodiversidade\b", 8),
        (r"\bdesmatamento\b", 8),
        (r"\bconservacao ambiental\b", 8),
        (r"\bunidade(s)? de conservacao\b", 8),
        (r"\bpreservacao\b", 6),

        (r"\bclima\b", 6),
        (r"\bmudanca do clima\b", 8),
        (r"\bmudancas climaticas\b", 8),
        (r"\bemissao de carbono\b", 7),
        (r"\bgases de efeito estufa\b", 8),

        (r"\blicenciamento ambiental\b", 8),
        (r"\bresiduo(s)? solido(s)?\b", 7),
        (r"\breciclagem\b", 7),
        (r"\bpoluicao\b", 7),
        (r"\bherbicida(s)?\b", 7),
        (r"\bagrotoxico(s)?\b", 7),

        (r"\benergia limpa\b", 7),
        (r"\btransicao energetica\b", 8),
        (r"\bcarbono\b", 7),
        (r"\bcredito de carbono\b", 8),
        (r"\breserva legal\b", 7),
        (r"\bcodigo florestal\b", 8),
        (r"\bqueimada(s)?\b", 7),
        (r"\bamazonia\b", 6),
        (r"\bbioma\b", 7)
    ],

    # -----------------------------------------------------
    # SEGURANÇA PÚBLICA
    # -----------------------------------------------------
    "Segurança Pública": [

        (r"\bseguranca publica\b", 9),
        (r"\bsistema unico de seguranca publica\b", 9),
        (r"\bsusp\b", 8),

        (r"\bpolicia\b", 6),
        (r"\bpolicial(is)?\b", 6),
        (r"\bpolicia militar\b", 8),
        (r"\bpolicia civil\b", 8),
        (r"\bpolicia federal\b", 8),
        (r"\bguarda municipal\b", 7),

        (r"\bcrime(s)?\b", 5),
        (r"\bcriminal\b", 5),
        (r"\bviolencia\b", 6),
        (r"\bprisao\b", 6),
        (r"\bpenitenciari[oa]\b", 7),
        (r"\bsistema prisional\b", 8),

        (r"\barmas?\b", 5),
        (r"\bmunicao\b", 5),
        (r"\bfeminicidio\b", 8),
        (r"\bhomicidio\b", 7),
        (r"\btrafico de drogas\b", 8),
        (r"\borganiza[cç]ao criminosa\b", 8)
    ],

    # -----------------------------------------------------
    # ECONOMIA
    # -----------------------------------------------------
    "Economia": [

        (r"\beconomia\b", 7),
        (r"\beconomico\b", 6),
        (r"\beconomica\b", 6),

        (r"\btributo(s)?\b", 7),
        (r"\btributaria\b", 7),
        (r"\btributario\b", 7),
        (r"\bimposto(s)?\b", 7),
        (r"\btaxa(s)?\b", 5),
        (r"\bcontribuicao\b", 5),

        (r"\borcamento\b", 6),
        (r"\bdespesa(s)? publica(s)?\b", 3),
        (r"\breceita(s)? publica(s)?\b", 3),
        (r"\brenuncia de receita\b", 8),
        (r"\bresponsabilidade fiscal\b", 8),

        (r"\bcredito\b", 5),
        (r"\bfinanciamento\b", 5),
        (r"\bincentivo fiscal\b", 8),
        (r"\bsubsidio\b", 6),

        (r"\bmercado financeiro\b", 8),
        (r"\bbanco central\b", 8),
        (r"\binflacao\b", 7),
        (r"\bjuros\b", 6),
        (r"\bdivida publica\b", 8)
    ],

    # -----------------------------------------------------
    # AGRICULTURA
    # -----------------------------------------------------
    "Agricultura": [

        (r"\bagricultura\b", 8),
        (r"\bagricola\b", 7),
        (r"\bagropecuaria\b", 8),
        (r"\bagropecuario\b", 8),
        (r"\bagro\b", 5),

        (r"\bprodutor rural\b", 8),
        (r"\bpequeno produtor\b", 7),
        (r"\bagricultura familiar\b", 8),
        (r"\bassentamento\b", 5),
        (r"\breforma agraria\b", 8),

        (r"\bpecuaria\b", 7),
        (r"\bsafra\b", 6),
        (r"\bplantio\b", 6),
        (r"\birrigacao\b", 6),
        (r"\bcredito rural\b", 8),

        (r"\bdefesa agropecuaria\b", 8),
        (r"\bsanidade animal\b", 8),
        (r"\bsanidade vegetal\b", 8),
        (r"\babastecimento\b", 5),

        (r"\bdefensivo agricola\b", 8),
        (r"\bcooperativa agricola\b", 7),
        (r"\bagronegocio\b", 8),
        (r"\bcultivo\b", 6),
        (r"\bcolheita\b", 6),
        (r"\bgrao(s)?\b", 5)
    ],

    # -----------------------------------------------------
    # TECNOLOGIA
    # -----------------------------------------------------
    "Tecnologia": [

        (r"\btecnologia\b", 7),
        (r"\btecnologico\b", 6),
        (r"\btecnologica\b", 6),

        (r"\binovacao\b", 7),
        (r"\bciencia, tecnologia e inovacao\b", 9),
        (r"\btransformacao digital\b", 8),
        (r"\bdigitalizacao\b", 7),

        (r"\binteligencia artificial\b", 9),
        (r"\bia\b", 5),
        (r"\balgoritmo(s)?\b", 7),
        (r"\bprotecao de dados\b", 8),
        (r"\bdados pessoais\b", 7),
        (r"\bbanco de dados\b", 6),
        (r"\bprotecao de dados\b", 8),
        (r"\blgpd\b", 8),

        (r"\bseguranca cibernetica\b", 9),
        (r"\bciberseguranca\b", 9),
        (r"\binternet\b", 5),
        (r"\bsoftware\b", 6),
        (r"\bprogramacao\b", 6),
        (r"\bstartup(s)?\b", 7),
        (r"\bfabrica de programadores\b", 8),

        (r"\bplataforma digital\b", 7),
        (r"\baplicativo\b", 6),
        (r"\bgovernanca digital\b", 8),
        (r"\bcomputacao\b", 6),
        (r"\bcloud\b", 6),
        (r"\bcomputacao em nuvem\b", 8),
        (r"\b5g\b", 8),
        (r"\bblockchain\b", 8)
    ]
}


# =========================================================
# THRESHOLDS POR CLASSE
# =========================================================

TEMA_THRESHOLDS = {

    "Saúde": 4,

    "Educação": 4,

    "Comunicação e Radiodifusão": 5,

    "Datas Comemorativas e Homenagens": 4,

    "Homenagens e Denominações": 5,

    "Meio Ambiente": 5,

    "Segurança Pública": 5,

    "Economia": 5,

    "Agricultura": 5,

    "Tecnologia": 5
}


# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================

TEMA_MIN_SCORE = 4

TEMA_MIN_MARGIN = 1

TEMA_FALLBACK = "Tema Não Explícito"