from pyspark.sql.functions import col, to_date, to_timestamp, upper, trim, year, month, current_timestamp

def transform_votacoes(df):
    data_votacao = to_date(col("data"))

    return (
        df.select(
            col("id").cast("string").alias("id_votacao"),
            col("parent_id").cast("string").alias("id_proposicao"),
            data_votacao.alias("data_votacao"),
            to_timestamp(col("dataHoraRegistro")).alias("data_registro"),
            col("descricao").alias("descricao_votacao"),
            col("aprovacao").cast("boolean"),
            upper(trim(col("siglaOrgao"))).alias("orgao"),
            year(data_votacao).alias("ano_votacao"),
            month(data_votacao).alias("mes_votacao"),
            current_timestamp().alias("data_processamento")
        )
        .dropDuplicates(["id_votacao"])
    )