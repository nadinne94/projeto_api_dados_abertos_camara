# Linhagem do Pipeline

## Objetivo

Este documento descreve a linhagem dos dados do projeto `projeto_api_dados_abertos_camara`, desde a ingestão na API pública da Câmara dos Deputados até a publicação das tabelas analíticas para consumo no Power BI.

O objetivo é tornar explícito o fluxo entre as camadas Bronze, Silver, Gold, Star Schema e Serving, facilitando manutenção, auditoria, explicação em entrevistas e evolução futura do projeto.

---

## Contexto

O projeto utiliza uma arquitetura lakehouse em camadas para transformar dados públicos legislativos em um produto analítico.

A linhagem mostra como cada entidade percorre o pipeline:

```text
API Dados Abertos Câmara
        ↓
Bronze
        ↓
Silver
        ↓
Gold
        ↓
Star Schema
        ↓
Serving SQL
        ↓
Power BI
```

Essa documentação ajuda a responder perguntas como:

- De onde vem cada tabela?
- Em qual camada uma entidade é tratada ou enriquecida?
- Quais tabelas Gold alimentam dimensões e fatos?
- Quais tabelas finais são usadas no Power BI?
- Onde a classificação ML/NLP entra no pipeline?

---

## Escopo

Este documento cobre:

- visão geral da linhagem;
- fluxo geral do pipeline;
- linhagem por entidade;
- linhagem das dimensões;
- linhagem das tabelas fato;
- linhagem da camada ML/NLP;
- classificações geradas;
- linhagem até o Power BI;
- benefícios da rastreabilidade;
- próximas evoluções.

Este documento não detalha schemas completos, contratos de dados ou medidas DAX. Esses temas possuem documentos próprios na pasta `docs/`.

---

## Conteúdo Principal

### 1. Visão geral da linhagem

| Camada | Responsabilidade | Tipo de dado |
|---|---|---|
| Bronze | Ingestão dos dados brutos da API. | Dados crus, próximos da origem. |
| Silver | Padronização, limpeza e normalização. | Dados tratados e consistentes. |
| Gold | Enriquecimento analítico e classificação. | Dados prontos para análise. |
| Star Schema | Modelagem dimensional. | Fatos e dimensões. |
| Serving | Publicação para consumo. | Tabelas SQL analíticas. |
| Power BI | Visualização e exploração. | Dashboard e indicadores. |

### 2. Fluxo geral

```text
/dados-abertos-camara-api
        ↓
src/bronze/ingest
        ↓
bronze.<dataset>
        ↓
src/silver/transforms
        ↓
silver.<dataset>
        ↓
src/gold/transforms
        ↓
gold.<dataset>
        ↓
src/star/dimensions + src/star/facts
        ↓
star_schema.<dimensoes_e_fatos>
        ↓
src/serving
        ↓
dados_abertos.star_schema
        ↓
Power BI
```

### 3. Linhagem por entidade

#### 3.1 Deputados

```text
API /deputados
        ↓
bronze.deputados
        ↓
silver.deputados
        ↓
gold.deputados
        ↓
star.dim_deputado
        ↓
star.fato_autoria
        ↓
star.fato_voto
        ↓
star.fato_presenca
        ↓
Power BI
```

Os dados de deputados são ingeridos da API, padronizados na Silver, enriquecidos na Gold e utilizados como dimensão analítica no Star Schema.

A dimensão `dim_deputado` é usada para cruzar autores de proposições, votos e presença em eventos.

#### 3.2 Partidos

```text
API /partidos
        ↓
bronze.partidos
        ↓
silver.partidos
        ↓
gold.partidos
        ↓
star.dim_partido
        ↓
Power BI
```

Os dados de partidos são usados como dimensão de análise política, permitindo segmentações por sigla, nome, espectro político, corrente ideológica e bloco ideológico.

#### 3.3 Órgãos

```text
API /orgaos
        ↓
bronze.orgaos
        ↓
silver.orgaos
        ↓
gold.orgaos
        ↓
star.dim_orgao
        ↓
star.fato_evento
        ↓
star.fato_tramitacao
        ↓
Power BI
```

Os órgãos legislativos são usados para contextualizar eventos, tramitações e atividades parlamentares.

#### 3.4 Proposições

```text
API /proposicoes
        ↓
bronze.proposicoes
        ↓
silver.proposicoes
        ↓
gold.proposicoes
        ↓
ML/NLP - classificação temática e jurídica
        ↓
gold.proposicoes
        ↓
star.dim_proposicao
        ↓
star.fato_proposicao
        ↓
star.fato_autoria
        ↓
star.fato_tramitacao
        ↓
star.fato_votacao
        ↓
Power BI
```

