# Evolução do Projeto

Este documento registra as limitações atuais, oportunidades de melhoria e próximos passos do projeto `projeto_api_dados_abertos_camara`.

O objetivo é deixar claro que o projeto já possui uma arquitetura funcional para portfólio, mas também apresenta possibilidades reais de evolução técnica, aproximando-o de um cenário mais produtivo de Engenharia de Dados.

---

## 1. Visão geral

O projeto implementa um pipeline de dados com dados públicos da Câmara dos Deputados, utilizando:

- ingestão de dados via API pública;
- arquitetura medalhão;
- processamento com PySpark;
- armazenamento em Delta Lake;
- camada Bronze, Silver e Gold;
- classificação textual com regras e ML/NLP;
- modelo dimensional em Star Schema;
- camada de Serving;
- consumo analítico em Power BI;
- validações de qualidade de dados;
- documentação técnica na pasta `docs/`.

Essa estrutura demonstra uma visão ponta a ponta de um projeto de dados, desde a coleta até a disponibilização para análise.

---

## 2. Limitações atuais

As limitações abaixo não invalidam o projeto. Elas representam pontos naturais de evolução para transformar uma solução de portfólio em uma solução mais próxima de produção.

### 2.1 Execução ainda parcialmente manual

Atualmente, a execução do pipeline depende da chamada manual dos runners ou notebooks equivalentes.

Fluxo atual:

```text
Bronze → Silver → ML → Gold → Star Schema → Serving
```

Possível limitação:

- não há ainda uma orquestração externa completa com agendamento, dependências formais, retries e alertas.

Evolução possível:

- utilizar Databricks Workflows, Apache Airflow, Prefect ou Dagster para orquestrar o pipeline ponta a ponta.

---

### 2.2 Ausência de CI/CD completo

O projeto possui estrutura modular e testes, mas ainda pode evoluir para um fluxo completo de integração contínua.

Possível limitação:

- validações automatizadas podem não estar totalmente integradas ao GitHub Actions ou a outro serviço de CI/CD.

Evolução possível:

- configurar pipeline de CI para executar:
  - lint;
  - testes unitários;
  - testes de qualidade de dados;
  - validação de importações;
  - checagem de formatação;
  - validação de documentação.

---

### 2.3 Monitoramento operacional básico

O projeto já considera logs e rastreabilidade, mas o monitoramento pode ser ampliado.

Possível limitação:

- ausência de dashboards operacionais para acompanhar falhas, tempo de execução, volume processado e anomalias.

Evolução possível:

- criar métricas operacionais por execução;
- registrar início, fim, duração e status por dataset;
- criar painel de monitoramento técnico;
- adicionar alertas para falhas ou queda de volume.

---

### 2.4 Classificação ML/NLP ainda evolutiva

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

---

### 2.5 Validações de qualidade podem ser expandidas

O projeto já possui uma camada formal de Data Quality, mas ela pode ser fortalecida.

Possível limitação:

- as validações atuais podem cobrir apenas regras essenciais.

Evolução possível:

- criar contratos de dados por tabela;
- definir regras por camada;
- aplicar validações de domínio;
- validar integridade referencial entre fatos e dimensões;
- monitorar variação de volume entre execuções;
- registrar histórico de resultados das validações;
- impedir publicação na Serving quando regras críticas falharem.

---

### 2.6 Modelo dimensional pode ganhar novas métricas

O Star Schema atual organiza fatos e dimensões para análise, mas pode receber novos indicadores.

Possível limitação:

- nem todas as análises legislativas possíveis estão contempladas no modelo atual.

Evolução possível:

- criar novas métricas sobre tramitação de proposições;
- calcular tempo médio entre etapas legislativas;
- medir produtividade por parlamentar, partido, UF ou órgão;
- criar indicadores de participação em eventos;
- criar métricas de votação por partido ou orientação;
- adicionar dimensões auxiliares para análise temporal e temática.

---

### 2.7 Dashboard pode evoluir em profundidade analítica

O projeto possui consumo em Power BI, mas o dashboard pode ser expandido.

Possível limitação:

