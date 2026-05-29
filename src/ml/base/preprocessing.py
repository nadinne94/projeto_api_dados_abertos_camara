import re
import unicodedata

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

def normalizar_texto(text: str) -> str:
    """
    Normaliza texto para uso em classificação NLP.

    Args:
        text: Texto original.

    Returns:
        Texto normalizado, sem acentos, em minúsculas e sem pontuação.
    """

    if text is None:
        return ""

    text = str(text).lower().strip()

    text = unicodedata.normalize(
        "NFKD",
        text
    )

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text