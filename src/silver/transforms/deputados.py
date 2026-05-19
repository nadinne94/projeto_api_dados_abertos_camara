from pyspark.sql.functions import col, trim, upper, lower, current_timestamp

def transform_deputados(df):

    return (
        df.select(
            col("id").cast("string").alias("id_deputado"),
            trim(col("nome")).alias("nome_deputado"),
            upper(trim(col("siglaPartido"))).alias("sigla_partido"),
            upper(trim(col("siglaUf"))).alias("uf_origem"),
            lower(trim(col("email"))).alias("email"),
            col("urlFoto").alias("url_foto"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_deputado"])
    )