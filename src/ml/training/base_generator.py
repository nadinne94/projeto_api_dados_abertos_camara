from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    col,
    trim
)

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.utils.storage.delta_io import (
    read_table,
    write_table
)


def gerar_base_treino(
    config
):

    spark = SparkSession.getActiveSession()

    if spark is None:

        raise RuntimeError(
            "Nenhuma SparkSession ativa encontrada."
        )

    source_table = config["source_table"]

    target_col = config["target_col"]

    regex_func = config["regex_func"]

    tabela_treino = config["tabela_treino"]

    df = read_table(

        spark=spark,

        storage_config=STORAGE_CONFIG,

        layer="silver",

        table_name=source_table
    )

    df = (

        df

        .filter(
            col("ementa").isNotNull()
        )

        .filter(
            trim(col("ementa")) != ""
        )

        .dropDuplicates(
            ["ementa"]
        )
    )

    df = df.withColumn(

        target_col,

        regex_func(
            col("ementa")
        )
    )

    df = (

        df

        .filter(
            col(target_col).isNotNull()
        )

        .filter(
            trim(col(target_col)) != ""
        )
    )

    write_table(

        spark=spark,

        df=df,

        storage_config=STORAGE_CONFIG,

        layer="ml_models",

        table_name=tabela_treino
    )

    return df