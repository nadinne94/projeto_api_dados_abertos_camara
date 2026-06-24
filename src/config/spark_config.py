"""
Configuração da sessão Spark.

Centraliza os parâmetros usados para criação e configuração da SparkSession,
incluindo nome da aplicação, partições de shuffle, timezone e opções
relacionadas ao Delta Lake.

As configurações podem ser carregadas a partir de variáveis de ambiente.
"""

import os

from dotenv import load_dotenv


load_dotenv()


SPARK_CONFIG = {
    # DELTA
    "spark.databricks.delta.schema.autoMerge.enabled": os.getenv(
        "DELTA_SCHEMA_MERGE_ENABLED",
        "true",
    ),

    # AQE
    "spark.sql.adaptive.enabled": os.getenv(
        "SPARK_SQL_ADAPTIVE_ENABLED",
        "true",
    ),

    # SHUFFLE
    "spark.sql.shuffle.partitions": os.getenv(
        "SPARK_SQL_SHUFFLE_PARTITIONS",
        "50",
    ),

    # TIMEZONE
    "spark.sql.session.timeZone": os.getenv(
        "SPARK_SQL_SESSION_TIMEZONE",
        "America/Sao_Paulo",
    )
}