- o dashboard pode estar concentrado em uma primeira versão analítica.

Evolução possível:

- criar páginas temáticas no Power BI;
- adicionar indicadores executivos;
- documentar medidas DAX;
- criar visão por tema, partido, parlamentar, UF e período;
- incluir análise de tendências;
- incluir filtros avançados;
- criar seção de storytelling dos dados.

---

### 2.8 Ambiente produtivo ainda não formalizado

O projeto foi desenvolvido com foco em portfólio, portanto algumas práticas produtivas podem ser simuladas ou parcialmente implementadas.

Possível limitação:

- não há necessariamente separação formal de ambientes como desenvolvimento, homologação e produção.

Evolução possível:

- separar ambientes por configuração;
- criar schemas diferentes por ambiente;
- parametrizar paths e catálogos;
- adotar secrets para credenciais;
- criar processo de deploy automatizado;
- definir convenções de versionamento.

---

## 3. Melhorias futuras recomendadas

As melhorias abaixo estão organizadas por prioridade.

### 3.1 Prioridade alta

- Revisar execução completa ponta a ponta após cada alteração relevante.
- Garantir que o carregamento do `.env` funcione corretamente em ambiente local.
- Reduzir uso de `print()` em favor de logs estruturados.
- Revisar pontos remanescentes com `df.count()` para evitar custo desnecessário.
- Garantir logs claros de início, fim e erro por dataset.
- Validar aliases dos modelos ML utilizados na inferência.
- Consolidar documentação do README com links para todos os arquivos da pasta `docs/`.

---

### 3.2 Prioridade média

- Criar testes unitários para transformações críticas.
- Criar testes de integração para runners principais.
- Criar contratos de dados por tabela.
- Registrar métricas de Data Quality em uma tabela histórica.
- Expandir métricas do dashboard Power BI.
- Melhorar documentação das medidas DAX utilizadas.
- Documentar exemplos de consultas SQL nas tabelas finais.

---

### 3.3 Prioridade baixa

- Criar automação de deploy.
- Criar ambiente de demonstração reproduzível.
- Adicionar badges no README.
- Adicionar diagrama visual da arquitetura.
- Criar exemplos de análise exploratória.
- Adicionar comparação entre versões do modelo ML.

---

## 4. Roadmap sugerido

### Fase 1 — Finalização para portfólio

Objetivo: deixar o projeto claro, executável e bem documentado.

Tarefas recomendadas:

- revisar README;
- incluir links para todos os documentos;
- validar execução do pipeline completo;
- revisar docstrings principais;
- revisar exemplos de execução;
- garantir que o dashboard esteja documentado;
- incluir prints ou descrição das principais páginas do Power BI.

---

### Fase 2 — Qualidade e confiabilidade

Objetivo: aumentar a confiança nos dados gerados.

Tarefas recomendadas:

- ampliar testes;
- formalizar contratos de dados;
- registrar resultados de validações;
- criar validações entre camadas;
- validar integridade entre fatos e dimensões;
- criar logs operacionais mais detalhados.

---

### Fase 3 — Evolução do ML/NLP

Objetivo: melhorar a classificação automática das proposições.

Tarefas recomendadas:

- ampliar base de treinamento;
- medir desempenho por classe;
- revisar classes com baixa amostra;
- comparar abordagem por regras, modelo clássico e embeddings;
- registrar experimentos no MLflow;
- definir métrica mínima aceitável para publicação do modelo.

---

### Fase 4 — Orquestração e produção

Objetivo: aproximar o projeto de uma solução produtiva.

Tarefas recomendadas:

- criar workflow agendado;
- configurar retries;
- criar alertas;
- separar ambientes;
- automatizar testes no GitHub Actions;
- publicar tabelas finais com controle de versão;
- criar documentação de operação.

---

## 5. Possíveis evoluções arquiteturais

### 5.1 Orquestração com Databricks Workflows

Uma evolução natural é transformar a execução sequencial dos runners em um workflow com dependências explícitas:

```text
Bronze
  ↓
Silver
  ↓
ML Training
  ↓
Gold
  ↓
Star Schema
  ↓
Serving
```

