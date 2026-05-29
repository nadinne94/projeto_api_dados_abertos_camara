# Data Quality

Este projeto possui uma camada formal de Data Quality para validar os dados produzidos nas camadas Bronze, Silver, Gold e Star.

## Objetivo

Garantir que as tabelas do pipeline atendam a critérios mínimos de qualidade antes de serem persistidas ou consumidas analiticamente.

## Tipos de Validação

As principais validações são:

| Validação | Descrição |
|---|---|
| `not_empty` | Verifica se a tabela possui registros |
| `required_columns` | Verifica se as colunas obrigatórias existem |
| `no_nulls` | Verifica se colunas críticas não possuem nulos |
| `unique_key` | Verifica se uma chave é única |
| `max_null_ratio` | Verifica percentual máximo de nulos |
| `allowed_values` | Verifica se valores pertencem a um domínio permitido |
| `min_rows` | Verifica volume mínimo de registros |
| `value_range` | Verifica intervalo permitido para valores numéricos |

## Severidade

As regras podem ter duas severidades:

| Severidade | Comportamento |
|---|---|
| `error` | Falha bloqueante. O pipeline deve parar. |
| `warning` | Falha não bloqueante. O pipeline registra o alerta e continua. |

## Contratos de Qualidade

Os contratos ficam definidos em:

```text
src/utils/quality/contracts.py
```
Cada contrato é associado a uma camada e tabela.

Exemplo:

```python
"silver": {
    "proposicoes": {
        "not_empty": {"severity": "error"},
        "required_columns": {
            "columns": ["id_proposicao", "sigla_tipo", "ano", "ementa"],
            "severity": "error"
        },
        "no_nulls": {
            "columns": ["id_proposicao"],
            "severity": "error"
        },
        "unique_key": {
            "columns": ["id_proposicao"],
            "severity": "error"
        }
    }
}

```
## Relatório de Qualidade

Os resultados das validações podem ser persistidos em uma tabela Delta de monitoramento.

Campos sugeridos:

| Campo	| Descrição |
| - | - |
|execution_id |	Identificador da execução|
|layer	| Camada validada|
|table_name | Tabela validada|
|rule_name |	Nome da regra|
|status |	Resultado da regra|
|severity	| Severidade da regra |
|message|	Mensagem explicativa|
|metric_value|	Valor observado|
|expected_value |	Valor esperado|
|checked_at	|Timestamp da validação|

## Benefícios

A camada de Data Quality aumenta a confiabilidade do pipeline ao garantir:

* tabelas não vazias;
* presença de colunas obrigatórias;
* chaves não nulas;
* unicidade de dimensões;
* controle de domínios;
* monitoramento de anomalias;
* rastreabilidade de falhas.
