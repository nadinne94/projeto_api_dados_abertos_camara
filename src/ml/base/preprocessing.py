"""
Pré-processamento textual para classificação legislativa.

Centraliza funções de normalização, limpeza e padronização de textos
usados nas etapas de feature engineering, treinamento e inferência dos
modelos de classificação.

Este módulo apoia tanto regras determinísticas quanto modelos
supervisionados aplicados às proposições legislativas.
"""

import re
import unicodedata

from pyspark.sql.column import Column
from pyspark.sql.functions import coalesce, lit, lower, regexp_replace, trim


def remove_accents(col_texto: Column) -> Column:
    """Remove acentos comuns de uma coluna textual Spark."""

    texto = regexp_replace(col_texto, "[áàâãä]", "a")
    texto = regexp_replace(texto, "[éèêë]", "e")
    texto = regexp_replace(texto, "[íìîï]", "i")
    texto = regexp_replace(texto, "[óòôõö]", "o")
    texto = regexp_replace(texto, "[úùûü]", "u")
    texto = regexp_replace(texto, "[ç]", "c")

    return texto


def clean_spaces(col_texto: Column) -> Column:
    """Normaliza espaços consecutivos em uma coluna textual Spark."""

    return trim(regexp_replace(col_texto, r"\s+", " "))


def _normalize_python_text(text: str | None) -> str:
    """Normaliza uma string Python para uso em testes e treinamento local."""

    if text is None:
        return ""

    normalized = str(text).lower().strip()
    normalized = unicodedata.normalize("NFKD", normalized)
    normalized = "".join(
        char
        for char in normalized
        if not unicodedata.combining(char)
    )
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def _normalize_spark_column(col_texto: Column) -> Column:
    """Normaliza uma coluna Spark preservando a execução distribuída."""

    texto = lower(trim(coalesce(col_texto, lit(""))))
    texto = remove_accents(texto)
    texto = regexp_replace(texto, r"[^a-z0-9\s]", " ")

    return clean_spaces(texto)


def normalize_text(text: str | Column | None) -> str | Column:
    """
    Normaliza texto para uso em classificação NLP.

    Quando recebe uma string Python, retorna uma string normalizada.
    Quando recebe uma coluna Spark, retorna uma expressão Column equivalente.
    """

    if isinstance(text, Column):
        return _normalize_spark_column(text)

    return _normalize_python_text(text)
