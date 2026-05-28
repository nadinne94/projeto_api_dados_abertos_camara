"""
Transformação Gold — Proposições.

Versão performática para camada gold:
- bloqueia textos genéricos
- classifica tema por ML
- classifica natureza jurídica por ML
- classifica tipo documental por regra simples
- aplica taxonomia regimental
"""

from pyspark.sql.functions import (
    col,
    trim,
    upper,
    when,
    lit,
    current_timestamp,
    length
)

from src.gold.classification.proposicoes.functions import (
    classificar_tipo_documental
)

from src.gold.classification.proposicoes.taxonomy import (
    aplicar_taxonomia_regimental
)

from src.ml.inference.udf_loader import (
    criar_udf_classificacao
)


TEMA_FALLBACK = "Tema Não Explícito"

NATUREZA_FALLBACK = "Outros Tipos"

MIN_LEN_ML = 40


REGEX_TEXTOS_GENERICOS = r"""(?i)(
^ata\s+n[ºo]?\s*\d+
|
^termo\s+de\s+solene
|
^parecer\s+d[ao]\s+relator.*
|
^parecer\s+d[ao]\s+relatora.*
|
^parecer\s+pela\s+aprova[cç][aã]o.*
|
^requer\s+a\s+inclus[aã]o.*
|
^requerimento\s+de\s+invers[aã]o.*
|
^requerimento\s+de\s+retirada.*
|
^requerimento\s+de\s+adiamento.*
|
^requerimento\s+de\s+vota[cç][aã]o.*
|
^voto:.*
)$"""


def transform_proposicoes(df):

    tema_ml = criar_udf_classificacao(
        model_name="api_dados_abertos.ml.tema_classificador",
        model_alias="champion",
        fallback=TEMA_FALLBACK
    )

    natureza_ml = criar_udf_classificacao(
        model_name="api_dados_abertos.ml.natureza_classificador",
        model_alias="champion",
        fallback=NATUREZA_FALLBACK
    )

    df = (
        df
        .withColumn(
            "ementa",
            trim(col("ementa"))
        )
        .withColumn(
            "sigla_tipo",
            upper(trim(col("sigla_tipo")))
        )
    )

    ementa_valida_ml = (
        col("ementa").isNotNull()
        & (length(trim(col("ementa"))) >= MIN_LEN_ML)
        & (~col("ementa").rlike(REGEX_TEXTOS_GENERICOS))
    )

    df = (
        df
        .withColumn(
            "tema_ementa",
            when(
                ementa_valida_ml,
                tema_ml(col("ementa"))
            ).otherwise(
                lit(TEMA_FALLBACK)
            )
        )
        .withColumn(
            "origem_tema",
            when(
                ementa_valida_ml,
                lit("ML")
            ).otherwise(
                lit("SEM_EVIDENCIA")
            )
        )
        .withColumn(
            "natureza_juridica",
            when(
                ementa_valida_ml,
                natureza_ml(col("ementa"))
            ).otherwise(
                lit(NATUREZA_FALLBACK)
            )
        )
        .withColumn(
            "origem_natureza_juridica",
            when(
                ementa_valida_ml,
                lit("ML")
            ).otherwise(
                lit("SEM_EVIDENCIA")
            )
        )
        .withColumn(
            "tipo_documental",
            classificar_tipo_documental(
                col("ementa"),
                col("sigla_tipo")
            )
        )
    )

    df = aplicar_taxonomia_regimental(df)

    return (
        df
        .withColumn(
            "flag_tema_por_ml",
            col("origem_tema") == "ML"
        )
        .withColumn(
            "flag_natureza_por_ml",
            col("origem_natureza_juridica") == "ML"
        )
        .withColumn(
            "flag_classificacao_automatica",
            lit(1)
        )
        .withColumn(
            "data_gold",
            current_timestamp()
        )
    )