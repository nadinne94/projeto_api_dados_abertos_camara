from pyspark.sql import SparkSession

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.utils.storage.delta_io import (
    get_path
)


DEFAULT_SCHEMA = "dados_abertos.star_schema"


def listar_tabelas_star(
    spark: SparkSession
):

    files = dbutils.fs.ls(
        STORAGE_CONFIG["star"]
    )

    return [
        file.name.rstrip("/")
        for file in files
        if file.isDir()
    ]


def criar_schema(
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


def publicar_tabela(
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


def publicar_star_schema(
    spark: SparkSession = None,
    schema: str = DEFAULT_SCHEMA,
    reset_schema: bool = False
):

    spark = spark or SparkSession.builder.getOrCreate()

    print(
        f"[SERVING] Publicando camada star no schema SQL: {schema}",
        flush=True
    )

    criar_schema(
        spark=spark,
        schema=schema,
        reset=reset_schema
    )

    tables = listar_tabelas_star(
        spark
    )

    for table in tables:

        publicar_tabela(
            spark=spark,
            table_name=table,
            schema=schema
        )

    print(
        "[SERVING] Publicação concluída.",
        flush=True
    )


def validar_tabelas_publicadas(
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


def validar_delta_star(
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