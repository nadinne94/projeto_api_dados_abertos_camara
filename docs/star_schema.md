# Modelo Star Schema

## Objetivo

Este documento descreve o modelo dimensional do projeto `projeto_api_dados_abertos_camara`, incluindo dimensões, fatos, granularidade, relacionamentos, chaves e possibilidades analíticas.

O objetivo do Star Schema é transformar os dados enriquecidos da camada Gold em um modelo analítico simples, performático e adequado para consumo em Power BI.

---

## Contexto

O projeto utiliza dados legislativos da Câmara dos Deputados, processados em uma arquitetura lakehouse com camadas Bronze, Silver, Gold, Star Schema e Serving.

A camada Star Schema recebe dados tratados e enriquecidos da camada Gold e organiza essas informações em tabelas dimensionais e tabelas fato.

Esse modelo facilita análises sobre:

- proposições;
- autoria parlamentar;
- tramitações;
- votações;
- votos;
- eventos;
- presença parlamentar;
- partidos;
- órgãos legislativos;
- evolução temporal.

---

## Escopo

Este documento cobre:

- visão geral do modelo dimensional;
- origem dos dados usados na camada Star;
- dimensões principais;
- fatos principais;
- granularidade das tabelas;
- chaves substitutas e naturais;
- relacionamentos entre fatos e dimensões;
- possibilidades analíticas;
- conexão com Power BI;
- evolução futura do modelo.

Este documento não detalha medidas DAX, contratos de dados ou regras de classificação ML/NLP. Esses temas possuem documentos próprios na pasta `docs/`.

---

## Conteúdo Principal

### 1. Visão geral do modelo

O projeto utiliza um modelo dimensional em formato estrela para organizar os dados legislativos da Câmara dos Deputados.

A arquitetura geral do modelo é:

```text
Gold Tables
    ↓
Dimensions
    ↓
Facts
    ↓
Serving SQL
    ↓
Power BI
```

O Star Schema é composto por:

- dimensões, que descrevem entidades de análise;
- fatos, que representam eventos, relações ou medições;
- chaves substitutas, usadas para relacionar fatos e dimensões;
- chaves naturais, preservadas para rastreabilidade.

### 2. Objetivos analíticos

O modelo foi criado para permitir análises como:

- proposições por tema;
- proposições por ano;
- proposições por partido;
- autoria parlamentar;
- tramitações por órgão;
- votações por proposição;
- votos por deputado;
- votos por partido;
- presença parlamentar em eventos;
- eventos por órgão;
- evolução legislativa ao longo do tempo;
- comparação entre legislaturas.

### 3. Camada de origem

As tabelas dimensionais e fatos são construídas principalmente a partir da camada Gold.

```text
gold.deputados
gold.partidos
gold.proposicoes
gold.proposicoes_autores
gold.proposicoes_tramitacoes
gold.proposicoes_votacoes
gold.votacoes_votos
gold.eventos
gold.eventos_deputados
gold.orgaos
        ↓
star dimensions + facts
```

### 4. Dimensões

As dimensões armazenam atributos descritivos usados para filtros, segmentações e agrupamentos.

#### 4.1 `dim_tempo`

Dimensão calendário utilizada para análises temporais.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por data. |
| Chave substituta | `sk_tempo` no formato `yyyyMMdd`. |
| Chave natural | `data`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `data` | Data de referência. |
| `ano` | Ano da data. |
| `mes` | Número do mês. |
| `nome_mes` | Nome do mês. |
| `trimestre` | Trimestre. |
| `semestre` | Semestre. |
| `dia` | Dia do mês. |
| `dia_semana` | Dia da semana. |
| `nome_dia_semana` | Nome do dia da semana. |
| `ano_mes` | Ano e mês no formato `yyyy-MM`. |

Uso analítico:

- evolução temporal de proposições;
- evolução de votações;
- frequência de eventos;
- tramitações por período;
- filtros por ano, mês, trimestre ou semestre.

#### 4.2 `dim_deputado`

Dimensão com informações dos deputados.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por deputado. |
| Chave substituta | `sk_deputado`. |
| Chave natural | `id_deputado`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `nome_deputado` | Nome parlamentar. |
| `sigla_partido` | Partido atual ou associado. |
| `uf_origem` | Unidade federativa. |
| `regiao` | Região do Brasil. |
| `email` | E-mail institucional. |
| `url_foto` | URL da foto do deputado. |

