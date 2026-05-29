# Star Schema

Este documento descreve o modelo dimensional do projeto, incluindo dimensões, fatos, granularidade, relacionamentos, chaves e principais possibilidades analíticas.

O objetivo do Star Schema é transformar os dados enriquecidos da camada Gold em um modelo analítico simples, performático e adequado para consumo em Power BI.

## Visão Geral

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
````

O Star Schema é composto por:

* dimensões, que descrevem entidades de análise;
* fatos, que representam eventos, relações ou medições;
* chaves substitutas, usadas para relacionar fatos e dimensões;
* chaves naturais, preservadas para rastreabilidade.

## Objetivos do Modelo Dimensional

O modelo foi criado para permitir análises como:

* proposições por tema;
* proposições por ano;
* proposições por partido;
* autoria parlamentar;
* tramitações por órgão;
* votações por proposição;
* votos por deputado;
* votos por partido;
* presença parlamentar em eventos;
* eventos por órgão;
* evolução legislativa ao longo do tempo.


## Camada de Origem

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

# Dimensões

As dimensões armazenam atributos descritivos usados para filtros, segmentações e agrupamentos.

---

## `dim_tempo`

### Descrição

Dimensão calendário utilizada para análises temporais.

### Granularidade

Uma linha por data.

### Chave

| Campo      | Tipo    | Descrição                   |
| ---------- | ------- | --------------------------- |
| `sk_tempo` | inteiro | Chave no formato `yyyyMMdd` |
| `data`     | data    | Data de referência          |

### Atributos sugeridos

| Campo             | Descrição                      |
| ----------------- | ------------------------------ |
| `ano`             | Ano da data                    |
| `mes`             | Número do mês                  |
| `nome_mes`        | Nome do mês                    |
| `trimestre`       | Trimestre                      |
| `semestre`        | Semestre                       |
| `dia`             | Dia do mês                     |
| `dia_semana`      | Dia da semana                  |
| `nome_dia_semana` | Nome do dia da semana          |
| `ano_mes`         | Ano e mês no formato `yyyy-MM` |

### Uso analítico

* evolução temporal de proposições;
* evolução de votações;
* frequência de eventos;
* tramitações por período;
* filtros por ano, mês, trimestre ou semestre.

---

## `dim_deputado`

### Descrição

Dimensão com informações dos deputados.

### Granularidade

Uma linha por deputado.

### Chaves

| Campo         | Tipo           | Descrição                 |
| ------------- | -------------- | ------------------------- |
| `sk_deputado` | string/hash    | Surrogate key da dimensão |
| `id_deputado` | inteiro/string | Chave natural da API      |

### Atributos

| Campo           | Descrição                  |
| --------------- | -------------------------- |
| `nome_deputado` | Nome parlamentar           |
| `sigla_partido` | Partido atual ou associado |
| `uf_origem`     | Unidade federativa         |
| `regiao`        | Região do Brasil           |
| `email`         | E-mail institucional       |
| `url_foto`      | URL da foto do deputado    |

### Uso analítico

* proposições por deputado;
* autoria parlamentar;
* votos por deputado;
* presença em eventos;
* participação por UF;
* análise por região.

---

## `dim_partido`

### Descrição

Dimensão com informações dos partidos políticos.

### Granularidade

Uma linha por partido.

### Chaves

| Campo        | Tipo           | Descrição                 |
| ------------ | -------------- | ------------------------- |
| `sk_partido` | string/hash    | Surrogate key da dimensão |
| `id_partido` | inteiro/string | Chave natural da API      |

### Atributos

| Campo                 | Descrição                                |
| --------------------- | ---------------------------------------- |
| `sigla_partido`       | Sigla do partido                         |
| `nome_partido`        | Nome completo do partido                 |
| `espectro_politico`   | Classificação geral do espectro político |
| `corrente_ideologica` | Corrente ideológica associada            |
| `bloco_ideologico`    | Agrupamento ideológico                   |

### Uso analítico

* votos por partido;
* proposições por partido;
* comportamento parlamentar por legenda;
* análise por espectro político;
* filtros por bloco ideológico.

---

## `dim_proposicao`

### Descrição

Dimensão com informações analíticas das proposições legislativas.

### Granularidade

Uma linha por proposição.

### Chaves

| Campo           | Tipo           | Descrição                 |
| --------------- | -------------- | ------------------------- |
| `sk_proposicao` | string/hash    | Surrogate key da dimensão |
| `id_proposicao` | inteiro/string | Chave natural da API      |

