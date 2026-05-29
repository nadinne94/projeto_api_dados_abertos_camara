# Dashboard Power BI

O dashboard Power BI é a camada final de consumo analítico do projeto.

Ele utiliza as tabelas publicadas na camada Serving, construídas a partir do Star Schema do pipeline.

## Objetivo

O objetivo do dashboard é permitir a exploração dos dados legislativos processados pelo pipeline, facilitando análises sobre proposições, partidos, deputados, votações, votos, tramitações e eventos.

## Fonte dos Dados

O dashboard consome as tabelas finais publicadas no schema:

```text
api_dados_abertos.star_schema
````

Essas tabelas são geradas pela camada Star Schema e publicadas pela camada Serving.

## Modelo Analítico

O dashboard utiliza dimensões e fatos do modelo dimensional.

### Dimensões

* `dim_tempo`
* `dim_deputado`
* `dim_partido`
* `dim_proposicao`
* `dim_evento`
* `dim_orgao`

### Fatos

* `fato_proposicao`
* `fato_autoria`
* `fato_tramitacao`
* `fato_votacao`
* `fato_voto`
* `fato_evento`
* `fato_presenca`

## Análises Disponíveis

O dashboard permite análises como:

* proposições por tema;
* proposições por ano;
* proposições por partido;
* autores mais frequentes;
* tramitações por órgão;
* votações por proposição;
* votos por deputado;
* votos por partido;
* eventos legislativos;
* presença parlamentar em eventos.

## Relação com o Pipeline

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

O Power BI representa a última etapa do projeto, consumindo os dados já tratados, enriquecidos e modelados para análise.

## Link do Dashboard

[🔗 Acessar Dashboard Power BI](https://app.powerbi.com/view?r=eyJrIjoiZGIxYTA5MTMtZjIxNy00ZTlkLWJlMjEtMWZmODA1NTlhZWRmIiwidCI6Ijk2NDEzODNiLWQ0N2MtNDQyMy05OTA4LTU5MGYyYTRmNzgwZCJ9)



<img width="1436" height="820" alt="image" src="https://github.com/user-attachments/assets/271653fb-bb90-4492-aba0-71567c4d766a" />
