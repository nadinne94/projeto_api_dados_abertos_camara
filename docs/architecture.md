# Arquitetura do Projeto

## Objetivo

Este documento descreve a arquitetura técnica do projeto `projeto_api_dados_abertos_camara`.

O objetivo da arquitetura é transformar dados brutos da API pública da Câmara dos Deputados em um produto analítico confiável, organizado e pronto para visualização em Power BI.

A arquitetura foi desenhada para atender aos seguintes princípios:

- separação clara de responsabilidades;
- rastreabilidade entre camadas;
- modularidade;
- reprocessamento controlado;
- evolução incremental;
- suporte a dados analíticos;
- integração com Machine Learning;
- preparação para consumo em BI;
- observabilidade básica;
- facilidade de manutenção.

---

## Contexto

O projeto implementa um pipeline lakehouse com arquitetura medalhão, processamento em PySpark, armazenamento em Delta Lake, classificação ML/NLP, modelo dimensional em Star Schema e camada de Serving para consumo analítico.

A fonte principal é a API pública de Dados Abertos da Câmara dos Deputados. Os dados extraídos são organizados em camadas, enriquecidos com regras de negócio e preparados para análises sobre proposições, votações, deputados, partidos, órgãos, eventos e tramitações.

---

## Escopo

Este documento cobre:

- visão geral da arquitetura;
- componentes principais;
- estrutura de pastas;
- padrão arquitetural utilizado;
- camadas Bronze, Silver e Gold;
- ingestão de dados;
- registries;
- orquestração;
- Delta Lake;
- configuração;
- observabilidade;
- qualidade de dados;
- integração com ML/NLP;
- Star Schema;
- Serving;
- Power BI;
- pontos de evolução.

Este documento não detalha todos os contratos de dados, medidas DAX ou regras específicas de classificação. Esses temas possuem documentos próprios na pasta `docs/`.

---

## Conteúdo Principal

### 1. Visão geral da arquitetura

```text
┌──────────────────────────────────────────────┐
│ API Dados Abertos Câmara dos Deputados        │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Bronze                                       │
│ Ingestão bruta da API                         │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Silver                                       │
│ Padronização, limpeza e normalização          │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ ML/NLP                                       │
│ Treinamento e classificação textual           │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Gold                                         │
│ Enriquecimento analítico e classificação      │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Star Schema                                  │
│ Fatos e dimensões para análise                │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Serving                                      │
│ Publicação de tabelas analíticas              │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ Power BI                                     │
│ Visualização e exploração                     │
└──────────────────────────────────────────────┘
```

### 2. Componentes principais

| Componente | Responsabilidade |
|---|---|
| API Câmara | Fonte pública dos dados legislativos. |
| Bronze | Persistência dos dados brutos. |
| Silver | Limpeza, padronização e tipagem. |
| ML/NLP | Treinamento e inferência para classificação textual. |
| Gold | Enriquecimento, regras de negócio e classificação. |
| Star Schema | Modelo dimensional para análise. |
| Serving | Publicação das tabelas finais. |
| Power BI | Camada de visualização. |
| Monitoring | Logs, execução e rastreabilidade. |
| Data Quality | Validações formais por camada e tabela. |

### 3. Estrutura de pastas

```text
src/
  bronze/
    ingest/
    orchestration/
    monitoring/

  silver/
    transforms/
    registry/
    orchestration/

  gold/
    transforms/
    classification/
    registry/
    orchestration/

  star/
    dimensions/
    facts/
    registry/
    orchestration/

  ml/
    base/
    dictionaries/
    features/
    training/
    inference/
    orchestration/

  serving/

  config/

  utils/
    api/
    storage/
    monitoring/
    helpers/
    quality/
```

### 4. Padrões arquiteturais

O projeto combina três padrões principais:

1. **Arquitetura Medalhão**;
2. **Lakehouse com Delta Lake**;
3. **Modelo Dimensional Star Schema**.

Além disso, utiliza padrões de modularização como:

- registries;
- runners por camada;
- factories de ingestão;
- helpers reutilizáveis;
- contratos de qualidade;
- logging estruturado.

### 5. Arquitetura Medalhão

#### Bronze

A camada Bronze é responsável por capturar dados da API da forma mais próxima possível da origem.

Responsabilidades:

- consumir endpoints da API;
- tratar paginação;
- lidar com endpoints dependentes;
- controlar ingestões incrementais;
- adicionar metadados técnicos;
- salvar dados em Delta Lake;
- registrar logs de execução.

Dados típicos:

- deputados;
- partidos;
- órgãos;
- proposições;
- autores;
- tramitações;
- votações;
- votos;
- eventos;
- presença em eventos.