### Atributos

| Campo                           | Descrição                              |
| ------------------------------- | -------------------------------------- |
| `sigla_tipo`                    | Sigla do tipo da proposição            |
| `tipo_documental`               | Tipo documental classificado           |
| `categoria_regimental`          | Categoria regimental                   |
| `macrotema`                     | Macrotema analítico                    |
| `tema_ementa`                   | Tema principal classificado            |
| `origem_tema`                   | Origem da classificação do tema        |
| `natureza_juridica`             | Natureza jurídica classificada         |
| `origem_natureza_juridica`      | Origem da classificação jurídica       |
| `peso_regimental`               | Peso analítico/regimental              |
| `flag_normativa`                | Indica proposição normativa            |
| `flag_fiscalizacao`             | Indica proposição de fiscalização      |
| `flag_baixo_impacto`            | Indica baixo impacto legislativo       |
| `flag_social`                   | Indica tema social                     |
| `flag_economico`                | Indica tema econômico                  |
| `flag_tema_por_ml`              | Indica classificação temática via ML   |
| `flag_natureza_por_ml`          | Indica classificação jurídica via ML   |
| `flag_classificacao_automatica` | Indica uso de classificação automática |

### Uso analítico

* proposições por tema;
* proposições por natureza jurídica;
* proposições por tipo documental;
* análise de macrotemas;
* comparação entre classificação por regra e ML;
* análise de impacto legislativo.

---

## `dim_evento`

### Descrição

Dimensão com informações dos eventos legislativos.

### Granularidade

Uma linha por evento.

### Chaves

| Campo       | Tipo           | Descrição                 |
| ----------- | -------------- | ------------------------- |
| `sk_evento` | string/hash    | Surrogate key da dimensão |
| `id_evento` | inteiro/string | Chave natural da API      |

### Atributos

| Campo                   | Descrição                        |
| ----------------------- | -------------------------------- |
| `tipo_evento_original`  | Tipo original do evento          |
| `tipo_evento`           | Tipo classificado                |
| `situacao_original`     | Situação original                |
| `situacao_evento`       | Situação padronizada             |
| `tipo_local`            | Tipo do local                    |
| `local_nome`            | Nome do local                    |
| `flag_evento_realizado` | Indica se o evento foi realizado |

### Uso analítico

* eventos por tipo;
* eventos por situação;
* eventos realizados versus não realizados;
* presença parlamentar por evento;
* análise por local.

---

## `dim_orgao`

### Descrição

Dimensão com órgãos legislativos associados a tramitações, votações e eventos.

### Granularidade

Uma linha por órgão.

### Chaves

| Campo      | Tipo        | Descrição                      |
| ---------- | ----------- | ------------------------------ |
| `sk_orgao` | string/hash | Surrogate key da dimensão      |
| `orgao`    | string      | Chave natural textual do órgão |

### Atributos

| Campo   | Descrição                          |
| ------- | ---------------------------------- |
| `orgao` | Nome ou sigla do órgão legislativo |

### Uso analítico

* tramitações por órgão;
* votações por órgão;
* eventos por órgão;
* participação institucional no processo legislativo.

---

# Fatos

As tabelas fato armazenam eventos, ocorrências, relações e métricas.

---

## `fato_proposicao`

### Descrição

Fato principal de proposições.

### Granularidade

Uma linha por proposição.

### Fontes principais

* `gold.proposicoes`;
* `dim_proposicao`;
* `dim_tempo`.

### Chaves estrangeiras

| Campo                   | Dimensão         |
| ----------------------- | ---------------- |
| `sk_proposicao`         | `dim_proposicao` |
| `sk_tempo_apresentacao` | `dim_tempo`      |

### Métricas e atributos possíveis

| Campo               | Descrição                          |
| ------------------- | ---------------------------------- |
| `id_proposicao`     | Chave natural para rastreabilidade |
| `ano`               | Ano da proposição                  |
| `numero`            | Número da proposição               |
| `data_apresentacao` | Data de apresentação               |
| `status_proposicao` | Situação ou status                 |
| `flag_normativa`    | Indicador analítico                |
| `flag_social`       | Indicador analítico                |
| `flag_economico`    | Indicador analítico                |

### Análises possíveis

* total de proposições;
* proposições por ano;
* proposições por tipo;
* proposições por tema;
* proposições por natureza jurídica.

