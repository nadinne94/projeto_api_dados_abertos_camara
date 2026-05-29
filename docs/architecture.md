# Arquitetura do Projeto

Este documento descreve a arquitetura técnica do projeto de Engenharia de Dados desenvolvido com dados públicos da Câmara dos Deputados.

O projeto implementa um pipeline lakehouse com arquitetura medalhão, processamento em PySpark, armazenamento em Delta Lake, classificação NLP/ML, modelo dimensional em star schema e camada de serving para consumo analítico em Power BI.


## Objetivo da Arquitetura

O objetivo da arquitetura é transformar dados brutos da API pública da Câmara dos Deputados em um produto analítico confiável, organizado e pronto para visualização.

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

## Visão Geral

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
│ Gold                                         │
│ Enriquecimento analítico e classificação      │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ ML/NLP                                       │
│ Classificação temática e jurídica             │
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

## Componentes Principais

| Componente   | Responsabilidade                                  |
| ------------ | ------------------------------------------------- |
| API Câmara   | Fonte pública dos dados legislativos              |
| Bronze       | Persistência dos dados brutos                     |
| Silver       | Limpeza, padronização e tipagem                   |
| Gold         | Enriquecimento, regras de negócio e classificação |
| ML/NLP       | Classificação textual de proposições              |
| Star Schema  | Modelo dimensional para análise                   |
| Serving      | Publicação das tabelas finais                     |
| Power BI     | Camada de visualização                            |
| Monitoring   | Logs, execução e rastreabilidade                  |
| Data Quality | Validações formais por camada e tabela            |


## Estrutura de Pastas

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

## Padrão Arquitetural

O projeto combina três padrões principais:

1. **Arquitetura Medalhão**
2. **Lakehouse com Delta Lake**
3. **Modelo Dimensional Star Schema**

Além disso, o projeto usa padrões de modularização como:

* registries;
* runners por camada;
* factories de ingestão;
* helpers reutilizáveis;
* contratos de qualidade;
* logging estruturado.

# Arquitetura Medalhão

## Bronze

A camada Bronze é responsável por capturar dados da API da forma mais próxima possível da origem.

### Responsabilidades

* consumir endpoints da API;
* tratar paginação;
* lidar com endpoints dependentes;
* controlar ingestões incrementais;
* adicionar metadados técnicos;
* salvar dados em Delta Lake;
* registrar logs de execução.

### Dados típicos

* deputados;
* partidos;
* órgãos;
* proposições;
* autores;
* tramitações;
* votações;
* votos;
* eventos;
* presença em eventos.

### Características

A Bronze não deve conter regras analíticas complexas. Seu papel principal é preservar o dado bruto e garantir rastreabilidade.

```text
API
 ↓
Bronze Delta
```

## Silver

A camada Silver é responsável por transformar os dados brutos em dados limpos, consistentes e padronizados.

### Responsabilidades

* renomear colunas;
* converter tipos;
* padronizar datas;
* tratar nulos;
* remover duplicidades;
* normalizar textos;
* padronizar identificadores;
* preparar dados para enriquecimento.

### Características

A Silver deve conter dados confiáveis e coerentes, mas ainda sem regras analíticas muito específicas.

```text
Bronze Delta
 ↓
Silver Delta
```

## Gold

A camada Gold adiciona valor analítico aos dados.

### Responsabilidades

* criar atributos derivados;
* aplicar regras de negócio;
* classificar proposições;
* enriquecer votos, eventos e tramitações;
* gerar flags analíticas;
* preparar dados para modelo dimensional.

### Exemplos de enriquecimentos

* classificação temática;
* natureza jurídica;
* tipo documental;
* categoria regimental;
* macrotema;
* flags sociais, econômicas e normativas;
* classificação de votos;
* categorização de eventos.

```text
Silver Delta
 ↓
Gold Delta
```

# Ingestão de Dados

A ingestão foi desenhada para suportar diferentes padrões da API da Câmara.

