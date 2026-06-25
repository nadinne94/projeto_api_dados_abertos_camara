"""
Funções de classificação de eventos.

Centraliza regras usadas para classificar tipo e status de eventos
legislativos.
"""

from pyspark.sql.functions import lower, when, coalesce, lit

def classify_event_type(col_tipo):
    t = lower(coalesce(col_tipo, lit("")))

    return (
        when(t.rlike("sessão|sessao"), "Sessão")
        .when(t.rlike("comissão|comissao"), "Comissão")
        .when(t.rlike("audiência|audiencia"), "Audiência Pública")
        .when(t.rlike("reunião|reuniao"), "Reunião")
        .otherwise("Outros")
    )
def classify_event_status(col_situacao):
    s = lower(coalesce(col_situacao, lit("")))

    return (
        when(s.rlike("realizad|encerrad"), "Realizado")
        .when(s.rlike("cancelad"), "Cancelado")
        .when(s.rlike("adiad"), "Adiado")
        .when(s.rlike("andamento"), "Em Andamento")
        .otherwise("Indefinido")
    )