---

## `fato_autoria`

### Descrição

Fato que relaciona proposições e autores.

### Granularidade

Uma linha por relação entre proposição e autor.

### Fontes principais

* `gold.proposicoes_autores`;
* `dim_proposicao`;
* `dim_deputado`.

### Chaves estrangeiras

| Campo           | Dimensão         |
| --------------- | ---------------- |
| `sk_proposicao` | `dim_proposicao` |
| `sk_deputado`   | `dim_deputado`   |

### Atributos possíveis

| Campo              | Descrição                           |
| ------------------ | ----------------------------------- |
| `id_proposicao`    | Chave natural da proposição         |
| `id_deputado`      | Chave natural do deputado           |
| `tipo_autor`       | Tipo de autor, quando disponível    |
| `ordem_assinatura` | Ordem de autoria, quando disponível |

### Análises possíveis

* autores mais frequentes;
* proposições por deputado;
* proposições por partido;
* temas mais propostos por deputado;
* autoria individual ou coletiva.

---

## `fato_tramitacao`

### Descrição

Fato com movimentações e tramitações das proposições.

### Granularidade

Uma linha por tramitação ou movimentação.

### Fontes principais

* `gold.proposicoes_tramitacoes`;
* `dim_proposicao`;
* `dim_orgao`;
* `dim_tempo`.

### Chaves estrangeiras

| Campo                 | Dimensão         |
| --------------------- | ---------------- |
| `sk_proposicao`       | `dim_proposicao` |
| `sk_orgao`            | `dim_orgao`      |
| `sk_tempo_tramitacao` | `dim_tempo`      |

### Atributos possíveis

| Campo               | Descrição                   |
| ------------------- | --------------------------- |
| `id_proposicao`     | Chave natural da proposição |
| `data_tramitacao`   | Data da tramitação          |
| `sequencia`         | Ordem da tramitação         |
| `despacho`          | Descrição do despacho       |
| `situacao`          | Situação da tramitação      |
| `regime_tramitacao` | Regime, quando disponível   |

### Análises possíveis

* número de tramitações por proposição;
* tramitações por órgão;
* tramitações ao longo do tempo;
* tempo de movimentação legislativa;
* análise de fluxo legislativo.

---

## `fato_votacao`

### Descrição

Fato com votações relacionadas a proposições.

### Granularidade

Uma linha por votação.

### Fontes principais

* `gold.proposicoes_votacoes`;
* `dim_proposicao`;
* `dim_orgao`;
* `dim_tempo`.

### Chaves estrangeiras

| Campo              | Dimensão         |
| ------------------ | ---------------- |
| `sk_proposicao`    | `dim_proposicao` |
| `sk_orgao`         | `dim_orgao`      |
| `sk_tempo_votacao` | `dim_tempo`      |

### Atributos possíveis

| Campo               | Descrição                                 |
| ------------------- | ----------------------------------------- |
| `id_votacao`        | Chave natural da votação                  |
| `id_proposicao`     | Chave natural da proposição               |
| `data_votacao`      | Data da votação                           |
| `resultado`         | Resultado da votação                      |
| `descricao_votacao` | Descrição da votação                      |
| `aprovada`          | Indicador de aprovação, quando disponível |

### Análises possíveis

* votações por período;
* votações por proposição;
* votações por órgão;
* resultado de votações;
* relação entre tema e votação.

---

## `fato_voto`

### Descrição

Fato com votos individuais dos deputados em votações.

### Granularidade

Uma linha por voto de deputado em uma votação.

### Fontes principais

* `gold.votacoes_votos`;
* `dim_deputado`;
* `dim_partido`;
* `dim_proposicao`;
* `fato_votacao`, quando aplicável.

### Chaves estrangeiras

| Campo           | Dimensão         |
| --------------- | ---------------- |
| `sk_deputado`   | `dim_deputado`   |
| `sk_partido`    | `dim_partido`    |
| `sk_proposicao` | `dim_proposicao` |

### Atributos possíveis

| Campo                 | Descrição                                |
| --------------------- | ---------------------------------------- |
| `id_votacao`          | Chave natural da votação                 |
| `id_deputado`         | Chave natural do deputado                |
| `id_proposicao`       | Chave natural da proposição              |
| `voto`                | Voto do parlamentar                      |
| `orientacao_partido`  | Orientação partidária, quando disponível |
| `flag_voto_favoravel` | Indicador de voto favorável              |
| `flag_voto_contrario` | Indicador de voto contrário              |

