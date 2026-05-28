import pytest

from src.utils.helpers.surrogate import add_surrogate_key


def test_add_surrogate_key_creates_column(spark):
    df = spark.createDataFrame(
        [
            (1, "Deputada A"),
            (2, "Deputado B"),
        ],
        ["id_deputado", "nome_deputado"]
    )

    result = add_surrogate_key(
        df=df,
        key_name="sk_deputado",
        natural_keys=["id_deputado"]
    )

    assert "sk_deputado" in result.columns


def test_add_surrogate_key_is_deterministic(spark):
    df = spark.createDataFrame(
        [
            (1, "Deputada A"),
            (2, "Deputado B"),
        ],
        ["id_deputado", "nome_deputado"]
    )

    result_1 = (
        add_surrogate_key(
            df=df,
            key_name="sk_deputado",
            natural_keys=["id_deputado"]
        )
        .orderBy("id_deputado")
        .collect()
    )

    result_2 = (
        add_surrogate_key(
            df=df,
            key_name="sk_deputado",
            natural_keys=["id_deputado"]
        )
        .orderBy("id_deputado")
        .collect()
    )

    keys_1 = [
        row["sk_deputado"]
        for row in result_1
    ]

    keys_2 = [
        row["sk_deputado"]
        for row in result_2
    ]

    assert keys_1 == keys_2


def test_add_surrogate_key_generates_different_keys_for_different_natural_keys(spark):
    df = spark.createDataFrame(
        [
            (1, "Deputada A"),
            (2, "Deputado B"),
        ],
        ["id_deputado", "nome_deputado"]
    )

    result = (
        add_surrogate_key(
            df=df,
            key_name="sk_deputado",
            natural_keys=["id_deputado"]
        )
        .select("sk_deputado")
        .collect()
    )

    keys = [
        row["sk_deputado"]
        for row in result
    ]

    assert len(set(keys)) == 2


def test_add_surrogate_key_handles_null_values(spark):
    df = spark.createDataFrame(
        [
            (None, "Órgão sem ID"),
            ("ABC", "Órgão com ID"),
        ],
        ["id_orgao", "nome_orgao"]
    )

    result = add_surrogate_key(
        df=df,
        key_name="sk_orgao",
        natural_keys=["id_orgao"]
    )

    rows = result.collect()

    assert all(
        row["sk_orgao"] is not None
        for row in rows
    )


def test_add_surrogate_key_raises_error_when_natural_keys_are_empty(spark):
    df = spark.createDataFrame(
        [
            (1, "Deputada A"),
        ],
        ["id_deputado", "nome_deputado"]
    )

    with pytest.raises(ValueError):
        add_surrogate_key(
            df=df,
            key_name="sk_deputado",
            natural_keys=[]
        )


def test_add_surrogate_key_raises_error_when_column_does_not_exist(spark):
    df = spark.createDataFrame(
        [
            (1, "Deputada A"),
        ],
        ["id_deputado", "nome_deputado"]
    )

    with pytest.raises(ValueError):
        add_surrogate_key(
            df=df,
            key_name="sk_deputado",
            natural_keys=["coluna_inexistente"]
        )