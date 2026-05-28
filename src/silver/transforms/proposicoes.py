# Importação de Dependências Spark SQL
from pyspark.sql.functions import col, upper, to_date, current_timestamp

# Processamento de dataset
def transform_proposicoes(df):
    return (
        df.select(
            col("id").cast("string").alias("id_proposicao"),
            upper(col("siglaTipo")).alias("sigla_tipo"),
            col("numero").cast("int"),
            col("ano").cast("int"),
            col("ementa"),
            to_date(col("dataApresentacao")).alias("data_apresentacao"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_proposicao"])
    )