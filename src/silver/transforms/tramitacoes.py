from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col,
    upper,
    to_timestamp,
    to_date,
    current_timestamp,
    row_number
)

def transform_tramitacoes(df):

    df_sel = (
        df.select(
            col("parent_id").cast("string").alias("id_proposicao"),
            col("sequencia").cast("int").alias("sequencia"),
            to_timestamp(col("dataHora")).alias("data_hora_tramitacao"),
            to_date(col("dataHora")).alias("data_tramitacao"),
            upper(col("siglaOrgao")).alias("orgao"),
            col("descricaoTramitacao").alias("descricao_tramitacao"),
            col("descricaoSituacao").alias("descricao_situacao"),
            col("codSituacao").cast("int").alias("cod_situacao"),
            col("despacho"),
            current_timestamp().alias("data_processamento")
        )
    )

    w = (
        Window
        .partitionBy("id_proposicao")
        .orderBy(col("sequencia").desc())
    )

    return (
        df_sel
        .withColumn(
            "rn_tramitacao_recente",
            row_number().over(w)
        )
        .dropDuplicates(
            ["id_proposicao","sequencia"]
        )
    )