import pytest

from src.utils.helpers.data_quality import (
    assert_no_nulls,
    assert_not_empty,
    assert_required_columns,
    assert_unique_key
)


def test_assert_not_empty_passes_for_non_empty_dataframe(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
        ],
        ["id", "sigla"]
    )

    assert_not_empty(
        df,
        dataset_name="partidos"
    )


def test_assert_not_empty_raises_for_empty_dataframe(spark):
    df = spark.createDataFrame(
        [],
        "id INT, sigla STRING"
    )

    with pytest.raises(ValueError):
        assert_not_empty(
            df,
            dataset_name="partidos"
        )


def test_assert_required_columns_passes_when_columns_exist(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
        ],
        ["id", "sigla"]
    )

    assert_required_columns(
        df,
        required_columns=["id", "sigla"],
        dataset_name="partidos"
    )


def test_assert_required_columns_raises_when_column_is_missing(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
        ],
        ["id", "sigla"]
    )

    with pytest.raises(ValueError):
        assert_required_columns(
            df,
            required_columns=["id", "nome"],
            dataset_name="partidos"
        )


def test_assert_no_nulls_passes_when_columns_have_no_nulls(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "PT"),
        ],
        ["id", "sigla"]
    )

    assert_no_nulls(
        df,
        columns=["id", "sigla"],
        dataset_name="partidos"
    )


def test_assert_no_nulls_raises_when_column_has_null(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, None),
        ],
        ["id", "sigla"]
    )

    with pytest.raises(ValueError):
        assert_no_nulls(
            df,
            columns=["sigla"],
            dataset_name="partidos"
        )


def test_assert_unique_key_passes_when_key_is_unique(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "PT"),
        ],
        ["id", "sigla"]
    )

    assert_unique_key(
        df,
        key_columns=["id"],
        dataset_name="partidos"
    )


def test_assert_unique_key_raises_when_key_is_duplicated(spark):
    df = spark.createDataFrame(
        [
            (1, "PL"),
            (1, "PL"),
        ],
        ["id", "sigla"]
    )

    with pytest.raises(ValueError):
        assert_unique_key(
            df,
            key_columns=["id"],
            dataset_name="partidos"
        )