### Análises possíveis

* votos por deputado;
* votos por partido;
* votos por tema;
* distribuição de votos;
* comportamento parlamentar;
* alinhamento partidário.

---

## `fato_evento`

### Descrição

Fato com eventos legislativos.

### Granularidade

Uma linha por evento.

### Fontes principais

* `gold.eventos`;
* `dim_evento`;
* `dim_orgao`;
* `dim_tempo`.

### Chaves estrangeiras

| Campo             | Dimensão     |
| ----------------- | ------------ |
| `sk_evento`       | `dim_evento` |
| `sk_orgao`        | `dim_orgao`  |
| `sk_tempo_evento` | `dim_tempo`  |

### Atributos possíveis

| Campo                   | Descrição                  |
| ----------------------- | -------------------------- |
| `id_evento`             | Chave natural do evento    |
| `data_evento`           | Data do evento             |
| `hora_inicio`           | Horário de início          |
| `hora_fim`              | Horário de fim             |
| `situacao_evento`       | Situação                   |
| `flag_evento_realizado` | Indicador se foi realizado |

### Análises possíveis

* eventos por período;
* eventos por órgão;
* eventos realizados;
* eventos por tipo;
* agenda legislativa.

---

## `fato_presenca`

### Descrição

Fato que relaciona deputados aos eventos legislativos.

### Granularidade

Uma linha por presença de deputado em evento.

### Fontes principais

* `gold.eventos_deputados`;
* `dim_evento`;
* `dim_deputado`.

### Chaves estrangeiras

| Campo         | Dimensão       |
| ------------- | -------------- |
| `sk_evento`   | `dim_evento`   |
| `sk_deputado` | `dim_deputado` |

### Atributos possíveis

| Campo               | Descrição                                |
| ------------------- | ---------------------------------------- |
| `id_evento`         | Chave natural do evento                  |
| `id_deputado`       | Chave natural do deputado                |
| `situacao_presenca` | Situação da presença, quando disponível  |
| `flag_presente`     | Indicador de presença, quando disponível |

### Análises possíveis

* presença por deputado;
* presença por evento;
* presença por partido;
* participação parlamentar;
* eventos com maior participação.


# Relacionamentos

O modelo dimensional segue relacionamentos um-para-muitos entre dimensões e fatos.

```text
dim_tempo       1 ─── * fato_proposicao
dim_tempo       1 ─── * fato_tramitacao
dim_tempo       1 ─── * fato_votacao
dim_tempo       1 ─── * fato_evento

dim_proposicao  1 ─── * fato_proposicao
dim_proposicao  1 ─── * fato_autoria
dim_proposicao  1 ─── * fato_tramitacao
dim_proposicao  1 ─── * fato_votacao
dim_proposicao  1 ─── * fato_voto

dim_deputado    1 ─── * fato_autoria
dim_deputado    1 ─── * fato_voto
dim_deputado    1 ─── * fato_presenca

dim_partido     1 ─── * fato_voto

dim_evento      1 ─── * fato_evento
dim_evento      1 ─── * fato_presenca

dim_orgao       1 ─── * fato_tramitacao
dim_orgao       1 ─── * fato_votacao
dim_orgao       1 ─── * fato_evento
```

# Diagrama Conceitual

```text
                         ┌──────────────┐
                         │  dim_tempo   │
                         └──────┬───────┘
                                │
                                │
┌────────────────┐      ┌───────▼────────┐      ┌────────────────┐
│ dim_deputado   │──────│ fato_autoria   │──────│ dim_proposicao │
└──────┬─────────┘      └────────────────┘      └──────┬─────────┘
       │                                                │
       │                                                │
       │              ┌────────────────┐                │
       └──────────────│  fato_voto     │────────────────┘
                      └───────┬────────┘
                              │
                       ┌──────▼───────┐
                       │ dim_partido  │
                       └──────────────┘


┌────────────────┐      ┌───────────────────┐      ┌──────────────┐
│ dim_proposicao │──────│ fato_tramitacao   │──────│ dim_orgao    │
└────────────────┘      └───────────────────┘      └──────┬───────┘
                                                           │
┌────────────────┐      ┌───────────────────┐              │
│ dim_proposicao │──────│ fato_votacao      │──────────────┘
└────────────────┘      └───────────────────┘


┌──────────────┐        ┌───────────────────┐       ┌──────────────┐
│ dim_evento   │────────│ fato_evento       │───────│ dim_orgao    │
└──────┬───────┘        └───────────────────┘       └──────────────┘
       │
       │
       │              ┌───────────────────┐       ┌────────────────┐
       └──────────────│ fato_presenca     │───────│ dim_deputado   │
                      └───────────────────┘       └────────────────┘
```


