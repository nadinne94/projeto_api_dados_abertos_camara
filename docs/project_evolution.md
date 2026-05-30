# Evolução do Projeto

## Objetivo

Este documento registra as limitações atuais, oportunidades de melhoria e próximos passos do projeto `projeto_api_dados_abertos_camara`.

O objetivo é deixar claro que o projeto já possui uma arquitetura funcional para portfólio, mas também apresenta possibilidades reais de evolução técnica, aproximando-o de um cenário mais produtivo de Engenharia de Dados.

---

## Contexto

O projeto implementa um pipeline de dados com dados públicos da Câmara dos Deputados, utilizando:

- ingestão de dados via API pública;
- arquitetura medalhão;
- processamento com PySpark;
- armazenamento em Delta Lake;
- camadas Bronze, Silver e Gold;
- classificação textual com regras e ML/NLP;
- modelo dimensional em Star Schema;
- camada de Serving;
- consumo analítico em Power BI;
- validações de qualidade de dados;
- contratos de dados;
- documentação técnica na pasta `docs/`.

Essa estrutura demonstra uma visão ponta a ponta de um projeto de dados, desde a coleta até a disponibilização para análise.

As evoluções descritas neste documento não indicam que o projeto está incompleto. Elas mostram maturidade técnica ao reconhecer limitações, propor melhorias e indicar caminhos para aproximar o projeto de uma solução produtiva.

---

## Escopo

Este documento cobre:

- limitações atuais;
- melhorias futuras de Engenharia de Dados;
- melhorias futuras de Analytics e BI;
- evolução da camada ML/NLP;
- evolução de Data Quality e contratos;
- evolução do modelo dimensional;
- evolução da documentação;
- roadmap sugerido;
- competências demonstradas;
- próximos passos recomendados.

Este documento não substitui o README nem os guias técnicos específicos. Ele funciona como registro de roadmap e evolução contínua do projeto.

---

## Conteúdo Principal

### 1. Visão geral da evolução

O projeto já cobre as principais etapas de um pipeline moderno de dados:

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
Serving
   ↓
