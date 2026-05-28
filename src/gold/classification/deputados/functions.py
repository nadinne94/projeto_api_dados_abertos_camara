from pyspark.sql.functions import when

def classificar_regiao(col_uf):
    return (
        when(col_uf.isin("AC","AP","AM","PA","RO","RR","TO"), "Norte")
        .when(col_uf.isin("AL","BA","CE","MA","PB","PE","PI","RN","SE"), "Nordeste")
        .when(col_uf.isin("DF","GO","MT","MS"), "Centro-Oeste")
        .when(col_uf.isin("ES","MG","RJ","SP"), "Sudeste")
        .when(col_uf.isin("PR","RS","SC"), "Sul")
        .otherwise("Indefinida")
    )

def classificar_estado(col_uf):

    return (

        when(col_uf == "AC", "Acre")
        .when(col_uf == "AL", "Alagoas")
        .when(col_uf == "AP", "Amapa")
        .when(col_uf == "AM", "Amazonas")
        .when(col_uf == "BA", "Bahia")
        .when(col_uf == "CE", "Ceara")
        .when(col_uf == "DF", "Distrito Federal")
        .when(col_uf == "ES", "Espirito Santo")
        .when(col_uf == "GO", "Goias")
        .when(col_uf == "MA", "Maranhao")
        .when(col_uf == "MT", "Mato Grosso")
        .when(col_uf == "MS", "Mato Grosso do Sul")
        .when(col_uf == "MG", "Minas Gerais")
        .when(col_uf == "PA", "Para")
        .when(col_uf == "PB", "Paraiba")
        .when(col_uf == "PR", "Parana")
        .when(col_uf == "PE", "Pernambuco")
        .when(col_uf == "PI", "Piaui")
        .when(col_uf == "RJ", "Rio de Janeiro")
        .when(col_uf == "RN", "Rio Grande do Norte")
        .when(col_uf == "RS", "Rio Grande do Sul")
        .when(col_uf == "RO", "Rondonia")
        .when(col_uf == "RR", "Roraima")
        .when(col_uf == "SC", "Santa Catarina")
        .when(col_uf == "SP", "Sao Paulo")
        .when(col_uf == "SE", "Sergipe")
        .when(col_uf == "TO", "Tocantins")

        .otherwise("Indefinido")
    )