Uso analítico:

- proposições por deputado;
- autoria parlamentar;
- votos por deputado;
- presença em eventos;
- participação por UF;
- análise por região.

#### 4.3 `dim_partido`

Dimensão com informações dos partidos políticos.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por partido. |
| Chave substituta | `sk_partido`. |
| Chave natural | `id_partido` ou `sigla_partido`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `sigla_partido` | Sigla do partido. |
| `nome_partido` | Nome completo do partido. |
| `espectro_politico` | Classificação geral do espectro político. |
| `corrente_ideologica` | Corrente ideológica associada. |
| `bloco_ideologico` | Agrupamento ideológico. |

Uso analítico:

- votos por partido;
- proposições por partido;
- comportamento parlamentar por legenda;
- análise por espectro político;
- filtros por bloco ideológico.

#### 4.4 `dim_proposicao`

Dimensão com informações analíticas das proposições legislativas.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por proposição. |
| Chave substituta | `sk_proposicao`. |
| Chave natural | `id_proposicao`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `sigla_tipo` | Sigla do tipo da proposição. |
| `tipo_documental` | Tipo documental classificado. |
| `categoria_regimental` | Categoria regimental. |
| `macrotema` | Macrotema analítico. |
| `tema_ementa` | Tema principal classificado. |
| `origem_tema` | Origem da classificação do tema. |
| `natureza_juridica` | Natureza jurídica classificada. |
| `origem_natureza_juridica` | Origem da classificação jurídica. |
| `peso_regimental` | Peso analítico/regimental. |
| `flag_normativa` | Indica proposição normativa. |
| `flag_fiscalizacao` | Indica proposição de fiscalização. |
| `flag_baixo_impacto` | Indica baixo impacto legislativo. |
| `flag_social` | Indica tema social. |
| `flag_economico` | Indica tema econômico. |
| `flag_tema_por_ml` | Indica classificação temática via ML. |
| `flag_natureza_por_ml` | Indica classificação jurídica via ML. |
| `flag_classificacao_automatica` | Indica uso de classificação automática. |

Uso analítico:

- proposições por tema;
- proposições por natureza jurídica;
- proposições por tipo documental;
- análise de macrotemas;
- comparação entre classificação por regra e ML;
- análise de impacto legislativo.

#### 4.5 `dim_evento`

Dimensão com informações dos eventos legislativos.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por evento. |
| Chave substituta | `sk_evento`. |
| Chave natural | `id_evento`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `tipo_evento_original` | Tipo original do evento. |
| `tipo_evento` | Tipo classificado. |
| `situacao_original` | Situação original. |
| `situacao_evento` | Situação padronizada. |
| `tipo_local` | Tipo do local. |
| `local_nome` | Nome do local. |
| `flag_evento_realizado` | Indica se o evento foi realizado. |

Uso analítico:

- eventos por tipo;
- eventos por situação;
- eventos realizados versus não realizados;
- presença parlamentar por evento;
- análise por local.

#### 4.6 `dim_orgao`

Dimensão com órgãos legislativos associados a tramitações, votações e eventos.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por órgão. |
| Chave substituta | `sk_orgao`. |
| Chave natural | `id_orgao`, `sigla_orgao` ou `orgao`. |

Atributos sugeridos:

| Campo | Descrição |
|---|---|
| `orgao` | Nome ou sigla do órgão legislativo. |
| `sigla_orgao` | Sigla do órgão, quando disponível. |
| `nome_orgao` | Nome completo do órgão, quando disponível. |

Uso analítico:

- tramitações por órgão;
- votações por órgão;
- eventos por órgão;
- participação institucional no processo legislativo.

### 5. Fatos

As tabelas fato armazenam eventos, ocorrências, relações e métricas.

#### 5.1 `fato_proposicao`

Fato principal de proposições.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por proposição. |
| Fontes principais | `gold.proposicoes`, `dim_proposicao`, `dim_tempo`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_proposicao` | `dim_proposicao` |
| `sk_tempo_apresentacao` | `dim_tempo` |

Métricas e atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_proposicao` | Chave natural para rastreabilidade. |
| `ano` | Ano da proposição. |
| `numero` | Número da proposição. |
| `data_apresentacao` | Data de apresentação. |
| `status_proposicao` | Situação ou status. |
| `flag_normativa` | Indicador analítico. |
| `flag_social` | Indicador analítico. |
| `flag_economico` | Indicador analítico. |

