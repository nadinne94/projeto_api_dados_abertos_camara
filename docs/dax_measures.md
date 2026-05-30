# Medidas DAX do Dashboard

## Objetivo

Este documento registra as principais medidas DAX sugeridas para o dashboard Power BI do projeto `projeto_api_dados_abertos_camara`.

O objetivo é documentar a lógica analítica usada ou recomendada para explorar as tabelas finais publicadas na camada Serving, principalmente a partir do modelo dimensional em Star Schema.

As medidas ajudam a transformar tabelas fato e dimensão em indicadores de negócio para responder perguntas sobre proposições, deputados, partidos, temas, tramitações, votações, votos, eventos e presença parlamentar.

---

## Contexto

O dashboard Power BI representa a camada final de consumo analítico do projeto.

O modelo parte de tabelas dimensionais e fatos, como:

### Dimensões

- `dim_tempo`;
- `dim_deputado`;
- `dim_partido`;
- `dim_proposicao`;
- `dim_orgao`;
- `dim_evento`.

### Fatos

- `fato_proposicao`;
- `fato_autoria`;
- `fato_tramitacao`;
- `fato_votacao`;
- `fato_voto`;
- `fato_evento`;
- `fato_presenca`.

As medidas documentadas aqui funcionam como referência analítica e podem ser ajustadas conforme os nomes finais das tabelas e colunas no arquivo `.pbix`.

---

## Escopo

Este documento cobre:

- organização recomendada das medidas;
- medidas gerais;
- medidas de proposições;
- medidas de autoria;
- medidas de tramitação;
- medidas de votações;
- medidas de eventos e presença;
- medidas temporais;
- medidas de ranking;
- medidas de participação parlamentar;
- medidas de qualidade analítica;
- recomendações de formatação;
- recomendações de uso no dashboard;
- boas práticas para DAX;
- próximas evoluções.

Este documento não substitui o arquivo `.pbix`. Ele funciona como catálogo técnico e analítico das medidas sugeridas ou esperadas.

---

## Conteúdo Principal

### 1. Organização recomendada das medidas

No Power BI, recomenda-se organizar as medidas em pastas temáticas:

```text
00 - Medidas Gerais
01 - Proposições
02 - Autoria
03 - Tramitação
04 - Votações
05 - Eventos e Presença
06 - Participação Parlamentar
07 - Indicadores Temporais
08 - Qualidade Analítica
```

Também é recomendado criar uma tabela exclusiva para medidas, por exemplo:

```text
_medidas
```

### 2. Medidas gerais

#### Total de Proposições

```DAX
Total de Proposições =
DISTINCTCOUNT ( fato_proposicao[id_proposicao] )
```

#### Total de Deputados

```DAX
Total de Deputados =
DISTINCTCOUNT ( dim_deputado[id_deputado] )
```

#### Total de Partidos

```DAX
Total de Partidos =
DISTINCTCOUNT ( dim_partido[sigla_partido] )
```

#### Total de Órgãos

```DAX
Total de Órgãos =
DISTINCTCOUNT ( dim_orgao[id_orgao] )
```

### 3. Medidas de proposições

#### Proposições por Tema

```DAX
Proposições por Tema =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[tema_ementa]`;
- valor: `[Proposições por Tema]`.

#### Proposições por Natureza Jurídica

```DAX
Proposições por Natureza Jurídica =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[natureza_juridica]`;
- valor: `[Proposições por Natureza Jurídica]`.

#### Proposições por Ano

```DAX
Proposições por Ano =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_tempo[ano]`;
- valor: `[Proposições por Ano]`.

#### Proposições com Tema Classificado

```DAX
Proposições com Tema Classificado =
CALCULATE (
    [Total de Proposições],
    NOT ISBLANK ( dim_proposicao[tema_ementa] ),
    dim_proposicao[tema_ementa] <> "Tema Não Explícito"
)
```

#### Proposições sem Tema Explícito

```DAX
Proposições sem Tema Explícito =
CALCULATE (
    [Total de Proposições],
    dim_proposicao[tema_ementa] = "Tema Não Explícito"
)
```

#### Percentual de Proposições Classificadas

```DAX
% Proposições Classificadas =
DIVIDE (
    [Proposições com Tema Classificado],
    [Total de Proposições]
)
```

#### Proposições por Tipo

```DAX
Proposições por Tipo =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[sigla_tipo]`;
- valor: `[Proposições por Tipo]`.

### 4. Medidas de autoria

#### Total de Autorias

```DAX
Total de Autorias =
COUNTROWS ( fato_autoria )
```

#### Deputados Autores

```DAX
Deputados Autores =
DISTINCTCOUNT ( fato_autoria[sk_deputado] )
```

#### Média de Autores por Proposição

```DAX
Média de Autores por Proposição =
DIVIDE (
    [Total de Autorias],
    [Total de Proposições]
)
```

#### Proposições por Partido do Autor

```DAX
Proposições por Partido do Autor =
DISTINCTCOUNT ( fato_autoria[id_proposicao] )
```

Uso recomendado:

