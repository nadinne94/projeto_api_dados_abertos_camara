# Lineage do Pipeline

Este documento descreve a linhagem dos dados do projeto, desde a ingestão na API pública da Câmara dos Deputados até a publicação das tabelas analíticas para consumo no Power BI.

O objetivo é tornar explícito o fluxo entre as camadas Bronze, Silver, Gold, Star Schema e Serving, facilitando manutenção, auditoria, explicação em entrevistas e evolução futura do projeto.

## Visão Geral da Linhagem

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

| Camada   | Responsabilidade                         | Tipo de dado                   |
| -------- | ---------------------------------------- | ------------------------------ |
| Bronze   | Ingestão dos dados brutos da API         | Dados crus, próximos da origem |
| Silver   | Padronização, limpeza e normalização     | Dados tratados e consistentes  |
| Gold     | Enriquecimento analítico e classificação | Dados prontos para análise     |
| Star     | Modelagem dimensional                    | Fatos e dimensões              |
| Serving  | Publicação para consumo                  | Tabelas SQL analíticas         |
| Power BI | Visualização e exploração                | Dashboard e indicadores        |

## Fluxo Geral
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
## Linhagem por Entidade
###Deputados
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
**Descrição:**

Os dados de deputados são ingeridos da API, padronizados na Silver, enriquecidos na Gold e utilizados como dimensão analítica no Star Schema.

A dimensão dim_deputado é utilizada para cruzar autores de proposições, votos e presença em eventos.

### Partidos
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
**Descrição:**

Os dados de partidos são usados como dimensão de análise política, permitindo segmentações por sigla, nome, espectro político, corrente ideológica e bloco ideológico.

### Órgãos
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

**Descrição:**

Os órgãos legislativos são usados para contextualizar eventos, tramitações e atividades parlamentares.

### Proposições
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
**Descrição:**

As proposições são a entidade central do projeto.

Na camada Gold, elas recebem enriquecimentos analíticos e classificações relacionadas a:

- tema;
- macrotema;
- natureza jurídica;
- tipo documental;
- categoria regimental;
- flags analíticas.

Essas informações alimentam a dimensão dim_proposicao e os fatos relacionados.

### Autores de Proposições
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
**Descrição:**

A entidade de autores representa a relação entre proposições e seus respectivos autores.

A tabela final fato_autoria permite analisar:

- quantidade de proposições por deputado;
- quantidade de proposições por partido;
- autoria individual ou coletiva;
- relação entre parlamentar e tema legislativo.

### Tramitações
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

**Descrição:**

As tramitações registram movimentações das proposições ao longo do tempo.

A tabela fato_tramitacao permite analisar:

- evolução temporal das proposições;
- órgãos envolvidos;
- tipos de despacho;
- situação da proposição;
- tempo e fluxo legislativo.

### Votações
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

**Descrição:**

As votações registram deliberações associadas às proposições.

A tabela fato_votacao permite analisar:

- quantidade de votações por proposição;
- votações por período;
- votações por órgão;
- resultado de votações;
- relação entre proposições e decisões legislativas.

### Votos
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

**Descrição:**

Os votos representam a manifestação individual dos parlamentares em votações.

A tabela fato_voto permite analisar:

- voto por deputado;
- voto por partido;
- voto por proposição;
- distribuição entre Sim, Não, Abstenção e outros valores;
- comportamento parlamentar por tema.

### Eventos
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
**Descrição:**

Eventos representam atividades legislativas, reuniões, audiências e demais compromissos institucionais.

A tabela fato_evento permite analisar:

- quantidade de eventos por período;
- tipo de evento;
- situação do evento;
- órgão responsável;
- local de realização.

### Presença em Eventos
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

**Descrição:**

A presença em eventos relaciona deputados aos eventos legislativos.

A tabela fato_presenca permite analisar:

- presença parlamentar em eventos;
- participação por partido;
- participação por UF;
- relação entre deputados e órgãos/eventos.
## Linhagem das Tabelas Dimensionais
| Dimensão         | Fontes principais                                  | Finalidade                              |
| ---------------- | -------------------------------------------------- | --------------------------------------- |
| `dim_tempo`      | Calendário gerado internamente                     | Análises temporais                      |
| `dim_deputado`   | `gold.deputados`                                   | Análise por parlamentar                 |
| `dim_partido`    | `gold.partidos`                                    | Análise por partido                     |
| `dim_proposicao` | `gold.proposicoes`                                 | Análise por proposição, tema e natureza |
| `dim_evento`     | `gold.eventos`                                     | Análise por evento                      |
| `dim_orgao`      | `gold.orgaos`, `gold.tramitacoes`, `gold.votacoes` | Análise por órgão legislativo           |

## Linhagem das Tabelas Fato
| Fato              | Fontes principais                                  | Granularidade                          |
| ----------------- | -------------------------------------------------------------------------- | -------------------------------------- |
| `fato_proposicao` | `gold.proposicoes`, `dim_proposicao`, `dim_tempo`                          | Uma linha por proposição               |
| `fato_autoria`    | `gold.proposicoes_autores`, `dim_proposicao`, `dim_deputado`               | Uma linha por relação proposição-autor |
| `fato_tramitacao` | `gold.proposicoes_tramitacoes`, `dim_proposicao`, `dim_orgao`, `dim_tempo` | Uma linha por tramitação               |
| `fato_votacao`    | `gold.proposicoes_votacoes`, `dim_proposicao`, `dim_orgao`, `dim_tempo`    | Uma linha por votação                  |
| `fato_voto`       | `gold.votacoes_votos`, `dim_deputado`, `dim_partido`, `dim_proposicao`     | Uma linha por voto parlamentar         |
| `fato_evento`     | `gold.eventos`, `dim_evento`, `dim_orgao`, `dim_tempo`                     | Uma linha por evento                   |
| `fato_presenca`   | `gold.eventos_deputados`, `dim_evento`, `dim_deputado`                     | Uma linha por presença em evento       |

## Linhagem do ML/NLP
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
## Classificações Geradas

As principais classificações aplicadas às proposições são:

| Classificação              | Descrição                            | Origem                |
| -------------------------- | ------------------------------------ | --------------------- |
| `tema_ementa`              | Tema principal da proposição         | Regex + ML            |
| `macrotema`                | Agrupamento analítico do tema        | Regra de negócio      |
| `natureza_juridica`        | Finalidade legislativa da proposição | Regex + ML            |
| `tipo_documental`          | Tipo do documento legislativo        | Regra de negócio      |
| `categoria_regimental`     | Categoria de tramitação ou impacto   | Regra de negócio      |
| `origem_tema`              | Origem da classificação temática     | Regex, ML ou fallback |
| `origem_natureza_juridica` | Origem da classificação jurídica     | Regex, ML ou fallback |

## Linhagem para Power BI

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
serving.publish_tables
        ↓
dados_abertos.star_schema
        ↓
Power BI
```

## Principais Relacionamentos Analíticos
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

## Observabilidade da Linhagem

O projeto possui logs estruturados para rastrear execuções do pipeline.

As informações monitoradas incluem:

- identificador da execução;
- camada;
- dataset;
- status;
- quantidade de registros;
- mensagem de execução;
- timestamp.

Esses logs ajudam a responder:

- qual dataset foi processado;
- quando foi processado;
- quantos registros foram gerados;
- se houve erro;
- em qual camada o erro ocorreu.

## Pontos de Controle de Qualidade

Os principais pontos onde Data Quality deve ser aplicado são:
```text
Bronze:
  depois da ingestão da API

Silver:
  depois da padronização

Gold:
  depois do enriquecimento e classificação

Star:
  depois da criação de fatos e dimensões

Serving:
  depois da publicação das tabelas finais
```

## Evoluções Futuras de Linhagem

Possíveis melhorias:

- criar documentação automática de dependências entre tabelas;
- adicionar data contracts por dataset;
- integrar com Unity Catalog;
- integrar com OpenLineage;
- gerar diagrama automático do pipeline;
- versionar contratos de schema;
- criar dashboard de execução do pipeline;
- criar alerta para falhas de linhagem ou tabelas vazias.

##Resumo

Este pipeline transforma dados públicos legislativos em um produto analítico estruturado.

A linhagem principal pode ser resumida como:

API pública
  → Bronze
  → Silver
  → Gold + ML/NLP
  → Star Schema
  → Serving SQL
  → Power BI