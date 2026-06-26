"""
Publicação das tabelas finais para consumo analítico.

Centraliza a criação de schema, validação de tabelas Delta e publicação
do modelo Star Schema em uma camada SQL para consumo pelo Power BI.
"""

from pyspark.sql import SparkSession

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.utils.storage.delta_io import (
    get_path
)


DEFAULT_SCHEMA = "api_dados_abertos.star_schema"

try:
    from pyspark.dbutils import DBUtils
except ImportError:
    DBUtils = None


def list_star_tables(
    spark: SparkSession
):
    if DBUtils is None:
        raise RuntimeError(
            "DBUtils não está disponível. A publicação automática das tabelas requer execução no Databricks."
        )

    dbutils = DBUtils(spark)

    files = dbutils.fs.ls(
        STORAGE_CONFIG["star"]
    )

    return [
        file.name.rstrip("/")
        for file in files
        if file.isDir()
    ]


def create_schema(
    spark: SparkSession,
    schema: str = DEFAULT_SCHEMA,
    reset: bool = False
):

    if reset:

        spark.sql(
            f"DROP SCHEMA IF EXISTS {schema} CASCADE"
        )

    spark.sql(
        f"CREATE SCHEMA IF NOT EXISTS {schema}"
    )


def publish_table(
    spark: SparkSession,
    table_name: str,
    schema: str = DEFAULT_SCHEMA
):

    path = get_path(
        STORAGE_CONFIG,
        "star",
        table_name
    )

    print(
        f"[PUBLISH] star.{table_name} -> {schema}.{table_name}",
        flush=True
    )

    df = (
        spark.read
        .format("delta")
        .load(path)
    )

    (
        df.write
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(
            f"{schema}.{table_name}"
        )
    )


def publish_star_schema(
    spark: SparkSession = None,
    schema: str = DEFAULT_SCHEMA,
    reset_schema: bool = False
):

    spark = spark or SparkSession.builder.getOrCreate()

    print(
        f"[SERVING] Publicando camada star no schema SQL: {schema}",
        flush=True
    )

    create_schema(
        spark=spark,
        schema=schema,
        reset=reset_schema
    )

    tables = list_star_tables(
        spark
    )

    for table in tables:

        publish_table(
            spark=spark,
            table_name=table,
            schema=schema
        )

    print(
        "[SERVING] Publicação concluída.",
        flush=True
    )


def validate_published_tables(
    spark: SparkSession = None,
    schema: str = DEFAULT_SCHEMA
):

    spark = spark or SparkSession.builder.getOrCreate()

    tables = [
        row.tableName
        for row in spark.sql(
            f"SHOW TABLES IN {schema}"
        ).collect()
    ]

    for table in tables:

        print(
            f"\n[VALIDATE] {schema}.{table}",
            flush=True
        )

        df = spark.read.table(
            f"{schema}.{table}"
        )

        print(
            f"Registros: {df.count()}",
            flush=True
        )

        df.printSchema()


def validate_star_delta_tables(
    spark: SparkSession = None,
    table_name: str = "fato_tramitacao"
):

    spark = spark or SparkSession.builder.getOrCreate()

    path = get_path(
        STORAGE_CONFIG,
        "star",
        table_name
    )

    df = (
        spark.read
        .format("delta")
        .load(path)
    )

    print(
        f"[DELTA] star.{table_name}",
        flush=True
    )

    print(
        f"Registros: {df.count()}",
        flush=True
    )

    df.printSchema()

    return df

if __name__ == "__main__":
    publish_star_schema()
    validate_published_tables()
    validate_star_delta_tables()