A Bronze não deve conter regras analíticas complexas. Seu papel principal é preservar o dado bruto e garantir rastreabilidade.

```text
API
 ↓
Bronze Delta
```

#### Silver

A camada Silver transforma os dados brutos em dados limpos, consistentes e padronizados.

Responsabilidades:

- renomear colunas;
- converter tipos;
- padronizar datas;
- tratar nulos;
- remover duplicidades;
- normalizar textos;
- padronizar identificadores;
- preparar dados para enriquecimento.

A Silver deve conter dados confiáveis e coerentes, mas ainda sem regras analíticas muito específicas.

```text
Bronze Delta
 ↓
Silver Delta
```

#### Gold

A camada Gold adiciona valor analítico aos dados.

Responsabilidades:

- criar atributos derivados;
- aplicar regras de negócio;
- classificar proposições;
- enriquecer votos, eventos e tramitações;
- gerar flags analíticas;
- preparar dados para modelo dimensional.

Exemplos de enriquecimentos:

- classificação temática;
- natureza jurídica;
- tipo documental;
- categoria regimental;
- macrotema;
- flags sociais, econômicas e normativas;
- classificação de votos;
- categorização de eventos.

```text
Silver Delta
 ↓
Gold Delta
```

### 6. Ingestão de dados

A ingestão foi desenhada para suportar diferentes padrões da API da Câmara.

#### Ingestão simples

Usada para endpoints que retornam entidades independentes.

Exemplos:

```text
/deputados
/partidos
/orgaos
```

Fluxo:

```text
request API
  ↓
parse response
  ↓
create DataFrame
  ↓
write Bronze
```

#### Ingestão incremental

Usada para endpoints que podem ser processados por período ou atualização.

Exemplos:

```text
/proposicoes
/eventos
/votacoes
```

Fluxo:

```text
read watermark
  ↓
request API with date filter
  ↓
write/merge Bronze
  ↓
update watermark
```

#### Ingestão dependente

Usada para endpoints filhos que dependem de IDs de entidades pai.

Exemplos:

```text
/proposicoes/{id}/autores
/proposicoes/{id}/tramitacoes
/proposicoes/{id}/votacoes
/votacoes/{id}/votos
/eventos/{id}/deputados
```

Fluxo:

```text
read parent ids
  ↓
for each parent id
  ↓
request child endpoint
  ↓
append parent id metadata
  ↓
write Bronze
```

### 7. Registries

O projeto utiliza registries para desacoplar os runners das transformações.

Em vez de codificar regras diretamente no runner, cada camada consulta um registry que informa:

- nome da tabela;
- função de transformação;
- origem;
- destino;
- chaves;
- dependências.

Benefícios:

- facilita inclusão de novos datasets;
- reduz acoplamento;
- melhora organização;
- torna o pipeline mais extensível;
- facilita leitura por camada.

Exemplo conceitual:

```python
TRANSFORM_REGISTRY = {
    "proposicoes": transform_proposicoes,
    "deputados": transform_deputados,
}
```

### 8. Orquestração

A orquestração é modular, com runners separados por camada.

```text
bronze/orchestration/runner.py
silver/orchestration/runner.py
gold/orchestration/runner.py
star/orchestration/runner.py
ml/orchestration/training_runner.py
```

Responsabilidades dos runners:

- identificar datasets a processar;
- consultar registries;
- executar transformações;
- aplicar validações;
- salvar dados;
- registrar logs;
- tratar erros.

Fluxo de execução recomendado:

```text
1. Bronze
2. Silver
3. ML Training
4. Gold
5. Star Schema
6. Serving
7. Power BI
```

### 9. Delta Lake

O Delta Lake é usado como formato de armazenamento nas camadas do pipeline.

Benefícios:

- transações ACID;
- schema enforcement;
- suporte a merge/upsert;
- histórico de versões;
- integração nativa com Spark;
- base adequada para arquitetura lakehouse.

Operações centralizadas em utilitários:

- leitura de tabelas;
- escrita;
- merge;
- overwrite;
- append;
- optimize;
- vacuum.

```text
src/utils/storage/delta_io.py
```

### 10. Configuração

As configurações ficam centralizadas em `src/config`.

```text
src/config/
  api_config.py
  dataset_config.py
  project_config.py
  spark_config.py
```

| Arquivo | Responsabilidade |
|---|---|
| `api_config.py` | Configurações da API. |
| `dataset_config.py` | Definição dos datasets, endpoints e dependências. |
| `project_config.py` | Caminhos, schemas e storage. |
| `spark_config.py` | Configurações Spark. |