As proposições são a entidade central do projeto.

Na camada Gold, elas recebem enriquecimentos analíticos e classificações relacionadas a:

- tema;
- macrotema;
- natureza jurídica;
- tipo documental;
- categoria regimental;
- flags analíticas.

Essas informações alimentam a dimensão `dim_proposicao` e os fatos relacionados.

#### 3.5 Autores de proposições

```text
API /proposicoes/{id}/autores
        ↓
bronze.proposicoes_autores
        ↓
silver.proposicoes_autores
        ↓
gold.proposicoes_autores
        ↓
star.fato_autoria
        ↓
Power BI
```

A entidade de autores representa a relação entre proposições e seus respectivos autores.

A tabela final `fato_autoria` permite analisar:

- quantidade de proposições por deputado;
- quantidade de proposições por partido;
- autoria individual ou coletiva;
- relação entre parlamentar e tema legislativo.

#### 3.6 Tramitações

```text
API /proposicoes/{id}/tramitacoes
        ↓
bronze.proposicoes_tramitacoes
        ↓
silver.proposicoes_tramitacoes
        ↓
gold.proposicoes_tramitacoes
        ↓
star.fato_tramitacao
        ↓
Power BI
```

As tramitações registram movimentações das proposições ao longo do tempo.

A tabela `fato_tramitacao` permite analisar:

- evolução temporal das proposições;
- órgãos envolvidos;
- tipos de despacho;
- situação da proposição;
- tempo e fluxo legislativo.

#### 3.7 Votações

```text
API /proposicoes/{id}/votacoes
        ↓
bronze.proposicoes_votacoes
        ↓
silver.proposicoes_votacoes
        ↓
gold.proposicoes_votacoes
        ↓
star.fato_votacao
        ↓
Power BI
```

As votações registram deliberações associadas às proposições.

A tabela `fato_votacao` permite analisar:

- quantidade de votações por proposição;
- votações por período;
- votações por órgão;
- resultado de votações;
- relação entre proposições e decisões legislativas.

#### 3.8 Votos

```text
API /votacoes/{id}/votos
        ↓
bronze.votacoes_votos
        ↓
silver.votacoes_votos
        ↓
gold.votacoes_votos
        ↓
star.fato_voto
        ↓
Power BI
```

Os votos representam a manifestação individual dos parlamentares em votações.

A tabela `fato_voto` permite analisar:

- voto por deputado;
- voto por partido;
- voto por proposição;
- distribuição entre Sim, Não, Abstenção e outros valores;
- comportamento parlamentar por tema.

#### 3.9 Eventos

```text
API /eventos
        ↓
bronze.eventos
        ↓
silver.eventos
        ↓
gold.eventos
        ↓
star.dim_evento
        ↓
star.fato_evento
        ↓
Power BI
```

Eventos representam atividades legislativas, reuniões, audiências e demais compromissos institucionais.

A tabela `fato_evento` permite analisar:

- quantidade de eventos por período;
- tipo de evento;
- situação do evento;
- órgão responsável;
- local de realização.

#### 3.10 Presença em eventos

```text
API /eventos/{id}/deputados
        ↓
bronze.eventos_deputados
        ↓
silver.eventos_deputados
        ↓
gold.eventos_deputados
        ↓
star.fato_presenca
        ↓
Power BI
```

A presença em eventos relaciona deputados aos eventos legislativos.

A tabela `fato_presenca` permite analisar:

- presença parlamentar em eventos;
- participação por partido;
- participação por UF;
- relação entre deputados e órgãos/eventos.

### 4. Linhagem das tabelas dimensionais

| Dimensão | Fontes principais | Finalidade |
|---|---|---|
| `dim_tempo` | Calendário gerado internamente. | Análises temporais. |
| `dim_deputado` | `gold.deputados`. | Análise por parlamentar. |
| `dim_partido` | `gold.partidos`. | Análise por partido. |
| `dim_proposicao` | `gold.proposicoes`. | Análise por proposição, tema e natureza. |
| `dim_evento` | `gold.eventos`. | Análise por evento. |
| `dim_orgao` | `gold.orgaos`, `gold.tramitacoes`, `gold.votacoes`. | Análise por órgão legislativo. |

### 5. Linhagem das tabelas fato

