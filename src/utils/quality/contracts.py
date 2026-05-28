"""
Contratos declarativos de Data Quality.

Cada contrato define as regras mínimas esperadas para uma tabela em uma
determinada camada do pipeline.

As regras possuem severidade:

- error: falha bloqueante;
- warning: falha não bloqueante, apenas registrada.
"""

DATA_QUALITY_CONTRACTS = {
    "bronze": {
        "deputados": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id",
                    "nome",
                    "siglaPartido",
                    "siglaUf"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id"
                ],
                "severity": "warning"
            }
        },

        "partidos": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id",
                    "sigla",
                    "nome"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id"
                ],
                "severity": "error"
            }
        },

        "proposicoes": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id",
                    "siglaTipo",
                    "numero",
                    "ano",
                    "ementa"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id"
                ],
                "severity": "warning"
            }
        }
    },

    "silver": {
        "deputados": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id_deputado",
                    "nome_deputado",
                    "sigla_partido",
                    "uf_origem"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id_deputado"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id_deputado"
                ],
                "severity": "error"
            }
        },

        "partidos": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id_partido",
                    "sigla_partido",
                    "nome_partido"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id_partido"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id_partido"
                ],
                "severity": "error"
            }
        },

        "proposicoes": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id_proposicao",
                    "sigla_tipo",
                    "numero",
                    "ano",
                    "ementa"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id_proposicao"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id_proposicao"
                ],
                "severity": "error"
            },
            "max_null_ratio": {
                "column": "ementa",
                "max_ratio": 0.30,
                "severity": "warning"
            }
        },

        "votacoes": {
            "not_empty": {
                "severity": "warning"
            },
            "required_columns": {
                "columns": [
                    "id_votacao",
                    "id_proposicao"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id_votacao"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id_votacao"
                ],
                "severity": "warning"
            }
        }
    },

    "gold": {
        "proposicoes": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "id_proposicao",
                    "sigla_tipo",
                    "tipo_documental",
                    "tema_ementa",
                    "natureza_juridica",
                    "macrotema"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "id_proposicao",
                    "tipo_documental"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "id_proposicao"
                ],
                "severity": "error"
            },
            "max_null_ratio": {
                "column": "tema_ementa",
                "max_ratio": 0.50,
                "severity": "warning"
            }
        },

        "votos": {
            "not_empty": {
                "severity": "warning"
            },
            "required_columns": {
                "columns": [
                    "id_votacao",
                    "id_deputado",
                    "voto"
                ],
                "severity": "error"
            },
            "allowed_values": {
                "column": "voto",
                "values": [
                    "Sim",
                    "Não",
                    "Abstenção",
                    "Obstrução",
                    "Art. 17",
                    "Não Votou",
                    "Liberado",
                    "Presidente"
                ],
                "severity": "warning"
            }
        }
    },

    "star": {
        "dim_deputado": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "sk_deputado",
                    "id_deputado",
                    "nome_deputado",
                    "sigla_partido"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "sk_deputado",
                    "id_deputado"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "sk_deputado"
                ],
                "severity": "error"
            }
        },

        "dim_partido": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "sk_partido",
                    "id_partido",
                    "sigla_partido",
                    "nome_partido"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "sk_partido",
                    "id_partido"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "sk_partido"
                ],
                "severity": "error"
            }
        },

        "dim_proposicao": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "sk_proposicao",
                    "id_proposicao",
                    "tipo_documental",
                    "tema_ementa",
                    "natureza_juridica"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "sk_proposicao",
                    "id_proposicao"
                ],
                "severity": "error"
            },
            "unique_key": {
                "columns": [
                    "sk_proposicao"
                ],
                "severity": "error"
            }
        },

        "fato_proposicao": {
            "not_empty": {
                "severity": "error"
            },
            "required_columns": {
                "columns": [
                    "sk_proposicao",
                    "sk_tempo_apresentacao"
                ],
                "severity": "error"
            },
            "no_nulls": {
                "columns": [
                    "sk_proposicao"
                ],
                "severity": "error"
            }
        },

        "fato_voto": {
            "not_empty": {
                "severity": "warning"
            },
            "required_columns": {
                "columns": [
                    "sk_deputado",
                    "sk_proposicao",
                    "voto"
                ],
                "severity": "error"
            }
        }
    }
}