## Ingestão Simples

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

---

## Ingestão Incremental

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


## Ingestão Dependente

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

---

# Registries

O projeto utiliza registries para desacoplar os runners das transformações.

## Objetivo

Evitar que os runners conheçam detalhes internos de cada transformação.

Em vez de codificar regras diretamente no runner, cada camada consulta um registry que informa:

* nome da tabela;
* função de transformação;
* origem;
* destino;
* chaves;
* dependências.


## Benefícios

* facilita inclusão de novos datasets;
* reduz acoplamento;
* melhora organização;
* torna o pipeline mais extensível;
* facilita leitura por camada.

Exemplo conceitual:

```python
TRANSFORM_REGISTRY = {
    "proposicoes": transform_proposicoes,
    "deputados": transform_deputados,
}
```

# Orquestração

A orquestração é modular, com runners separados por camada.

```text
bronze/orchestration/runner.py
silver/orchestration/runner.py
gold/orchestration/runner.py
star/orchestration/runner.py
ml/orchestration/training_runner.py
```

## Responsabilidades dos runners

* identificar datasets a processar;
* consultar registries;
* executar transformações;
* aplicar validações;
* salvar dados;
* registrar logs;
* tratar erros.

---

## Fluxo de execução recomendado

```text
1. Bronze
2. Silver
3. ML Training
4. Gold
5. Star Schema
6. Serving
7. Power BI
```

---

# Delta Lake

O Delta Lake é usado como formato de armazenamento nas camadas do pipeline.

## Benefícios

* transações ACID;
* schema enforcement;
* suporte a merge/upsert;
* histórico de versões;
* integração nativa com Spark;
* base adequada para arquitetura lakehouse.

---

## Operações utilizadas

O projeto centraliza operações Delta em utilitários, como:

* leitura de tabelas;
* escrita;
* merge;
* overwrite;
* append;
* optimize;
* vacuum.

```text
src/utils/storage/delta_io.py
```

---

# Configuração

As configurações ficam centralizadas em `src/config`.

```text
src/config/
  api_config.py
  dataset_config.py
  project_config.py
  spark_config.py
```

## Responsabilidades

| Arquivo             | Responsabilidade                                 |
| ------------------- | ------------------------------------------------ |
| `api_config.py`     | Configurações da API                             |
| `dataset_config.py` | Definição dos datasets, endpoints e dependências |
| `project_config.py` | Caminhos, schemas e storage                      |
| `spark_config.py`   | Configurações Spark                              |


## Parametrização por ambiente

A arquitetura ideal usa variáveis de ambiente para evitar valores fixos no código.

Exemplo:

```text
BASE_STORAGE_PATH=file:/tmp/dados_abertos_camara
BRONZE_SCHEMA=dados_abertos.bronze
SILVER_SCHEMA=dados_abertos.silver
GOLD_SCHEMA=dados_abertos.gold
STAR_SCHEMA=dados_abertos.star_schema
```

Essas variáveis podem ser descritas no arquivo:

```text
.env.example
```

# ML/NLP Legislativo

O projeto possui uma camada de NLP e Machine Learning voltada à classificação de proposições legislativas.

## Objetivo

Classificar proposições com base em texto legislativo, especialmente ementa e descrição.

As principais classificações são:

* tema;
* macrotema;
* natureza jurídica;
* tipo documental;
* categoria regimental.

## Arquitetura ML/NLP

```text
Silver Proposições
        ↓
Pré-processamento textual
        ↓
Regras regex + dicionários
        ↓
Features textuais
        ↓
Treinamento supervisionado
        ↓
MLflow Tracking
        ↓
Model Registry
        ↓
Inferência
        ↓
Gold Proposições
```

## Estratégia Híbrida

O projeto usa uma estratégia híbrida:

| Técnica               | Uso                                       |
| --------------------- | ----------------------------------------- |
| Regex                 | Capturar padrões legislativos explícitos  |
| Dicionários           | Apoiar classificação temática e jurídica  |
| TF-IDF                | Transformar texto em features             |
| Modelo supervisionado | Generalizar padrões textuais              |
| MLflow                | Rastrear experimentos e versionar modelos |
| Fallback              | Evitar classificação forçada              |

## Por que regex + ML?

O domínio legislativo possui muitos padrões textuais explícitos, como:

* altera lei;
* institui política;
* revoga dispositivo;
* cria programa;
* dispõe sobre;
* concede homenagem;
* institui data comemorativa.

Regex captura bem esse tipo de padrão.

O ML complementa ao lidar com textos menos explícitos e melhorar a generalização.

# Star Schema

A camada Star organiza os dados em modelo dimensional para consumo analítico.

## Objetivo

Facilitar consultas e dashboards, separando:

* dimensões descritivas;
* fatos transacionais ou relacionais.

## Dimensões

| Dimensão         | Descrição                        |
| ---------------- | -------------------------------- |
| `dim_tempo`      | Calendário analítico             |
| `dim_deputado`   | Dados dos deputados              |
| `dim_partido`    | Dados dos partidos               |
| `dim_proposicao` | Dados analíticos das proposições |
| `dim_evento`     | Dados dos eventos                |
| `dim_orgao`      | Dados dos órgãos legislativos    |


## Fatos

| Fato              | Granularidade                          |
| ----------------- | -------------------------------------- |
| `fato_proposicao` | Uma linha por proposição               |
| `fato_autoria`    | Uma linha por relação proposição-autor |
| `fato_tramitacao` | Uma linha por tramitação               |
| `fato_votacao`    | Uma linha por votação                  |
| `fato_voto`       | Uma linha por voto parlamentar         |
| `fato_evento`     | Uma linha por evento                   |
| `fato_presenca`   | Uma linha por presença em evento       |

## Relacionamentos principais

```text
dim_proposicao 1 ─── * fato_proposicao
dim_proposicao 1 ─── * fato_autoria
dim_proposicao 1 ─── * fato_tramitacao
dim_proposicao 1 ─── * fato_votacao
dim_proposicao 1 ─── * fato_voto

dim_deputado   1 ─── * fato_autoria
dim_deputado   1 ─── * fato_voto
dim_deputado   1 ─── * fato_presenca

dim_partido    1 ─── * fato_voto

dim_evento     1 ─── * fato_evento
dim_evento     1 ─── * fato_presenca

dim_orgao      1 ─── * fato_evento
dim_orgao      1 ─── * fato_tramitacao
dim_orgao      1 ─── * fato_votacao

dim_tempo      1 ─── * fatos temporais
```

# Surrogate Keys

As dimensões utilizam surrogate keys para relacionamentos com fatos.

A estratégia recomendada é usar chaves determinísticas baseadas em hash das chaves naturais.

Exemplo conceitual:

```text
sk_deputado = sha2(id_deputado)
sk_proposicao = sha2(id_proposicao)
sk_partido = sha2(id_partido)
```

## Benefícios

* estabilidade entre reprocessamentos;
* consistência entre fatos e dimensões;
* independência do particionamento Spark;
* melhor suporte a reexecuções;
* maior confiabilidade analítica.

# Data Quality

A arquitetura prevê uma camada formal de Data Quality.

```text
src/utils/quality/
  checks.py
  contracts.py
  runner.py
  report.py
```

## Tipos de validação

| Regra              | Descrição                                      |
| ------------------ | ---------------------------------------------- |
| `not_empty`        | Verifica se a tabela possui registros          |
| `required_columns` | Verifica se colunas obrigatórias existem       |
| `no_nulls`         | Verifica se colunas críticas não possuem nulos |
| `unique_key`       | Verifica unicidade de chaves                   |
| `max_null_ratio`   | Controla percentual máximo de nulos            |
| `allowed_values`   | Valida domínio permitido de valores            |
| `min_rows`         | Verifica volume mínimo                         |
| `value_range`      | Valida intervalo numérico                      |