Benefícios:

- melhor controle de falhas;
- histórico de execuções;
- agendamento;
- retries;
- observabilidade operacional.

---

### 5.2 Integração com GitHub Actions

O GitHub Actions pode ser usado para validar o projeto a cada push ou pull request.

Exemplos de validações:

- instalação das dependências;
- execução dos testes;
- validação de lint;
- checagem de imports;
- validação de documentação Markdown.

---

### 5.3 Camada de métricas operacionais

Criar uma tabela de monitoramento técnico permitiria acompanhar a saúde do pipeline.

Exemplo de campos:

```text
execution_id
camada
dataset
status
started_at
finished_at
duration_seconds
rows_read
rows_written
error_message
```

Benefícios:

- rastreabilidade;
- análise de falhas;
- comparação entre execuções;
- base para alertas.

---

### 5.4 Data Quality como etapa bloqueante

Uma evolução importante é impedir que dados inconsistentes avancem para camadas analíticas.

Exemplo:

```text
se validação crítica falhar:
    não publicar na Serving
```

Benefícios:

- maior confiabilidade;
- redução de erro no dashboard;
- melhor governança dos dados.

---

## 6. Evolução da classificação de proposições

A classificação de proposições é um dos pontos mais importantes para evolução do projeto.

### Melhorias possíveis

- separar claramente classificação por regras e classificação por ML;
- medir cobertura das regras;
- medir acurácia do modelo ML;
- criar avaliação manual de amostras classificadas;
- balancear classes com poucos exemplos;
- revisar temas sobrepostos;
- criar hierarquia de temas;
- usar embeddings para capturar similaridade semântica;
- registrar versão do modelo utilizada em cada execução;
- salvar a origem da classificação em campo próprio.

### Métricas recomendadas

- acurácia geral;
- precisão por classe;
- recall por classe;
- F1-score por classe;
- matriz de confusão;
- percentual de registros classificados por regra;
- percentual de registros classificados por ML;
- percentual de registros classificados por fallback.

---

## 7. Evolução do dashboard

O dashboard pode ser expandido para contar melhor a história dos dados legislativos.

### Ideias de páginas

- visão geral legislativa;
- análise de proposições por tema;
- análise por parlamentar;
- análise por partido;
- análise por UF;
- tramitação e tempo médio;
- votações e posicionamentos;
- presença em eventos;
- evolução temporal.

### Melhorias técnicas

- documentar tabelas usadas;
- documentar medidas DAX;
- revisar relacionamentos no modelo Power BI;
- criar calendário analítico;
- padronizar nomes de medidas;
- separar medidas por pasta temática;
- incluir página de metodologia.

---

## 8. Evolução da documentação

A documentação atual já cobre os principais blocos do projeto, mas pode ser ampliada com documentos complementares.

Arquivos existentes:

```text
docs/architecture.md
docs/dashboard.md
docs/data_quality.md
docs/execution_guide.md
docs/lineage.md
docs/ml_nlp.md
docs/star_schema.md
docs/project_evolution.md
```

Possíveis documentos futuros:

```text
docs/troubleshooting.md
docs/data_contracts.md
docs/sql_examples.md
docs/dax_measures.md
docs/operations_guide.md
```

---

## 9. O que este projeto demonstra

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
- documentação técnica;
- classificação textual com ML/NLP;
- integração com Power BI;
- visão de pipeline ponta a ponta;
- preocupação com manutenção e evolução.

---

## 10. Conclusão

O projeto está estruturado como uma solução completa de portfólio, cobrindo ingestão, transformação, enriquecimento, modelagem dimensional e visualização.

As próximas evoluções devem priorizar:

1. execução ponta a ponta validada;
2. automação e orquestração;
3. melhoria da classificação ML/NLP;
4. ampliação da qualidade de dados;
5. documentação de métricas e dashboard;
6. preparação para um cenário mais próximo de produção.

Essas melhorias reforçam a maturidade do projeto e mostram capacidade de pensar não apenas no código, mas também em arquitetura, confiabilidade, governança e evolução contínua.