Power BI
```

As oportunidades de evolução estão organizadas em quatro grandes dimensões:

| Dimensão | Foco |
|---|---|
| Engenharia de Dados | Orquestração, CI/CD, logs, testes, padronização e confiabilidade. |
| ML/NLP | Melhoria da classificação, avaliação formal e modelos mais avançados. |
| Analytics | Novas análises, indicadores e expansão histórica. |
| Governança | Data Quality, contratos, lineage e monitoramento operacional. |

### 2. Limitações atuais

As limitações abaixo não invalidam o projeto. Elas representam pontos naturais de evolução para transformar uma solução de portfólio em uma solução mais próxima de produção.

#### Execução ainda parcialmente manual

Atualmente, a execução do pipeline depende da chamada manual dos runners ou notebooks equivalentes.

Fluxo atual:

```text
Bronze → Silver → ML → Gold → Star Schema → Serving
```

Possível limitação:

- não há ainda uma orquestração externa completa com agendamento, dependências formais, retries e alertas.

Evolução possível:

- utilizar Databricks Workflows, Apache Airflow, Prefect ou Dagster para orquestrar o pipeline ponta a ponta.

#### Ausência de CI/CD completo

O projeto possui estrutura modular e testes, mas ainda pode evoluir para um fluxo completo de integração contínua.

Possível limitação:

- validações automatizadas podem não estar totalmente integradas ao GitHub Actions ou a outro serviço de CI/CD.

Evolução possível:

- configurar pipeline de CI para executar lint, testes unitários, testes de qualidade, validação de importações, checagem de formatação e validação de documentação.

#### Monitoramento operacional básico

O projeto já considera logs e rastreabilidade, mas o monitoramento pode ser ampliado.

Possível limitação:

- ausência de dashboards operacionais para acompanhar falhas, tempo de execução, volume processado e anomalias.

Evolução possível:

- criar métricas operacionais por execução;
- registrar início, fim, duração e status por dataset;
- criar painel de monitoramento técnico;
- adicionar alertas para falhas ou queda de volume.

#### Classificação ML/NLP ainda evolutiva

O projeto utiliza classificação textual para enriquecer proposições com tema e natureza jurídica.

Possível limitação:

- a classificação pode depender de regras, dicionários e modelos treinados com base limitada;
- alguns textos podem ser classificados por fallback;
- categorias com baixa frequência podem ter menor desempenho.

Evolução possível:

- ampliar a base de treinamento;
- revisar classes com poucos exemplos;
- medir precisão, recall e F1-score por classe;
- criar matriz de confusão;
- versionar datasets de treino;
- comparar diferentes algoritmos;
- testar embeddings ou modelos de linguagem para classificação semântica;
- registrar métricas no MLflow;
- documentar critérios de aceite do modelo.

#### Validações de qualidade podem ser expandidas

O projeto já possui uma camada formal de Data Quality, mas ela pode ser fortalecida.

Possível limitação:

- as validações atuais podem cobrir apenas regras essenciais.

Evolução possível:

- criar contratos de dados executáveis;
- definir regras por camada;
- aplicar validações de domínio;
- validar integridade referencial entre fatos e dimensões;
- monitorar variação de volume entre execuções;
- registrar histórico de resultados das validações;
- impedir publicação na Serving quando regras críticas falharem.

### 3. Melhorias futuras de Engenharia de Dados

Melhorias recomendadas:

- padronizar nomes de funções, módulos e variáveis para manter consistência entre português e inglês;
- revisar e reduzir uso de `print()` em favor de logs estruturados;
- revisar pontos remanescentes com `df.count()` para evitar custo desnecessário em Spark;
- garantir carregamento correto do `.env` em ambiente local;
- centralizar nomes e aliases de modelos ML em configuração;
- criar logs claros de início, fim e erro por dataset;
- configurar CI/CD com GitHub Actions;
- ampliar testes unitários e de integração;
- criar workflow orquestrado com Databricks Workflows, Airflow, Prefect ou Dagster;
- persistir logs operacionais em tabela Delta;
- criar modo de execução parcial por camada ou dataset;
- criar release/tag de portfólio, como `v1.0.0-portfolio`.

### 4. Melhorias futuras de ML/NLP

A classificação de proposições é um dos diferenciais técnicos do projeto.

Melhorias recomendadas:

- ampliar a base de treinamento;
- revisar classes com baixa representatividade;
- medir acurácia, precisão, recall e F1-score por classe;
- gerar matriz de confusão;
- registrar métricas no MLflow;
- criar critérios mínimos para promoção de modelos ao alias `champion`;
- versionar datasets de treino;
- comparar abordagem por regras, modelo clássico e embeddings;
- testar embeddings ou modelos de linguagem para classificação semântica;
- criar avaliação manual de amostras classificadas;
- reduzir conflitos entre temas semelhantes;
- monitorar percentual de fallback;
- documentar evolução dos modelos por versão.

Métricas recomendadas:

- acurácia geral;
- precisão por classe;
- recall por classe;
- F1-score por classe;
- matriz de confusão;
- percentual de registros classificados por regra;
- percentual de registros classificados por ML;
- percentual de registros classificados por fallback.

### 5. Melhorias futuras de Analytics e BI

O projeto pode evoluir na camada analítica para ampliar a leitura sobre a atuação do Congresso.

Análises possíveis:

- evolução temporal da quantidade de proposições;
- temas legislativos mais frequentes por ano ou legislatura;
- distribuição de proposições por partido, UF e parlamentar;
- deputados com maior volume de autoria;
- partidos com maior participação em proposições;
- análise da tramitação das proposições ao longo do tempo;
- órgãos com maior concentração de eventos e tramitações;
- distribuição de votações por período;
- comportamento dos votos por partido;
- participação parlamentar em eventos;
- comparação entre legislaturas;
- identificação de temas prioritários em diferentes períodos políticos.

Melhorias recomendadas no dashboard:

- criar páginas temáticas no Power BI;
- adicionar indicadores executivos;
- documentar medidas DAX reais do `.pbix`;
- criar visão por tema, partido, parlamentar, UF, órgão e período;
- incluir análise de tendências;
- incluir filtros avançados;
- criar seção de storytelling dos dados;
- adicionar página de metodologia;
- incluir análise por legislaturas antigas.

### 6. Ampliação histórica

Uma evolução importante é aumentar o período de análise para incluir legislaturas antigas.

Benefícios:

- permitir comparação entre legislaturas;
- analisar evolução de temas ao longo dos anos;
- identificar mudanças de prioridade legislativa;
- comparar atuação de partidos em diferentes períodos;
- avaliar comportamento parlamentar em janelas históricas maiores.

Cuidados necessários:

- avaliar volume adicional de dados;
- revisar paginação e limites da API;
- ajustar estratégia incremental;
- validar consistência histórica de partidos, deputados e órgãos;
- revisar modelo de tempo e legislatura.

### 7. Evolução de Data Quality e contratos

Possíveis melhorias:

- transformar contratos em arquivos YAML executáveis;
- criar registry formal de contratos por tabela;
- integrar contratos ao runner de cada camada;
- persistir resultados das validações em tabela Delta;
- criar dashboard operacional de qualidade de dados;
- aplicar bloqueio automático antes da camada Serving;
- adicionar validação de integridade referencial entre fatos e dimensões;
- alinhar contratos com schemas físicos finais das tabelas Delta;
- versionar contratos por release do projeto.

### 8. Evolução do modelo dimensional

Possíveis melhorias:

- criar diagrama visual do Star Schema;
- validar integridade referencial entre todos os fatos e dimensões;
- documentar fisicamente o schema final de cada tabela;
- incluir dimensões adicionais para legislatura, mandato e região;
- criar fatos agregados para otimizar consultas no Power BI;
- revisar historização de partido por parlamentar;
- documentar granularidade final com base nas tabelas publicadas;
- alinhar contratos de dados com as tabelas físicas da camada Star.

### 9. Evolução da documentação

A documentação atual cobre os principais blocos do projeto.

Arquivos existentes:

```text
docs/architecture.md
docs/dashboard.md
docs/data_contracts.md
docs/data_quality.md
docs/dax_measures.md
docs/execution_guide.md
docs/lineage.md
docs/ml_nlp.md
docs/project_evolution.md
docs/star_schema.md
```

Possíveis documentos futuros:

```text
docs/troubleshooting.md
docs/sql_examples.md
docs/operations_guide.md
docs/model_diagram.md
```

### 10. Roadmap sugerido

#### Fase 1 — Finalização para portfólio

Objetivo: deixar o projeto claro, executável e bem documentado.

Tarefas recomendadas:

- revisar README;
- incluir links para todos os documentos;
- validar execução do pipeline completo;
- revisar docstrings principais;
- revisar exemplos de execução;
- garantir que o dashboard esteja documentado;
- incluir print do Power BI em `docs/images/dashboard-preview.png`.

#### Fase 2 — Qualidade e confiabilidade

Objetivo: aumentar a confiança nos dados gerados.

Tarefas recomendadas:

- ampliar testes;
- formalizar contratos executáveis;
- registrar resultados de validações;
- criar validações entre camadas;
- validar integridade entre fatos e dimensões;
- criar logs operacionais mais detalhados.

#### Fase 3 — Evolução do ML/NLP

Objetivo: melhorar a classificação automática das proposições.

Tarefas recomendadas:

- ampliar base de treinamento;
- medir desempenho por classe;
- revisar classes com baixa amostra;
- comparar abordagem por regras, modelo clássico e embeddings;
- registrar experimentos no MLflow;
- definir métrica mínima aceitável para publicação do modelo.

#### Fase 4 — Orquestração e produção

Objetivo: aproximar o projeto de uma solução produtiva.

Tarefas recomendadas:

- criar workflow agendado;
- configurar retries;
- criar alertas;
- separar ambientes;
- automatizar testes no GitHub Actions;
- publicar tabelas finais com controle de versão;
- criar documentação de operação.

### 11. Competências demonstradas

Mesmo com pontos de evolução, o projeto já demonstra competências importantes para uma vaga júnior em Engenharia de Dados:

- consumo de APIs públicas;
- organização de projeto Python;
- PySpark;
- Delta Lake;
- arquitetura medalhão;
- modelagem dimensional;
- Star Schema;
- Fact Tables;
- Dimension Tables;
- qualidade de dados;
- contratos de dados;
- documentação técnica;
- classificação textual com ML/NLP;
- integração com Power BI;
- visão de pipeline ponta a ponta;
- preocupação com manutenção e evolução.

### 12. Próximos passos recomendados

Próximos passos de maior impacto:

1. adicionar a imagem real do dashboard em `docs/images/dashboard-preview.png`;
2. validar links do README e da pasta `docs/`;
3. executar testes com `pytest`;
4. executar lint com `ruff`;
5. revisar `.env.example` e carregamento de variáveis;
6. validar execução ponta a ponta;
7. criar tag/release de portfólio;
8. divulgar o projeto no currículo e LinkedIn.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para roadmap, evolução e próximos passos do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta as evoluções futuras de forma resumida;
- `docs/architecture.md`, que mostra a base arquitetural atual;
- `docs/execution_guide.md`, que pode evoluir com orquestração e automação;
- `docs/ml_nlp.md`, que detalha a camada de classificação a ser aprimorada;
- `docs/data_quality.md`, que pode evoluir para validações bloqueantes;
- `docs/data_contracts.md`, que pode evoluir para contratos executáveis;
- `docs/star_schema.md`, que pode evoluir com novas dimensões e fatos;
- `docs/dashboard.md`, que pode evoluir com novas páginas e análises;
- `docs/dax_measures.md`, que pode evoluir com medidas reais do `.pbix`.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Classificação ML/NLP](ml_nlp.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Linhagem dos Dados](lineage.md)

---

## Próximas evoluções

As próximas evoluções prioritárias são:

- adicionar imagem real do dashboard ao repositório;
- validar execução ponta a ponta;
- configurar CI/CD básico;
- criar release de portfólio;
- ampliar avaliação formal do modelo ML/NLP;
- transformar contratos de dados em validações executáveis;
- ampliar análise para legislaturas antigas;
- evoluir o dashboard com novas análises sobre atuação do Congresso.
