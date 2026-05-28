# Importação de Dependências Spark SQL
from pyspark.sql.functions import col, upper, current_timestamp

# Processamento de dataset
def transform_presencas(df):
    return (
        df.select(
            col("parent_id").cast("string").alias("id_evento"),
            col("id").cast("string").alias("id_deputado"),
            col("nome").alias("nome_deputado"),
            upper(col("siglaPartido")).alias("sigla_partido"),
            upper(col("siglaUf")).alias("uf_origem"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_evento", "id_deputado"])
    )