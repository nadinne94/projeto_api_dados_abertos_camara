from pyspark.sql.functions import lower, when, coalesce, lit

def classificar_tipo_evento(col_tipo):
    t = lower(coalesce(col_tipo, lit("")))

    return (
        when(t.rlike("sessão|sessao"), "Sessão")
        .when(t.rlike("comissão|comissao"), "Comissão")
        .when(t.rlike("audiência|audiencia"), "Audiência Pública")
        .when(t.rlike("reunião|reuniao"), "Reunião")
        .otherwise("Outros")
    )
def classificar_status_evento(col_situacao):
    s = lower(coalesce(col_situacao, lit("")))

    return (
        when(s.rlike("realizad|encerrad"), "Realizado")
        .when(s.rlike("cancelad"), "Cancelado")
        .when(s.rlike("adiad"), "Adiado")
        .when(s.rlike("andamento"), "Em Andamento")
        .otherwise("Indefinido")
    )