| Fato | Fontes principais | Granularidade |
|---|---|---|
| `fato_proposicao` | `gold.proposicoes`, `dim_proposicao`, `dim_tempo`. | Uma linha por proposição. |
| `fato_autoria` | `gold.proposicoes_autores`, `dim_proposicao`, `dim_deputado`. | Uma linha por relação proposição-autor. |
| `fato_tramitacao` | `gold.proposicoes_tramitacoes`, `dim_proposicao`, `dim_orgao`, `dim_tempo`. | Uma linha por tramitação. |
| `fato_votacao` | `gold.proposicoes_votacoes`, `dim_proposicao`, `dim_orgao`, `dim_tempo`. | Uma linha por votação. |
| `fato_voto` | `gold.votacoes_votos`, `dim_deputado`, `dim_partido`, `dim_proposicao`. | Uma linha por voto parlamentar. |
| `fato_evento` | `gold.eventos`, `dim_evento`, `dim_orgao`, `dim_tempo`. | Uma linha por evento. |
| `fato_presenca` | `gold.eventos_deputados`, `dim_evento`, `dim_deputado`. | Uma linha por presença em evento. |

### 6. Linhagem do ML/NLP

```text
silver.proposicoes
        ↓
Pré-processamento textual
        ↓
Dicionários e regras regex
        ↓
Geração de labels e features
        ↓
Treinamento ML
        ↓
MLflow Tracking
        ↓
MLflow Model Registry
        ↓
Inferência na camada Gold
        ↓
gold.proposicoes
        ↓
dim_proposicao
        ↓
Power BI
```

### 7. Classificações geradas

As principais classificações aplicadas às proposições são:

| Classificação | Descrição | Origem |
|---|---|---|
| `tema_ementa` | Tema principal da proposição. | Regex + ML. |
| `macrotema` | Agrupamento analítico do tema. | Regra de negócio. |
| `natureza_juridica` | Finalidade legislativa da proposição. | Regex + ML. |
| `tipo_documental` | Tipo do documento legislativo. | Regra de negócio. |
| `categoria_regimental` | Categoria de tramitação ou impacto. | Regra de negócio. |
| `origem_tema` | Origem da classificação temática. | Regex, ML ou fallback. |
| `origem_natureza_juridica` | Origem da classificação jurídica. | Regex, ML ou fallback. |

### 8. Linhagem para Power BI

```text
star.dim_tempo
star.dim_deputado
star.dim_partido
star.dim_proposicao
star.dim_evento
star.dim_orgao
star.fato_proposicao
star.fato_autoria
star.fato_tramitacao
star.fato_votacao
star.fato_voto
star.fato_evento
star.fato_presenca
        ↓
serving / dados_abertos.star_schema
        ↓
Power BI
```

O Power BI deve consumir preferencialmente as tabelas publicadas pela camada Serving, e não diretamente as camadas intermediárias.

### 9. Benefícios da linhagem

A documentação de linhagem ajuda em:

- manutenção do pipeline;
- auditoria de transformações;
- identificação de origem de erros;
- explicação técnica em entrevistas;
- evolução segura do projeto;
- validação de dependências entre camadas;
- rastreabilidade entre API, Delta Lake, Star Schema e Power BI.

### 10. Cuidados e limitações

Pontos de atenção:

- a nomenclatura física pode variar conforme schemas e registries finais;
- algumas entidades dependem de endpoints filhos;
- dados de votações, votos e presença dependem da disponibilidade da API;
- classificações ML/NLP podem usar fallback quando o texto for insuficiente;
- análises históricas mais amplas dependem da ampliação do período de ingestão.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para entender o caminho dos dados entre as camadas do pipeline.

Ele se conecta diretamente a:

- `README.md`, que apresenta a arquitetura resumida do projeto;
- `docs/architecture.md`, que descreve os componentes e camadas;
- `docs/execution_guide.md`, que define a ordem de execução;
- `docs/star_schema.md`, que detalha dimensões e fatos;
- `docs/ml_nlp.md`, que explica a classificação textual;
- `docs/data_quality.md`, que define validações por camada;
- `docs/data_contracts.md`, que define contratos esperados para tabelas;
- `docs/dashboard.md`, que consome os dados finais no Power BI.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Modelo Star Schema](star_schema.md)
- [Classificação ML/NLP](ml_nlp.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções da documentação de linhagem:

- criar diagrama visual de lineage;
- gerar lineage automaticamente a partir dos registries;
- documentar dependências entre datasets;
- documentar colunas-chave por transição de camada;
- mapear transformações críticas por tabela;
- integrar lineage com Data Quality;
- adicionar lineage técnico dos modelos MLflow;
- documentar diferenças entre tabelas internas e tabelas publicadas na Serving.
