"""
Configuração da sessão Spark.

Centraliza os parâmetros usados para criação e configuração da SparkSession,
incluindo nome da aplicação, partições de shuffle, timezone e opções
relacionadas ao Delta Lake.

As configurações podem ser carregadas a partir de variáveis de ambiente.
"""

SPARK_CONFIG = {

    # Delta

    "spark.databricks.delta.schema.autoMerge.enabled":
        "true",

    # AQE

    "spark.sql.adaptive.enabled":
        "true",

    # Bronze workloads (API)

    "spark.sql.shuffle.partitions":
        "50"
}