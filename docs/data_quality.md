# Data Quality

## Objetivo

Este documento descreve a camada de Data Quality do projeto `projeto_api_dados_abertos_camara`.

O objetivo é garantir que as tabelas produzidas pelo pipeline atendam a critérios mínimos de qualidade antes de serem persistidas, promovidas entre camadas ou consumidas analiticamente no Power BI.

---

## Contexto

O projeto processa dados públicos da Câmara dos Deputados em uma arquitetura lakehouse com camadas Bronze, Silver, Gold, Star Schema e Serving.

Como os dados são extraídos de múltiplos endpoints e passam por várias transformações, é importante validar:

- existência de dados;
- presença de colunas obrigatórias;
- preenchimento de chaves críticas;
- unicidade de chaves;
- limites aceitáveis de nulos;
- valores dentro de domínios esperados;
- consistência entre fatos e dimensões.

A camada de Data Quality ajuda a aumentar a confiabilidade do pipeline e a reduzir riscos de erro no dashboard final.

---

## Escopo

Este documento cobre:

- objetivos da camada de Data Quality;
- tipos de validação aplicáveis;
- severidade das regras;
- contratos de qualidade;
- relatório de qualidade;
- aplicação por camada;
- integração com contratos de dados;
- boas práticas;
- benefícios;
- próximas evoluções.

Este documento não substitui os contratos detalhados por tabela, que estão documentados em `docs/data_contracts.md`.

---

## Conteúdo Principal

### 1. Tipos de validação

As principais validações são:

| Validação | Descrição |
|---|---|
| `not_empty` | Verifica se a tabela possui registros. |
| `required_columns` | Verifica se as colunas obrigatórias existem. |
| `no_nulls` | Verifica se colunas críticas não possuem nulos. |
| `unique_key` | Verifica se uma chave é única. |
| `max_null_ratio` | Verifica percentual máximo de nulos. |
| `allowed_values` | Verifica se valores pertencem a um domínio permitido. |
| `min_rows` | Verifica volume mínimo de registros. |
| `value_range` | Verifica intervalo permitido para valores numéricos. |
| `referential_integrity` | Verifica relacionamento entre fatos e dimensões. |
| `schema_stability` | Verifica estabilidade de schema em tabelas finais. |

### 2. Severidade das regras

As regras podem ter duas severidades principais:

| Severidade | Comportamento |
|---|---|
| `error` | Falha bloqueante. O pipeline deve parar ou impedir publicação da tabela. |
| `warning` | Falha não bloqueante. O pipeline registra o alerta e continua. |

Regras do tipo `error` devem ser usadas para problemas que comprometem a confiabilidade dos dados, como:

- tabela crítica vazia;
- ausência de colunas obrigatórias;
- chave primária nula;
- duplicidade em chave única;
- schema incompatível com o consumo analítico.

Regras do tipo `warning` devem ser usadas para problemas que precisam de monitoramento, mas não necessariamente impedem a execução, como:

- percentual elevado de nulos em campo não crítico;
- valores fora de domínio em pequena quantidade;
- volume diferente do esperado;
- relacionamento ausente em parcela pequena dos registros.

### 3. Contratos de qualidade

Os contratos de qualidade podem ser definidos em configuração, por exemplo:

```text
src/utils/quality/contracts.py
```

Cada contrato deve estar associado a uma camada e tabela.

Exemplo conceitual:

```python
"silver": {
    "proposicoes": {
        "not_empty": {"severity": "error"},
        "required_columns": {
            "columns": ["id_proposicao", "sigla_tipo", "ano", "ementa"],
            "severity": "error",
        },
        "no_nulls": {
            "columns": ["id_proposicao"],
            "severity": "error",
        },
        "unique_key": {
            "columns": ["id_proposicao"],
            "severity": "error",
        },
    }
}
```

Os contratos técnicos devem estar alinhados com o documento [Contratos de Dados](data_contracts.md).

### 4. Aplicação por camada

#### Bronze

Validações recomendadas:

- tabela não vazia;
- colunas mínimas da origem presentes;
- identificadores principais preenchidos quando disponíveis;
- metadados de ingestão presentes quando aplicável.

Objetivo:

Garantir que a ingestão da API retornou dados utilizáveis e rastreáveis.

#### Silver

Validações recomendadas:

- colunas padronizadas presentes;
- tipos de dados coerentes;
- chaves principais não nulas;
- duplicidades críticas removidas;
- nulos controlados em campos relevantes.

Objetivo:

Garantir que os dados estejam limpos, tipados e prontos para enriquecimento.

#### Gold

Validações recomendadas:

- campos derivados presentes;
- classificações geradas ou fallback aplicado;
- origem da classificação preenchida;
- domínios de categorias controlados;
- rastreabilidade com a Silver preservada.

Objetivo:

Garantir que as regras de negócio e classificações foram aplicadas corretamente.

#### Star Schema

Validações recomendadas:

- dimensões não vazias;
- fatos não vazios;
- chaves substitutas não nulas;
- chaves dimensionais únicas;
- integridade entre fatos e dimensões.

Objetivo:

Garantir que o modelo dimensional está consistente para análise.

#### Serving

Validações recomendadas:

- tabelas finais publicadas;
- schema estável para consumo no Power BI;
- colunas esperadas pelo dashboard presentes;
- falhas críticas bloqueando publicação.

Objetivo:

Garantir que apenas dados confiáveis sejam disponibilizados para consumo analítico.

### 5. Relatório de qualidade

Os resultados das validações podem ser persistidos em uma tabela Delta de monitoramento.

Campos sugeridos:

| Campo | Descrição |
|---|---|
| `execution_id` | Identificador da execução. |
| `layer` | Camada validada. |
| `table_name` | Tabela validada. |
| `rule_name` | Nome da regra. |
| `status` | Resultado da regra. |
| `severity` | Severidade da regra. |
| `message` | Mensagem explicativa. |
| `metric_value` | Valor observado. |
| `expected_value` | Valor esperado. |
| `checked_at` | Timestamp da validação. |

### 6. Fluxo recomendado

Fluxo ideal de aplicação da qualidade:

```text
Tabela produzida
      ↓
Identificar contrato aplicável
      ↓
Executar validações
      ↓
Registrar resultado
      ↓
Existem erros críticos?
      ├── Sim → bloquear avanço/publicação
      └── Não → permitir avanço
```

### 7. Integração com contratos de dados

A camada de Data Quality deve ser orientada pelos contratos de dados.

Relação esperada:

```text
Contrato de dados
      ↓
Regra declarativa
      ↓
Validação automatizada
      ↓
Resultado auditável
```

Os contratos definem o que é esperado. A camada de Data Quality executa e registra a verificação.

### 8. Benefícios

A camada de Data Quality aumenta a confiabilidade do pipeline ao garantir:

- tabelas não vazias;
- presença de colunas obrigatórias;
- chaves não nulas;
- unicidade de dimensões;
- controle de domínios;
- monitoramento de anomalias;
- rastreabilidade de falhas;
- maior segurança para publicação na camada Serving;
- maior confiança no dashboard Power BI.

### 9. Boas práticas

Boas práticas recomendadas:

- diferenciar regras críticas de alertas;
- evitar validações excessivamente rígidas em campos naturalmente incompletos;
- registrar resultados em tabela de monitoramento;
- versionar contratos quando o schema mudar;
- validar dimensões antes dos fatos;
- validar integridade referencial na camada Star;
- impedir publicação na Serving em caso de erro crítico;
- documentar exceções conhecidas.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para as validações de qualidade do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta Data Quality como competência demonstrada;
- `docs/architecture.md`, que posiciona qualidade de dados dentro da arquitetura;
- `docs/execution_guide.md`, que recomenda validações após cada etapa;
- `docs/data_contracts.md`, que detalha contratos por entidade e camada;
- `docs/star_schema.md`, que depende de integridade entre fatos e dimensões;
- `docs/dashboard.md`, que consome dados finais confiáveis;
- `docs/project_evolution.md`, que propõe evolução de Data Quality como etapa bloqueante.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Contratos de Dados](data_contracts.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Linhagem dos Dados](lineage.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções da camada de Data Quality:

- transformar regras em contratos YAML executáveis;
- persistir resultados das validações em tabela Delta;
- criar dashboard operacional de qualidade;
- tornar Data Quality uma etapa bloqueante antes da Serving;
- validar integridade referencial entre todos os fatos e dimensões;
- monitorar variação de volume entre execuções;
- criar alertas para falhas críticas;
- versionar contratos por tabela;
- adicionar validações específicas por domínio legislativo.