Análises possíveis:

- total de proposições;
- proposições por ano;
- proposições por tipo;
- proposições por tema;
- proposições por natureza jurídica.

#### 5.2 `fato_autoria`

Fato que relaciona proposições e autores.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por relação entre proposição e autor. |
| Fontes principais | `gold.proposicoes_autores`, `dim_proposicao`, `dim_deputado`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_proposicao` | `dim_proposicao` |
| `sk_deputado` | `dim_deputado` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_proposicao` | Chave natural da proposição. |
| `id_deputado` | Chave natural do deputado. |
| `tipo_autor` | Tipo de autor, quando disponível. |
| `ordem_assinatura` | Ordem de autoria, quando disponível. |

Análises possíveis:

- autores por proposição;
- proposições por deputado;
- proposições por partido;
- volume de autoria parlamentar.

#### 5.3 `fato_tramitacao`

Fato que representa movimentações ou tramitações de proposições.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por tramitação. |
| Fontes principais | `gold.proposicoes_tramitacoes`, `dim_proposicao`, `dim_tempo`, `dim_orgao`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_proposicao` | `dim_proposicao` |
| `sk_tempo` | `dim_tempo` |
| `sk_orgao` | `dim_orgao` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_proposicao` | Chave natural da proposição. |
| `data_tramitacao` | Data da tramitação. |
| `descricao_tramitacao` | Descrição da tramitação. |
| `status_tramitacao` | Status classificado da tramitação. |

Análises possíveis:

- quantidade de tramitações por proposição;
- tramitações por órgão;
- evolução da tramitação ao longo do tempo;
- status das proposições.

#### 5.4 `fato_votacao`

Fato que representa votações legislativas.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por votação. |
| Fontes principais | `gold.proposicoes_votacoes`, `dim_proposicao`, `dim_tempo`, `dim_orgao`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_proposicao` | `dim_proposicao` |
| `sk_tempo` | `dim_tempo` |
| `sk_orgao` | `dim_orgao` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_votacao` | Chave natural da votação. |
| `id_proposicao` | Chave natural da proposição. |
| `data_votacao` | Data da votação. |
| `resultado_votacao` | Resultado da votação. |

Análises possíveis:

- total de votações;
- votações por proposição;
- votações por órgão;
- votações ao longo do tempo.

#### 5.5 `fato_voto`

Fato que representa votos individuais dos parlamentares.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por voto parlamentar em uma votação. |
| Fontes principais | `gold.votacoes_votos`, `dim_deputado`, `dim_partido`, `dim_tempo`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_deputado` | `dim_deputado` |
| `sk_partido` | `dim_partido` |
| `sk_tempo` | `dim_tempo` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_votacao` | Chave natural da votação. |
| `id_deputado` | Chave natural do deputado. |
| `voto` | Voto registrado. |
| `orientacao_partido` | Orientação partidária, quando disponível. |

Análises possíveis:

- votos por deputado;
- votos por partido;
- votos por UF;
- comportamento de votação;
- distribuição entre votos Sim, Não, Abstenção e Obstrução.

#### 5.6 `fato_evento`

Fato que representa eventos legislativos.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por evento. |
| Fontes principais | `gold.eventos`, `dim_evento`, `dim_tempo`, `dim_orgao`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_evento` | `dim_evento` |
| `sk_tempo` | `dim_tempo` |
| `sk_orgao` | `dim_orgao` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_evento` | Chave natural do evento. |
| `data_evento` | Data do evento. |
| `situacao_evento` | Situação do evento. |
| `flag_evento_realizado` | Indica se o evento foi realizado. |

Análises possíveis:

- eventos por órgão;
- eventos por período;
- eventos por situação;
- eventos realizados versus não realizados.

#### 5.7 `fato_presenca`

Fato que representa presença parlamentar em eventos.

| Item | Descrição |
|---|---|
| Granularidade | Uma linha por presença parlamentar em evento. |
| Fontes principais | `gold.eventos_deputados`, `dim_evento`, `dim_deputado`, `dim_partido`, `dim_tempo`. |

Chaves estrangeiras:

| Campo | Dimensão |
|---|---|
| `sk_evento` | `dim_evento` |
| `sk_deputado` | `dim_deputado` |
| `sk_partido` | `dim_partido` |
| `sk_tempo` | `dim_tempo` |