- eixo: `dim_partido[sigla_partido]`;
- valor: `[Proposições por Partido do Autor]`.

### 5. Medidas de tramitação

#### Total de Tramitações

```DAX
Total de Tramitações =
COUNTROWS ( fato_tramitacao )
```

#### Proposições com Tramitação

```DAX
Proposições com Tramitação =
DISTINCTCOUNT ( fato_tramitacao[id_proposicao] )
```

#### Média de Tramitações por Proposição

```DAX
Média de Tramitações por Proposição =
DIVIDE (
    [Total de Tramitações],
    [Proposições com Tramitação]
)
```

#### Tramitações por Órgão

```DAX
Tramitações por Órgão =
[Total de Tramitações]
```

Uso recomendado:

- eixo: `dim_orgao[sigla_orgao]` ou `dim_orgao[nome_orgao]`;
- valor: `[Tramitações por Órgão]`.

### 6. Medidas de votações

#### Total de Votações

```DAX
Total de Votações =
DISTINCTCOUNT ( fato_votacao[id_votacao] )
```

#### Total de Votos

```DAX
Total de Votos =
COUNTROWS ( fato_voto )
```

#### Deputados Votantes

```DAX
Deputados Votantes =
DISTINCTCOUNT ( fato_voto[sk_deputado] )
```

#### Votos Sim

```DAX
Votos Sim =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Sim"
)
```

#### Votos Não

```DAX
Votos Não =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Não"
)
```

#### Abstenções

```DAX
Abstenções =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Abstenção"
)
```

#### Percentual de Votos Sim

```DAX
% Votos Sim =
DIVIDE (
    [Votos Sim],
    [Total de Votos]
)
```

#### Percentual de Votos Não

```DAX
% Votos Não =
DIVIDE (
    [Votos Não],
    [Total de Votos]
)
```

### 7. Medidas de eventos e presença

#### Total de Eventos

```DAX
Total de Eventos =
DISTINCTCOUNT ( fato_evento[id_evento] )
```

#### Total de Presenças

```DAX
Total de Presenças =
COUNTROWS ( fato_presenca )
```

#### Deputados Presentes

```DAX
Deputados Presentes =
DISTINCTCOUNT ( fato_presenca[sk_deputado] )
```

#### Média de Presenças por Evento

```DAX
Média de Presenças por Evento =
DIVIDE (
    [Total de Presenças],
    [Total de Eventos]
)
```

#### Eventos por Órgão

```DAX
Eventos por Órgão =
[Total de Eventos]
```

Uso recomendado:

- eixo: `dim_orgao[nome_orgao]`;
- valor: `[Eventos por Órgão]`.

### 8. Medidas temporais

#### Proposições no Ano Atual

```DAX
Proposições Ano Atual =
CALCULATE (
    [Total de Proposições],
    dim_tempo[ano] = YEAR ( TODAY() )
)
```

#### Proposições no Ano Anterior

```DAX
Proposições Ano Anterior =
CALCULATE (
    [Total de Proposições],
    dim_tempo[ano] = YEAR ( TODAY() ) - 1
)
```

#### Variação de Proposições Ano contra Ano

```DAX
Variação Proposições YoY =
[Proposições Ano Atual] - [Proposições Ano Anterior]
```

#### Percentual de Variação Ano contra Ano

```DAX
% Variação Proposições YoY =
DIVIDE (
    [Variação Proposições YoY],
    [Proposições Ano Anterior]
)
```

#### Proposições Acumuladas

```DAX
Proposições Acumuladas =
CALCULATE (
    [Total de Proposições],
    FILTER (
        ALLSELECTED ( dim_tempo[data] ),
        dim_tempo[data] <= MAX ( dim_tempo[data] )
    )
)
```

### 9. Medidas de ranking

#### Ranking de Temas

```DAX
Ranking de Temas =
RANKX (
    ALLSELECTED ( dim_proposicao[tema_ementa] ),
    [Total de Proposições],
    ,
    DESC,
    DENSE
)
```

#### Ranking de Partidos por Proposição

```DAX
Ranking de Partidos por Proposição =
RANKX (
    ALLSELECTED ( dim_partido[sigla_partido] ),
    [Proposições por Partido do Autor],
    ,
    DESC,
    DENSE
)
```

#### Ranking de Deputados Autores

```DAX
Ranking de Deputados Autores =
RANKX (
    ALLSELECTED ( dim_deputado[nome_deputado] ),
    [Total de Autorias],
    ,
    DESC,
    DENSE
)
```

### 10. Medidas de participação parlamentar

#### Taxa de Participação em Eventos

```DAX
Taxa de Participação em Eventos =
DIVIDE (
    [Total de Presenças],
    [Total de Eventos]
)
```

Observação: esta medida representa a média geral de presenças registradas por evento no contexto filtrado. Para uma taxa individual por parlamentar, é necessário ajustar o denominador conforme a regra de negócio definida no dashboard.

#### Participações por Deputado

```DAX
Participações por Deputado =
COUNTROWS ( fato_presenca )
```

Uso recomendado:

