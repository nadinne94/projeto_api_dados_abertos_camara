from pyspark.sql.functions import col, upper, to_date, to_timestamp, current_timestamp

def transform_votos(df):
    data_hora_voto = to_timestamp(col("dataRegistroVoto"))

    return (
        df.select(
            col("parent_id").cast("string").alias("id_votacao"),
            col("deputado_")["id"].cast("string").alias("id_deputado"),
            col("deputado_nome").alias("nome_deputado"),
            upper(col("tipoVoto")).alias("voto"),
            to_date(data_hora_voto).alias("data_voto"),
            data_hora_voto.alias("data_hora_voto"),
            current_timestamp().alias("data_processamento")
        )
        .dropna(subset=["id_votacao","id_deputado"])
        .dropDuplicates(["id_votacao", "id_deputado"])
    )