Atributos possíveis:

| Campo | Descrição |
|---|---|
| `id_evento` | Chave natural do evento. |
| `id_deputado` | Chave natural do deputado. |
| `situacao_presenca` | Situação de presença, quando disponível. |

Análises possíveis:

- presença por deputado;
- presença por partido;
- presença por evento;
- participação parlamentar ao longo do tempo.

### 6. Relacionamentos principais

Modelo conceitual de relacionamentos:

```text
dim_tempo        ─┬─ fato_proposicao
                  ├─ fato_tramitacao
                  ├─ fato_votacao
                  ├─ fato_voto
                  ├─ fato_evento
                  └─ fato_presenca

dim_proposicao   ─┬─ fato_proposicao
                  ├─ fato_autoria
                  ├─ fato_tramitacao
                  └─ fato_votacao

dim_deputado     ─┬─ fato_autoria
                  ├─ fato_voto
                  └─ fato_presenca

dim_partido      ─┬─ fato_voto
                  └─ fato_presenca

dim_orgao        ─┬─ fato_tramitacao
                  ├─ fato_votacao
                  └─ fato_evento

dim_evento       ─┬─ fato_evento
                  └─ fato_presenca
```

### 7. Boas práticas adotadas

O modelo dimensional foi pensado para:

- separar atributos descritivos de eventos mensuráveis;
- facilitar filtros e segmentações no Power BI;
- reduzir complexidade de joins para usuários analíticos;
- preservar chaves naturais para rastreabilidade;
- usar chaves substitutas para relacionamento analítico;
- organizar fatos por granularidade clara;
- permitir evolução incremental com novas dimensões e fatos.

### 8. Cuidados e limitações

Pontos que devem ser observados:

- algumas entidades podem não possuir todos os identificadores em todos os endpoints;
- campos de partido podem representar situação no momento da extração, e não necessariamente histórico completo;
- classificações de tema e natureza jurídica podem depender de regras, ML ou fallback;
- presença e votação dependem da disponibilidade dos endpoints da API;
- análises históricas mais amplas exigem ampliação do período de ingestão.

### 9. Consumo no Power BI

O modelo Star Schema foi estruturado para facilitar o consumo no Power BI.

Boas práticas recomendadas:

- conectar preferencialmente às tabelas finais da camada Serving;
- usar dimensões para filtros e segmentações;
- usar fatos para contagens, métricas e indicadores;
- criar tabela de calendário no modelo ou utilizar `dim_tempo`;
- documentar medidas DAX em arquivo próprio;
- revisar cardinalidade e direção dos relacionamentos no Power BI.

### 10. Possibilidades analíticas

Com o modelo dimensional, é possível analisar:

- volume de proposições por ano;
- volume de proposições por tema;
- proposições por natureza jurídica;
- deputados mais associados à autoria;
- partidos com maior volume de proposições;
- órgãos com maior volume de tramitações;
- votações por período;
- votos por parlamentar;
- votos por partido;
- presença parlamentar em eventos;
- comparação entre legislaturas;
- evolução de temas legislativos ao longo do tempo.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para o modelo dimensional do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta a visão resumida do Star Schema;
- `docs/architecture.md`, que posiciona o Star Schema na arquitetura lakehouse;
- `docs/execution_guide.md`, que explica quando executar a camada Star;
- `docs/lineage.md`, que mostra a origem e destino dos dados;
- `docs/data_contracts.md`, que descreve regras esperadas para dimensões e fatos;
- `docs/dax_measures.md`, que documenta medidas analíticas sobre as tabelas finais;
- `docs/dashboard.md`, que mostra o consumo do modelo no Power BI.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Linhagem dos Dados](lineage.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Medidas DAX](dax_measures.md)
- [Dashboard Power BI](dashboard.md)
- [Classificação ML/NLP](ml_nlp.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções para o modelo dimensional:

- validar integridade referencial entre todos os fatos e dimensões;
- documentar fisicamente o schema final de cada tabela;
- criar diagrama visual do modelo;
- ampliar o período histórico para legislaturas antigas;
- incluir dimensões adicionais para legislatura, mandato e região;
- criar fatos agregados para otimizar consultas no Power BI;
- revisar historização de partido por parlamentar;
- documentar granularidade final com base nas tabelas publicadas;
- alinhar contratos de dados com as tabelas físicas da camada Star.
