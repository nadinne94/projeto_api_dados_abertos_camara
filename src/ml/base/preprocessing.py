from pyspark.sql.column import Column

from pyspark.sql.functions import (

    lower,
    trim,
    regexp_replace,
    coalesce,
    lit
)


def remover_acentos(
    col_texto: Column
):

    texto = regexp_replace(

        col_texto,

        "[áàâãä]",

        "a"
    )

    texto = regexp_replace(
        texto,
        "[éèêë]",
        "e"
    )

    texto = regexp_replace(
        texto,
        "[íìîï]",
        "i"
    )

    texto = regexp_replace(
        texto,
        "[óòôõö]",
        "o"
    )

    texto = regexp_replace(
        texto,
        "[úùûü]",
        "u"
    )

    texto = regexp_replace(
        texto,
        "[ç]",
        "c"
    )

    return texto


def limpar_espacos(
    col_texto: Column
):

    return trim(

        regexp_replace(

            col_texto,

            r"\s+",

            " "
        )
    )


def normalizar_texto(
    col_texto: Column
):

    texto = lower(
        coalesce(
            col_texto.cast("string"),
            lit("")
        )
    )

    texto = remover_acentos(
        texto
    )

    texto = regexp_replace(

        texto,

        r"[^a-z0-9\s]",

        " "
    )

    return limpar_espacos(
        texto
    )