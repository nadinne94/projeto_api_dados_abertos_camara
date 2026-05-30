# Medidas DAX do Dashboard

Este documento registra as principais medidas DAX sugeridas para o dashboard Power BI do projeto `projeto_api_dados_abertos_camara`.

O objetivo é documentar a lógica analítica usada ou recomendada para explorar as tabelas finais publicadas na camada Serving, principalmente a partir do modelo dimensional em Star Schema.

---

## 1. Objetivo

As medidas DAX ajudam a transformar as tabelas fato e dimensão em indicadores analíticos para responder perguntas sobre proposições, votações, deputados, partidos, temas, tramitações e eventos legislativos.

Este documento serve como referência para:

- manutenção do dashboard;
- padronização das medidas;
- explicação da lógica analítica;
- documentação para portfólio;
- evolução futura do modelo Power BI.

---

## 2. Premissas do modelo

As medidas abaixo assumem um modelo dimensional com tabelas como:

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

Os nomes das colunas podem ser ajustados conforme o modelo final publicado no Power BI.

---

## 3. Organização recomendada das medidas

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
```

Também é recomendado criar uma tabela exclusiva para medidas, por exemplo:

```text
_medidas
```

---

# 4. Medidas gerais

## 4.1 Total de Proposições

Conta o total de proposições no contexto selecionado.

```DAX
Total de Proposições =
DISTINCTCOUNT ( fato_proposicao[id_proposicao] )
```

---

## 4.2 Total de Deputados

Conta o total de deputados distintos no modelo.

```DAX
Total de Deputados =
DISTINCTCOUNT ( dim_deputado[id_deputado] )
```

---

## 4.3 Total de Partidos

Conta o total de partidos distintos.

```DAX
Total de Partidos =
DISTINCTCOUNT ( dim_partido[sigla_partido] )
```

---

## 4.4 Total de Órgãos

Conta o total de órgãos legislativos cadastrados no modelo.

```DAX
Total de Órgãos =
DISTINCTCOUNT ( dim_orgao[id_orgao] )
```

---

# 5. Medidas de proposições

## 5.1 Proposições por Tema

A medida base pode ser usada em visuais segmentados por `tema_ementa`.

```DAX
Proposições por Tema =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[tema_ementa]`;
- valor: `[Proposições por Tema]`.

---

## 5.2 Proposições por Natureza Jurídica

```DAX
Proposições por Natureza Jurídica =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[natureza_juridica]`;
- valor: `[Proposições por Natureza Jurídica]`.

---

## 5.3 Proposições por Ano

```DAX
Proposições por Ano =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_tempo[ano]`;
- valor: `[Proposições por Ano]`.

---

## 5.4 Proposições com Tema Classificado

Conta proposições que possuem tema diferente de nulo e diferente de fallback genérico.

```DAX
Proposições com Tema Classificado =
CALCULATE (
    [Total de Proposições],
    NOT ISBLANK ( dim_proposicao[tema_ementa] ),
    dim_proposicao[tema_ementa] <> "Tema Não Explícito"
)
```

---

## 5.5 Proposições sem Tema Explícito

```DAX
Proposições sem Tema Explícito =
CALCULATE (
    [Total de Proposições],
    dim_proposicao[tema_ementa] = "Tema Não Explícito"
)
```

---

## 5.6 Percentual de Proposições Classificadas

```DAX
% Proposições Classificadas =
DIVIDE (
    [Proposições com Tema Classificado],
    [Total de Proposições]
)
```

Formato recomendado:

```text
Percentual
```

---

## 5.7 Proposições por Tipo

```DAX
Proposições por Tipo =
[Total de Proposições]
```

Uso recomendado:

- eixo: `dim_proposicao[sigla_tipo]`;
- valor: `[Proposições por Tipo]`.

---

# 6. Medidas de autoria

## 6.1 Total de Autorias

Conta relações entre autores e proposições.

```DAX
Total de Autorias =
COUNTROWS ( fato_autoria )
```

---

## 6.2 Deputados Autores

Conta deputados distintos associados a autoria de proposições.

```DAX
Deputados Autores =
DISTINCTCOUNT ( fato_autoria[sk_deputado] )
```

---

## 6.3 Média de Autores por Proposição

```DAX
Média de Autores por Proposição =
DIVIDE (
    [Total de Autorias],
    [Total de Proposições]
)
```

---

## 6.4 Proposições por Partido do Autor

```DAX
Proposições por Partido do Autor =
DISTINCTCOUNT ( fato_autoria[id_proposicao] )
```

Uso recomendado:

- eixo: `dim_partido[sigla_partido]`;
- valor: `[Proposições por Partido do Autor]`.

---

# 7. Medidas de tramitação

## 7.1 Total de Tramitações

```DAX
Total de Tramitações =
COUNTROWS ( fato_tramitacao )
```

---

## 7.2 Proposições com Tramitação

```DAX
Proposições com Tramitação =
DISTINCTCOUNT ( fato_tramitacao[id_proposicao] )
```

---

## 7.3 Média de Tramitações por Proposição

```DAX
Média de Tramitações por Proposição =
DIVIDE (
    [Total de Tramitações],
    [Proposições com Tramitação]
)
```

---

## 7.4 Tramitações por Órgão

```DAX
Tramitações por Órgão =
[Total de Tramitações]
```

Uso recomendado:

- eixo: `dim_orgao[sigla_orgao]` ou `dim_orgao[nome_orgao]`;
- valor: `[Tramitações por Órgão]`.

---

# 8. Medidas de votações

## 8.1 Total de Votações

```DAX
Total de Votações =
DISTINCTCOUNT ( fato_votacao[id_votacao] )
```

---

## 8.2 Total de Votos

```DAX
Total de Votos =
COUNTROWS ( fato_voto )
```

---

## 8.3 Deputados Votantes

```DAX
Deputados Votantes =
DISTINCTCOUNT ( fato_voto[sk_deputado] )
```

---

## 8.4 Votos Sim

```DAX
Votos Sim =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Sim"
)
```

---

## 8.5 Votos Não

```DAX
Votos Não =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Não"
)
```

---

## 8.6 Abstenções

```DAX
Abstenções =
CALCULATE (
    [Total de Votos],
    fato_voto[voto] = "Abstenção"
)
```

---

## 8.7 Percentual de Votos Sim

```DAX
% Votos Sim =
DIVIDE (
    [Votos Sim],
    [Total de Votos]
)
```

---

## 8.8 Percentual de Votos Não

```DAX
% Votos Não =
DIVIDE (
    [Votos Não],
    [Total de Votos]
)
```

---

# 9. Medidas de eventos e presença

## 9.1 Total de Eventos

```DAX
Total de Eventos =
DISTINCTCOUNT ( fato_evento[id_evento] )
```

---

## 9.2 Total de Presenças

```DAX
Total de Presenças =
COUNTROWS ( fato_presenca )
```

---

## 9.3 Deputados Presentes

```DAX
Deputados Presentes =
DISTINCTCOUNT ( fato_presenca[sk_deputado] )
```

---

## 9.4 Média de Presenças por Evento

```DAX
Média de Presenças por Evento =
DIVIDE (
    [Total de Presenças],
    [Total de Eventos]
)
```

---

## 9.5 Eventos por Órgão

```DAX
Eventos por Órgão =
[Total de Eventos]
```

Uso recomendado:

- eixo: `dim_orgao[nome_orgao]`;
- valor: `[Eventos por Órgão]`.

---

# 10. Medidas temporais

## 10.1 Proposições no Ano Atual

```DAX
Proposições Ano Atual =
CALCULATE (
    [Total de Proposições],
    dim_tempo[ano] = YEAR ( TODAY() )
)
```

---

## 10.2 Proposições no Ano Anterior

```DAX
Proposições Ano Anterior =
CALCULATE (
    [Total de Proposições],
    dim_tempo[ano] = YEAR ( TODAY() ) - 1
)
```

---

## 10.3 Variação de Proposições Ano contra Ano

```DAX
Variação Proposições YoY =
[Proposições Ano Atual] - [Proposições Ano Anterior]
```

---

## 10.4 Percentual de Variação Ano contra Ano

```DAX
% Variação Proposições YoY =
DIVIDE (
    [Variação Proposições YoY],
    [Proposições Ano Anterior]
)
```

---

## 10.5 Proposições Acumuladas

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

---

# 11. Medidas de ranking

## 11.1 Ranking de Temas

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

---

## 11.2 Ranking de Partidos por Proposição

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

---

## 11.3 Ranking de Deputados Autores

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

---

# 12. Medidas de participação parlamentar

## 12.1 Taxa de Participação em Eventos

```DAX
Taxa de Participação em Eventos =
DIVIDE (
    [Total de Presenças],
    [Total de Eventos]
)
```

Observação: esta medida representa a média geral de presenças registradas por evento no contexto filtrado. Para uma taxa individual por parlamentar, é necessário ajustar o denominador conforme a regra de negócio definida no dashboard.

---

## 12.2 Participações por Deputado

```DAX
Participações por Deputado =
COUNTROWS ( fato_presenca )
```

Uso recomendado:

- eixo: `dim_deputado[nome_deputado]`;
- valor: `[Participações por Deputado]`.

---

## 12.3 Votos por Deputado

```DAX
Votos por Deputado =
COUNTROWS ( fato_voto )
```

Uso recomendado:

- eixo: `dim_deputado[nome_deputado]`;
- valor: `[Votos por Deputado]`.

---

# 13. Medidas de qualidade analítica

## 13.1 Proposições sem Classificação

```DAX
Proposições sem Classificação =
CALCULATE (
    [Total de Proposições],
    ISBLANK ( dim_proposicao[tema_ementa] )
        || dim_proposicao[tema_ementa] = "Tema Não Explícito"
)
```

---

## 13.2 Percentual sem Classificação

```DAX
% Sem Classificação =
DIVIDE (
    [Proposições sem Classificação],
    [Total de Proposições]
)
```

---

## 13.3 Registros com Natureza Jurídica

```DAX
Registros com Natureza Jurídica =
CALCULATE (
    [Total de Proposições],
    NOT ISBLANK ( dim_proposicao[natureza_juridica] )
)
```

---

## 13.4 Percentual com Natureza Jurídica

```DAX
% com Natureza Jurídica =
DIVIDE (
    [Registros com Natureza Jurídica],
    [Total de Proposições]
)
```

---

# 14. Recomendações de formatação

| Tipo de medida | Formato recomendado |
|---|---|
| Contagens | Número inteiro com separador de milhar |
| Percentuais | Percentual com 1 ou 2 casas decimais |
| Médias | Número decimal com 1 ou 2 casas decimais |
| Rankings | Número inteiro |
| Variações | Número inteiro ou percentual, conforme o caso |

---

# 15. Recomendações de uso no dashboard

## Página de visão geral

Medidas recomendadas:

- `[Total de Proposições]`;
- `[Total de Deputados]`;
- `[Total de Partidos]`;
- `[Total de Votações]`;
- `[Total de Eventos]`.

---

## Página de proposições

Medidas recomendadas:

- `[Total de Proposições]`;
- `[Proposições por Tema]`;
- `[Proposições por Natureza Jurídica]`;
- `[% Proposições Classificadas]`;
- `[Ranking de Temas]`.

---

## Página de deputados e partidos

Medidas recomendadas:

- `[Deputados Autores]`;
- `[Total de Autorias]`;
- `[Proposições por Partido do Autor]`;
- `[Ranking de Deputados Autores]`;
- `[Ranking de Partidos por Proposição]`.

---

## Página de votações

Medidas recomendadas:

- `[Total de Votações]`;
- `[Total de Votos]`;
- `[Votos Sim]`;
- `[Votos Não]`;
- `[% Votos Sim]`;
- `[% Votos Não]`.

---

## Página de eventos

Medidas recomendadas:

- `[Total de Eventos]`;
- `[Total de Presenças]`;
- `[Média de Presenças por Evento]`;
- `[Eventos por Órgão]`;
- `[Participações por Deputado]`.

---

# 16. Boas práticas para medidas DAX

- Usar nomes claros e orientados ao negócio.
- Evitar medidas com lógica duplicada.
- Criar medidas base e reutilizá-las em medidas derivadas.
- Usar `DIVIDE()` em vez de operador `/` para evitar erro de divisão por zero.
- Padronizar prefixos de percentuais com `%`.
- Separar medidas por pastas no Power BI.
- Documentar medidas críticas neste arquivo.
- Revisar nomes de colunas caso o schema final seja alterado.

---

# 17. Próximas evoluções

Possíveis melhorias futuras:

- adicionar medidas reais exportadas do arquivo `.pbix`;
- documentar relacionamento entre medidas e páginas do dashboard;
- criar tabela de calendário oficial no modelo Power BI;
- incluir medidas de tendência mensal e anual;
- criar indicadores específicos por tema legislativo;
- documentar cálculo de KPIs estratégicos;
- versionar medidas alteradas em futuras versões do dashboard.

---

# 18. Conclusão

As medidas DAX documentadas neste arquivo servem como base para padronizar a análise no Power BI e facilitar a manutenção do dashboard.

Mesmo quando uma medida precisar ser ajustada ao nome final das colunas, este documento registra a lógica analítica esperada para o projeto e fortalece a documentação do portfólio.
