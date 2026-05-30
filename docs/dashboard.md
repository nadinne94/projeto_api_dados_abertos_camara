# Dashboard Power BI

## Objetivo

Este documento descreve o dashboard Power BI do projeto `projeto_api_dados_abertos_camara`.

O objetivo do dashboard é permitir a exploração dos dados legislativos processados pelo pipeline, facilitando análises sobre proposições, partidos, deputados, votações, votos, tramitações, órgãos e eventos.

O Power BI representa a camada final de consumo analítico do projeto, utilizando tabelas publicadas pela camada Serving a partir do modelo Star Schema.

---

## Contexto

O projeto transforma dados públicos da Câmara dos Deputados em tabelas analíticas estruturadas. Depois da ingestão, tratamento, enriquecimento e modelagem dimensional, os dados são disponibilizados para visualização no Power BI.

Fluxo conceitual:

```text
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

O dashboard permite transformar o pipeline técnico em uma entrega visual e analítica, demonstrando o valor dos dados processados.

---

## Escopo

Este documento cobre:

- objetivo analítico do dashboard;
- fonte dos dados;
- modelo analítico utilizado;
- dimensões e fatos consumidos;
- principais análises disponíveis;
- possíveis páginas do dashboard;
- indicadores e medidas recomendadas;
- relação com o pipeline;
- link do dashboard publicado;
- imagem de referência;
- próximas evoluções.

Este documento não detalha todas as medidas DAX individualmente. As medidas estão documentadas em `docs/dax_measures.md`.

---

## Conteúdo Principal

### 1. Fonte dos dados

O dashboard consome as tabelas finais publicadas na camada Serving, derivadas do Star Schema do projeto.

Schema de referência:

```text
api_dados_abertos.star_schema
```

Essas tabelas são geradas a partir da camada Gold, organizadas na camada Star Schema e publicadas para consumo analítico.

### 2. Modelo analítico

O dashboard utiliza dimensões e fatos do modelo dimensional.

#### Dimensões

- `dim_tempo`;
- `dim_deputado`;
- `dim_partido`;
- `dim_proposicao`;
- `dim_evento`;
- `dim_orgao`.

#### Fatos

- `fato_proposicao`;
- `fato_autoria`;
- `fato_tramitacao`;
- `fato_votacao`;
- `fato_voto`;
- `fato_evento`;
- `fato_presenca`.

### 3. Objetivo analítico

O dashboard foi pensado para responder perguntas como:

- Quais temas legislativos aparecem com maior frequência?
- Como as proposições evoluem ao longo do tempo?
- Quais partidos e deputados aparecem mais associados às proposições?
- Como as proposições tramitam entre órgãos?
- Como se distribuem votações e votos parlamentares?
- Quais órgãos concentram eventos legislativos?
- Como ocorre a participação parlamentar em eventos?

### 4. Análises disponíveis

O dashboard permite análises como:

- proposições por tema;
- proposições por ano;
- proposições por partido;
- autores mais frequentes;
- tramitações por órgão;
- votações por proposição;
- votos por deputado;
- votos por partido;
- eventos legislativos;
- presença parlamentar em eventos;
- comparação entre períodos;
- comparação entre partidos, UF e parlamentares.

### 5. Páginas recomendadas do dashboard

Uma organização recomendada para o dashboard é:

| Página | Objetivo |
|---|---|
| Visão Geral | Apresentar KPIs principais e visão executiva dos dados legislativos. |
| Proposições | Analisar proposições por tema, tipo, natureza jurídica, ano e partido. |
| Deputados e Partidos | Explorar autoria, participação e distribuição por parlamentar ou legenda. |
| Tramitações | Avaliar movimentações, órgãos envolvidos e evolução do processo legislativo. |
| Votações e Votos | Analisar votações, votos parlamentares e comportamento por partido. |
| Eventos e Presença | Explorar eventos legislativos e participação parlamentar. |
| Metodologia | Explicar fonte dos dados, pipeline, Star Schema e limitações. |

### 6. Indicadores recomendados

Indicadores principais:

- total de proposições;
- total de deputados;
- total de partidos;
- total de votações;
- total de votos;
- total de eventos;
- total de presenças;
- percentual de proposições classificadas;
- proposições por tema;
- proposições por natureza jurídica;
- deputados autores;
- votos por partido;
- presença por deputado.

As medidas DAX recomendadas estão documentadas em [Medidas DAX](dax_measures.md).

### 7. Relação com o pipeline

O dashboard é a última etapa do projeto.

```text
API Câmara
   ↓
Bronze
   ↓
Silver
   ↓
ML/NLP
   ↓
Gold
   ↓
Star Schema
   ↓
Serving SQL
   ↓
Power BI
```

Cada visual do dashboard deve consumir preferencialmente as tabelas finais da camada Serving, evitando dependência direta das camadas intermediárias.

### 8. Link do dashboard

[🔗 Acessar Dashboard Power BI](https://app.powerbi.com/view?r=eyJrIjoiZGIxYTA5MTMtZjIxNy00ZTlkLWJlMjEtMWZmODA1NTlhZWRmIiwidCI6Ijk2NDEzODNiLWQ0N2MtNDQyMy05OTA4LTU5MGYyYTRmNzgwZCJ9)

### 9. Imagem de referência

Imagem atual do dashboard:

<img width="1436" height="820" alt="Dashboard Power BI" src="https://github.com/user-attachments/assets/271653fb-bb90-4492-aba0-71567c4d766a" />

Para exibição direta no README, recomenda-se salvar uma imagem do dashboard em:

```text
docs/images/dashboard-preview.png
```

### 10. Boas práticas para manutenção

Boas práticas recomendadas:

- consumir tabelas da camada Serving;
- evitar lógica excessiva no Power BI quando ela puder ser tratada no pipeline;
- documentar medidas DAX relevantes;
- manter nomes de medidas claros e orientados ao negócio;
- separar páginas por tema analítico;
- incluir página de metodologia;
- revisar relacionamentos e cardinalidade no modelo Power BI;
- atualizar o print do dashboard sempre que houver mudança visual relevante.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para o consumo analítico em Power BI.

Ele se conecta diretamente a:

- `README.md`, que apresenta o dashboard como resultado final do projeto;
- `docs/architecture.md`, que posiciona Power BI como camada final da arquitetura;
- `docs/star_schema.md`, que descreve as dimensões e fatos consumidos;
- `docs/dax_measures.md`, que documenta medidas analíticas;
- `docs/execution_guide.md`, que explica como publicar as tabelas finais na camada Serving;
- `docs/lineage.md`, que mostra a origem dos dados consumidos pelo dashboard.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Modelo Star Schema](star_schema.md)
- [Medidas DAX](dax_measures.md)
- [Linhagem dos Dados](lineage.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções do dashboard:

- adicionar página de metodologia;
- documentar todas as medidas DAX reais usadas no arquivo `.pbix`;
- incluir análise por legislatura;
- ampliar comparações entre partidos, UF e deputados;
- criar indicadores de participação parlamentar;
- criar análise de comportamento de votação;
- adicionar visão temporal por legislaturas antigas;
- revisar storytelling visual;
- adicionar imagem versionada do dashboard em `docs/images/dashboard-preview.png`;
- criar documentação das páginas finais do dashboard.
