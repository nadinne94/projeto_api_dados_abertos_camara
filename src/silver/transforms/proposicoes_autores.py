# Importação de Dependências Spark SQL
from pyspark.sql.functions import col, upper, current_timestamp

# Processamento de dataset
def transform_autores(df):
    return (
        df.select(
            col("parent_id").cast("string").alias("id_proposicao"),
            col("nome").alias("nome_autor"),
            upper(col("tipo")).alias("tipo_autor"),
            col("ordemAssinatura").cast("int").alias("ordem_assinatura"),
            col("proponente").cast("boolean").alias("proponente"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_proposicao", "nome_autor","ordem_assinatura"])
    )