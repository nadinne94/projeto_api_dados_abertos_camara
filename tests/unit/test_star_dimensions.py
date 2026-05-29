from src.star.dimensions.dim_deputado import build_dim_deputado
from src.star.dimensions.dim_partido import build_dim_partido


def test_build_dim_deputado_removes_duplicates_and_creates_surrogate_key(spark):
    df = spark.createDataFrame(
        [
            (
                1,
                "Deputada A",
                "PT",
                "MG",
                "Sudeste",
                "a@camara.leg.br",
                "foto_a"
            ),
            (
                1,
                "Deputada A",
                "PT",
                "MG",
                "Sudeste",
                "a@camara.leg.br",
                "foto_a"
            ),
            (
                2,
                "Deputado B",
                "PL",
                "SP",
                "Sudeste",
                "b@camara.leg.br",
                "foto_b"
            ),
        ],
        [
            "id_deputado",
            "nome_deputado",
            "sigla_partido",
            "uf_origem",
            "regiao",
            "email",
            "url_foto"
        ]
    )

    result = build_dim_deputado(df)

    assert result.count() == 2
    assert "sk_deputado" in result.columns


def test_build_dim_deputado_surrogate_key_is_stable(spark):
    df = spark.createDataFrame(
        [
            (
                1,
                "Deputada A",
                "PT",
                "MG",
                "Sudeste",
                "a@camara.leg.br",
                "foto_a"
            ),
        ],
        [
            "id_deputado",
            "nome_deputado",
            "sigla_partido",
            "uf_origem",
            "regiao",
            "email",
            "url_foto"
        ]
    )

    result_1 = build_dim_deputado(df).collect()[0]["sk_deputado"]
    result_2 = build_dim_deputado(df).collect()[0]["sk_deputado"]

    assert result_1 == result_2


def test_build_dim_partido_removes_duplicates_and_creates_surrogate_key(spark):
    df = spark.createDataFrame(
        [
            (
                10,
                "PT",
                "Partido dos Trabalhadores",
                "Esquerda",
                "Social-democracia",
                "Esquerda"
            ),
            (
                10,
                "PT",
                "Partido dos Trabalhadores",
                "Esquerda",
                "Social-democracia",
                "Esquerda"
            ),
            (
                20,
                "PL",
                "Partido Liberal",
                "Direita",
                "Liberal-conservador",
                "Direita"
            ),
        ],
        [
            "id_partido",
            "sigla_partido",
            "nome_partido",
            "espectro_politico",
            "corrente_ideologica",
            "bloco_ideologico"
        ]
    )

    result = build_dim_partido(df)

    assert result.count() == 2
    assert "sk_partido" in result.columns