- eixo: `dim_deputado[nome_deputado]`;
- valor: `[Participações por Deputado]`.

#### Votos por Deputado

```DAX
Votos por Deputado =
COUNTROWS ( fato_voto )
```

Uso recomendado:

- eixo: `dim_deputado[nome_deputado]`;
- valor: `[Votos por Deputado]`.

### 11. Medidas de qualidade analítica

#### Proposições sem Classificação

```DAX
Proposições sem Classificação =
CALCULATE (
    [Total de Proposições],
    ISBLANK ( dim_proposicao[tema_ementa] )
        || dim_proposicao[tema_ementa] = "Tema Não Explícito"
)
```

#### Percentual sem Classificação

```DAX
% Sem Classificação =
DIVIDE (
    [Proposições sem Classificação],
    [Total de Proposições]
)
```

#### Registros com Natureza Jurídica

```DAX
Registros com Natureza Jurídica =
CALCULATE (
    [Total de Proposições],
    NOT ISBLANK ( dim_proposicao[natureza_juridica] )
)
```

#### Percentual com Natureza Jurídica

```DAX
% com Natureza Jurídica =
DIVIDE (
    [Registros com Natureza Jurídica],
    [Total de Proposições]
)
```

### 12. Recomendações de formatação

| Tipo de medida | Formato recomendado |
|---|---|
| Contagens | Número inteiro com separador de milhar. |
| Percentuais | Percentual com 1 ou 2 casas decimais. |
| Médias | Número decimal com 1 ou 2 casas decimais. |
| Rankings | Número inteiro. |
| Variações | Número inteiro ou percentual, conforme o caso. |

### 13. Recomendações de uso no dashboard

#### Página de visão geral

Medidas recomendadas:

- `[Total de Proposições]`;
- `[Total de Deputados]`;
- `[Total de Partidos]`;
- `[Total de Votações]`;
- `[Total de Eventos]`.

#### Página de proposições

Medidas recomendadas:

- `[Total de Proposições]`;
- `[Proposições por Tema]`;
- `[Proposições por Natureza Jurídica]`;
- `[% Proposições Classificadas]`;
- `[Ranking de Temas]`.

#### Página de deputados e partidos

Medidas recomendadas:

- `[Deputados Autores]`;
- `[Total de Autorias]`;
- `[Proposições por Partido do Autor]`;
- `[Ranking de Deputados Autores]`;
- `[Ranking de Partidos por Proposição]`.

#### Página de votações

Medidas recomendadas:

- `[Total de Votações]`;
- `[Total de Votos]`;
- `[Votos Sim]`;
- `[Votos Não]`;
- `[% Votos Sim]`;
- `[% Votos Não]`.

#### Página de eventos

Medidas recomendadas:

- `[Total de Eventos]`;
- `[Total de Presenças]`;
- `[Média de Presenças por Evento]`;
- `[Eventos por Órgão]`;
- `[Participações por Deputado]`.

### 14. Boas práticas para medidas DAX

Boas práticas recomendadas:

- usar nomes claros e orientados ao negócio;
- evitar medidas com lógica duplicada;
- criar medidas base e reutilizá-las em medidas derivadas;
- usar `DIVIDE()` em vez de operador `/` para evitar erro de divisão por zero;
- padronizar prefixos de percentuais com `%`;
- separar medidas por pastas no Power BI;
- documentar medidas críticas neste arquivo;
- revisar nomes de colunas caso o schema final seja alterado.

### 15. Cuidados e limitações

Pontos de atenção:

- algumas medidas dependem dos nomes finais das tabelas e colunas no Power BI;
- medidas temporais podem precisar de uma tabela calendário marcada como tabela de datas;
- rankings dependem do contexto de filtro do relatório;
- medidas de participação parlamentar podem exigir regra de negócio específica para o denominador;
- medidas documentadas aqui são referência e podem ser ajustadas no `.pbix`.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para as medidas analíticas do dashboard Power BI.

Ele se conecta diretamente a:

- `README.md`, que apresenta Power BI, DAX e Power Query como tecnologias utilizadas;
- `docs/dashboard.md`, que descreve as páginas e objetivos do dashboard;
- `docs/star_schema.md`, que define as tabelas fato e dimensão usadas nas medidas;
- `docs/data_quality.md`, que garante confiabilidade dos dados usados nos indicadores;
- `docs/data_contracts.md`, que documenta colunas e regras esperadas;
- `docs/lineage.md`, que mostra a origem das tabelas consumidas no Power BI.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Dashboard Power BI](dashboard.md)
- [Modelo Star Schema](star_schema.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Linhagem dos Dados](lineage.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções deste documento:

- adicionar medidas reais exportadas do arquivo `.pbix`;
- documentar relacionamento entre medidas e páginas do dashboard;
- criar tabela de calendário oficial no modelo Power BI;
- incluir medidas de tendência mensal e anual;
- criar indicadores específicos por tema legislativo;
- documentar cálculo de KPIs estratégicos;
- versionar medidas alteradas em futuras versões do dashboard;
- adicionar exemplos visuais de uso de cada medida.
