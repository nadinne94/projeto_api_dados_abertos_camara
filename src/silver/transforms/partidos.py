# Importação de Dependências Spark SQL
from pyspark.sql.functions import col, upper, current_timestamp

# Processamento de dataset
def transform_partidos(df):
    return (
        df.select(
            col("id").cast("string").alias("id_partido"),
            col("nome").alias("nome_partido"),
            upper(col("sigla")).alias("sigla_partido"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_partido"])
    )