---

## Pontos de aplicação

```text
Bronze:
  após ingestão

Silver:
  após padronização

Gold:
  após enriquecimento

Star:
  após construção de fatos e dimensões

Serving:
  após publicação
```

# Observabilidade

O projeto possui observabilidade por meio de logs estruturados.

## Logs do pipeline

Os logs registram:

* execution_id;
* camada;
* dataset;
* status;
* quantidade de registros;
* mensagem;
* timestamp;
* erro, quando aplicável.

## Monitoramento recomendado

Além dos logs atuais, a arquitetura pode evoluir para monitorar:

* duração por etapa;
* volume processado;
* volume rejeitado;
* freshness;
* falhas por camada;
* falhas de Data Quality;
* versão do modelo ML;
* versão do pipeline.

# Serving

A camada Serving publica as tabelas finais para consumo analítico.

## Objetivo

Disponibilizar as dimensões e fatos em formato adequado para:

* Power BI;
* consultas SQL;
* análises exploratórias;
* dashboards executivos;
* validações analíticas.

## Fluxo de publicação

```text
Star Delta Tables
        ↓
Serving Publish Tables
        ↓
SQL Schema
        ↓
Power BI
```

# Power BI

O Power BI consome as tabelas finais do star schema.

## Modelo esperado

```text
Dimensões:
  dim_tempo
  dim_deputado
  dim_partido
  dim_proposicao
  dim_evento
  dim_orgao

Fatos:
  fato_proposicao
  fato_autoria
  fato_tramitacao
  fato_votacao
  fato_voto
  fato_evento
  fato_presenca
```

## Análises possíveis

* proposições por tema;
* proposições por ano;
* proposições por partido;
* autores mais frequentes;
* votos por parlamentar;
* votos por partido;
* tramitações por órgão;
* eventos por tipo;
* presença parlamentar;
* evolução legislativa ao longo do tempo.

# Fluxo de Execução

## Execução completa

```text
1. Ingestão Bronze
2. Transformação Silver
3. Treinamento ML
4. Enriquecimento Gold
5. Construção Star Schema
6. Publicação Serving
7. Consumo Power BI
```

## Execução conceitual por módulo

```bash
python -m src.bronze.orchestration.runner
python -m src.silver.orchestration.runner
python -m src.ml.orchestration.training_runner
python -m src.gold.orchestration.runner
python -m src.star.orchestration.runner
python -m src.serving.publish_tables
```
# Decisões Técnicas

## Uso de arquitetura medalhão

A arquitetura medalhão foi escolhida para separar claramente os estágios dos dados:

* dados brutos;
* dados limpos;
* dados enriquecidos;
* dados analíticos.


## Uso de Delta Lake

Delta Lake foi escolhido para aumentar a confiabilidade do data lake, permitindo:

* transações;
* controle de schema;
* histórico;
* upsert;
* integração com Spark.

## Uso de PySpark

PySpark foi escolhido por ser uma tecnologia amplamente usada em pipelines lakehouse e permitir processamento distribuído.

## Uso de registries

Registries reduzem o acoplamento entre orquestração e transformação, permitindo adicionar novos datasets com menor impacto no código.


## Uso de star schema

O star schema foi escolhido por ser adequado para consumo em BI, facilitando filtros, agregações e relacionamentos analíticos.


## Uso de MLflow

MLflow foi escolhido para rastrear experimentos e organizar o ciclo de vida dos modelos de classificação.

# Resumo da Arquitetura

Este projeto implementa uma arquitetura moderna de dados com:

* ingestão de API pública;
* arquitetura medalhão;
* Delta Lake;
* PySpark;
* ML/NLP aplicado;
* MLflow;
* star schema;
* serving analítico;
* Power BI;
* logs estruturados;
* proposta de Data Quality formal.

