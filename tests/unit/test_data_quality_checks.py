"""
Testes unitários dos checks de Data Quality.

Valida o comportamento das funções reutilizáveis de qualidade de dados,
incluindo verificação de datasets vazios, colunas obrigatórias, valores
nulos, unicidade, percentual máximo de nulos, domínios permitidos e volume
mínimo de registros.
"""


import pytest

from src.utils.quality.checks import (
    check_allowed_values,
    check_max_null_ratio,
    check_min_rows,
    check_no_nulls,
    check_not_empty,
    check_required_columns,
    check_unique_key,
)


def test_check_not_empty_passes_for_non_empty_dataframe(spark):
    df = spark.createDataFrame(
        [
            (1, "PL")
        ],
        ["id", "sigla"]
    )

    result = check_not_empty(df)

    assert result["status"] == "passed"


def test_check_not_empty_fails_for_empty_dataframe(spark):
    df = spark.createDataFrame(
        [],
        "id INT, sigla STRING"
    )

    result = check_not_empty(df)

    assert result["status"] == "failed"
    assert result["rule_name"] == "not_empty"


def test_check_required_columns_passes_when_columns_exist(spark):
    df = spark.createDataFrame(
        [
            (1, "PL")
        ],
        ["id", "sigla"]
    )

    result = check_required_columns(
        df=df,
        required_columns=["id", "sigla"]
    )

    assert result["status"] == "passed"


def test_check_required_columns_fails_when_column_is_missing(spark):
    df = spark.createDataFrame(
        [
            (1, "PL")
        ],
        ["id", "sigla"]
    )

    result = check_required_columns(
        df=df,
        required_columns=["id", "nome"]
    )

    assert result["status"] == "failed"
    assert "nome" in result["message"]


def test_check_no_nulls_passes_when_no_null_values(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "PT")
        ],
        ["id", "sigla"]
    )

    result = check_no_nulls(
        df=df,
        columns=["id", "sigla"]
    )

    assert result["status"] == "passed"


def test_check_no_nulls_fails_when_column_has_null(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, None)
        ],
        ["id", "sigla"]
    )

    result = check_no_nulls(
        df=df,
        columns=["sigla"]
    )

    assert result["status"] == "failed"


def test_check_no_nulls_fails_when_column_does_not_exist(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
        ],
        ["id", "sigla"],
    )

    result = check_no_nulls(
        df=df,
        columns=["nome"],
    )

    assert result["status"] == "failed"
    assert "nome" in result["message"]


def test_check_unique_key_passes_when_key_is_unique(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "PT")
        ],
        ["id", "sigla"]
    )

    result = check_unique_key(
        df=df,
        key_columns=["id"]
    )

    assert result["status"] == "passed"


def test_check_unique_key_fails_when_key_is_duplicated(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (1, "PL")
        ],
        ["id", "sigla"]
    )

    result = check_unique_key(
        df=df,
        key_columns=["id"]
    )

    assert result["status"] == "failed"


def test_check_unique_key_fails_when_key_column_does_not_exist(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
        ],
        ["id", "sigla"],
    )

    result = check_unique_key(
        df=df,
        key_columns=["id_inexistente"],
    )

    assert result["status"] == "failed"
    assert "id_inexistente" in result["message"]


def test_check_max_null_ratio_passes_when_ratio_is_below_limit(spark):
    df = spark.createDataFrame(
        [
            (1, "A"),
            (2, "B"),
            (3, None),
        ],
        ["id", "valor"]
    )

    result = check_max_null_ratio(
        df=df,
        column_name="valor",
        max_ratio=0.50
    )

    assert result["status"] == "passed"


def test_check_max_null_ratio_fails_when_ratio_is_above_limit(spark):
    df = spark.createDataFrame(
        [
            (1, None),
            (2, None),
            (3, "A"),
        ],
        ["id", "valor"]
    )

    result = check_max_null_ratio(
        df=df,
        column_name="valor",
        max_ratio=0.30
    )

    assert result["status"] == "failed"


def test_check_allowed_values_passes_for_valid_domain(spark):
    df = spark.createDataFrame(
        [
            ("Sim",),
            ("Não",),
            ("Abstenção",),
        ],
        ["voto"]
    )

    result = check_allowed_values(
        df=df,
        column_name="voto",
        allowed_values=[
            "Sim",
            "Não",
            "Abstenção"
        ]
    )

    assert result["status"] == "passed"


def test_check_allowed_values_fails_for_invalid_domain(spark):
    df = spark.createDataFrame(
        [
            ("Sim",),
            ("Valor inválido",),
        ],
        ["voto"]
    )

    result = check_allowed_values(
        df=df,
        column_name="voto",
        allowed_values=[
            "Sim",
            "Não",
            "Abstenção"
        ]
    )

    assert result["status"] == "failed"


def test_check_min_rows_passes_when_row_count_is_enough(spark):
    df = spark.createDataFrame(
        [
            (1,),
            (2,),
            (3,),
        ],
        ["id"],
    )

    result = check_min_rows(
        df=df,
        min_rows=2,
    )

    assert result["status"] == "passed"


def test_check_min_rows_fails_when_row_count_is_below_minimum(spark):
    df = spark.createDataFrame(
        [
            (1,),
        ],
        ["id"],
    )

    result = check_min_rows(
        df=df,
        min_rows=2,
    )

    assert result["status"] == "failed"