A arquitetura ideal usa variáveis de ambiente para evitar valores fixos no código.

Exemplo:

```text
BASE_STORAGE_PATH=file:/tmp/dados_abertos_camara
BRONZE_SCHEMA=dados_abertos.bronze
SILVER_SCHEMA=dados_abertos.silver
GOLD_SCHEMA=dados_abertos.gold
STAR_SCHEMA=dados_abertos.star_schema
```

### 11. Observabilidade

O projeto prevê logs estruturados para rastrear a execução do pipeline.

Informações recomendadas nos logs:

- identificador da execução;
- camada;
- dataset;
- status;
- mensagem;
- quantidade de registros;
- timestamp de início e fim;
- duração;
- erro, quando houver.

Exemplo conceitual:

| execution_id | layer | dataset | status | records | timestamp |
|---|---|---|---|---|---|
| abc123 | bronze | proposicoes | success | 10000 | 2026-05-28 10:00 |

### 12. Data Quality

A qualidade de dados é uma parte essencial da arquitetura.

Validações esperadas:

- dataset não vazio;
- colunas obrigatórias;
- chaves não nulas;
- unicidade de chaves;
- percentual máximo de nulos;
- domínio de valores permitidos;
- contratos de dados por tabela e camada.

A integração ideal é:

```text
Tabela produzida
      ↓
Contrato de dados
      ↓
Validações de qualidade
      ↓
Resultado da validação
      ↓
Publicação ou bloqueio
```

### 13. ML/NLP

O módulo de ML/NLP apoia a classificação textual de proposições legislativas.

Responsabilidades:

- pré-processamento textual;
- aplicação de regras regex;
- uso de dicionários temáticos;
- treinamento de modelos supervisionados;
- registro e versionamento com MLflow;
- inferência na camada Gold;
- fallback para textos ambíguos.

Fluxo conceitual:

```text
Texto da proposição
      ↓
Regras + dicionários
      ↓
Modelo supervisionado
      ↓
Classificação temática e jurídica
      ↓
Gold
```

### 14. Star Schema

A camada Star Schema organiza os dados em modelo dimensional.

Principais elementos:

- dimensões;
- fatos;
- chaves substitutas;
- chaves de negócio;
- granularidade definida por fato;
- relacionamentos para consumo em BI.

Exemplos:

| Tipo | Exemplos |
|---|---|
| Dimensões | `dim_tempo`, `dim_deputado`, `dim_partido`, `dim_proposicao`, `dim_orgao` |
| Fatos | `fato_proposicao`, `fato_autoria`, `fato_tramitacao`, `fato_votacao`, `fato_voto`, `fato_evento`, `fato_presenca` |

### 15. Serving

A camada Serving publica as tabelas finais para consumo analítico.

Objetivos:

- disponibilizar tabelas estáveis para Power BI;
- facilitar consultas SQL;
- separar produção analítica das camadas internas;
- garantir uma interface clara para consumo.

### 16. Power BI

O Power BI consome as tabelas finais publicadas pela camada Serving.

Análises possíveis:

- proposições por tema;
- proposições por partido;
- proposições por deputado;
- tramitações ao longo do tempo;
- votações e votos parlamentares;
- presença em eventos;
- atuação parlamentar por período;
- comparação entre legislaturas.

---

## Como este documento se conecta ao projeto

Este documento serve como referência arquitetural principal do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta uma versão resumida da arquitetura;
- `docs/execution_guide.md`, que explica como executar o fluxo;
- `docs/lineage.md`, que detalha a movimentação dos dados entre camadas;
- `docs/data_quality.md`, que aprofunda as validações;
- `docs/data_contracts.md`, que documenta regras por tabela;
- `docs/ml_nlp.md`, que aprofunda a classificação textual;
- `docs/star_schema.md`, que detalha o modelo dimensional;
- `docs/dashboard.md`, que documenta o consumo analítico em Power BI.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Guia de Execução](execution_guide.md)
- [Linhagem dos Dados](lineage.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Classificação ML/NLP](ml_nlp.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções arquiteturais:

- formalizar orquestração com Databricks Workflows, Airflow, Prefect ou Dagster;
- configurar CI/CD com GitHub Actions;
- persistir métricas operacionais de execução;
- transformar contratos de dados em arquivos YAML executáveis;
- tornar Data Quality uma etapa bloqueante antes da Serving;
- melhorar monitoramento e alertas;
- ampliar suporte a legislaturas antigas;
- evoluir a classificação ML/NLP com novas abordagens semânticas;
- versionar releases do pipeline.
