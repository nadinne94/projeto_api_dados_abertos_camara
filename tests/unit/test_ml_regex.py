"""
Testes unitários das funções auxiliares de regex.

Valida operações de matching, contagem, extração e pontuação baseadas em
expressões regulares usadas na classificação textual de proposições
legislativas.
"""

from pyspark.sql.functions import col

from src.ml.base.regex import (
    regex_count,
    regex_extract_length,
    regex_match,
    score_regex,
)


def test_regex_match_returns_true_when_pattern_matches(spark):
    df = spark.createDataFrame(
        [
            ("Projeto sobre saúde pública",),
            ("Projeto sobre educação",),
        ],
        ["texto"],
    )

    result = (
        df.withColumn(
            "has_match",
            regex_match(
                col("texto"),
                r"saúde",
            ),
        )
        .orderBy("texto")
        .collect()
    )

    rows = {
        row["texto"]: row["has_match"]
        for row in result
    }

    assert rows["Projeto sobre saúde pública"] is True
    assert rows["Projeto sobre educação"] is False


def test_regex_count_counts_pattern_occurrences(spark):
    df = spark.createDataFrame(
        [
            ("sus sus saúde",),
        ],
        ["texto"],
    )

    result = (
        df.withColumn(
            "total_matches",
            regex_count(
                col("texto"),
                r"sus",
            ),
        )
        .collect()[0]["total_matches"]
    )

    assert result == 2


def test_regex_extract_length_returns_match_length(spark):
    df = spark.createDataFrame(
        [
            ("sistema unico de saude",),
        ],
        ["texto"],
    )

    result = (
        df.withColumn(
            "match_length",
            regex_extract_length(
                col("texto"),
                r"saude",
            ),
        )
        .collect()[0]["match_length"]
    )

    assert result == 5


def test_score_regex_returns_weight_when_pattern_matches(spark):
    df = spark.createDataFrame(
        [
            ("sistema unico de saude",),
            ("tema nao relacionado",),
        ],
        ["texto"],
    )

    result = (
        df.withColumn(
            "score",
            score_regex(
                col("texto"),
                r"saude",
                10,
            ),
        )
        .orderBy("texto")
        .collect()
    )

    scores = [
        row["score"]
        for row in result
    ]

    assert scores == [10, 0]