# Estratégia de Chaves

## Chaves naturais

As chaves naturais são os identificadores vindos da API da Câmara ou atributos únicos do domínio.

Exemplos:

| Entidade   | Chave natural   |
| ---------- | --------------- |
| Deputado   | `id_deputado`   |
| Partido    | `id_partido`    |
| Proposição | `id_proposicao` |
| Evento     | `id_evento`     |
| Órgão      | `orgao`         |
| Votação    | `id_votacao`    |


## Surrogate Keys

As surrogate keys são chaves substitutas usadas nas relações entre fatos e dimensões.

A estratégia recomendada é gerar surrogate keys determinísticas com hash das chaves naturais.

Exemplo conceitual:

```text
sk_deputado    = sha2(id_deputado)
sk_partido     = sha2(id_partido)
sk_proposicao  = sha2(id_proposicao)
sk_evento      = sha2(id_evento)
sk_orgao       = sha2(orgao)
```


## Benefícios de chaves determinísticas

* estabilidade entre reprocessamentos;
* joins consistentes entre fatos e dimensões;
* independência do particionamento Spark;
* melhor rastreabilidade;
* menor risco de quebra em cargas incrementais;
* melhor comportamento em reexecuções do pipeline.


# Granularidade das Tabelas

| Tabela            | Granularidade                     |
| ----------------- | --------------------------------- |
| `dim_tempo`       | Uma linha por data                |
| `dim_deputado`    | Uma linha por deputado            |
| `dim_partido`     | Uma linha por partido             |
| `dim_proposicao`  | Uma linha por proposição          |
| `dim_evento`      | Uma linha por evento              |
| `dim_orgao`       | Uma linha por órgão               |
| `fato_proposicao` | Uma linha por proposição          |
| `fato_autoria`    | Uma linha por autor de proposição |
| `fato_tramitacao` | Uma linha por tramitação          |
| `fato_votacao`    | Uma linha por votação             |
| `fato_voto`       | Uma linha por voto parlamentar    |
| `fato_evento`     | Uma linha por evento              |
| `fato_presenca`   | Uma linha por presença em evento  |


# Métricas e Indicadores Possíveis

## Proposições

* total de proposições;
* proposições por ano;
* proposições por tema;
* proposições por natureza jurídica;
* proposições por tipo documental;
* proposições por categoria regimental;
* proposições normativas;
* proposições sociais;
* proposições econômicas.

## Autoria

* total de proposições por deputado;
* total de proposições por partido;
* ranking de autores;
* temas mais propostos por deputado;
* autoria por UF;
* autoria por região.


## Tramitação

* quantidade de tramitações por proposição;
* tramitações por órgão;
* evolução temporal de tramitações;
* tempo entre movimentações;
* órgãos com maior volume de tramitação.

## Votações

* total de votações;
* votações por proposição;
* votações por órgão;
* votações por período;
* votações aprovadas/rejeitadas;
* votações por tema.


## Votos

* votos por deputado;
* votos por partido;
* votos por proposição;
* distribuição de votos;
* votos favoráveis;
* votos contrários;
* abstenções;
* comportamento por tema.


## Eventos

* total de eventos;
* eventos por tipo;
* eventos por órgão;
* eventos realizados;
* eventos por período;
* locais mais frequentes.

## Presença

* presença por deputado;
* presença por partido;
* presença por evento;
* eventos com maior participação;
* taxa de participação parlamentar.

# Serving para Power BI

A camada Star é publicada na camada Serving para consumo analítico.

```text
star.dim_deputado
star.dim_partido
star.dim_proposicao
star.dim_tempo
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
dados_abertos.star_schema
        ↓
Power BI
```

# Resumo

O Star Schema deste projeto organiza dados legislativos em dimensões e fatos para permitir análises claras e performáticas.

O modelo cobre os principais domínios do pipeline:

* proposições;
* deputados;
* partidos;
* órgãos;
* eventos;
* autores;
* tramitações;
* votações;
* votos;
* presença parlamentar.

